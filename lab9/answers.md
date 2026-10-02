## Part 1 — SQL Warm-up

## Question 1

1. UNIQUE constraint: team name `Avengers` already exists.
2. FOREIGN KEY constraint: team_id 99 does not exist in team.
3. NOT NULL constraint: hero.name was not provided.
4. FOREIGN KEY constraint: team 1 is still referenced by heroes.

## Question 2

The foreign key is stored in the `hero` table because one team can have many heroes,
while each hero belongs to at most one team.

Therefore, every hero row stores the id of its team in `team_id`.

## Question 3

hero

- id (PK)
- name
- ...

mission

- id (PK)
- title

hero_mission

- hero_id (PK, FK -> hero.id)
- mission_id (PK, FK -> mission.id)

`hero_mission` is the link table for the many-to-many relationship.

## Part 2 — Project Setup and DATABASE_URL

## Question 4

We should read the `DATABASE_URL` from an environment variable instead of hardcoding it in `database.py` for two reasons:

1. **Security:** The database URL may contain sensitive information such as the username and password. Using an environment variable prevents these credentials from being stored directly in the source code or accidentally committed to Git.

2. **Flexibility:** Different environments such as development, testing, and production may use different databases. Using an environment variable allows us to change the database connection without modifying the source code.

## Part 3 — Define the Models

## Question 5

`id` is typed as `int | None` with `default=None` because a new Python object does not have an ID before it is inserted into the database.

After the object is inserted, PostgreSQL generates the primary key value, so the stored row has an integer ID.

## Question 6

The attributes of `Hero` that become database columns are:

- `id`
- `name`
- `age`
- `team_id`
- `secret_name`

The `team` attribute does not become a database column because it is defined as a `Relationship`.

`back_populates` connects both sides of the relationship. `Hero.team` refers to the team that a hero belongs to, while `Team.heroes` refers to the list of heroes that belong to that team.

## Part 4 — Engine, Tables and Session

## Question 7

The `hero` table generated from SQLModel has these columns:

- `id`: integer, NOT NULL, primary key, generated using the `hero_id_seq` sequence
- `name`: character varying, NOT NULL
- `age`: integer, nullable
- `team_id`: integer, nullable
- `secret_name`: character varying, NOT NULL

It also has:

- Primary key: `hero_pkey` on `id`
- Index: `ix_hero_name` on `name`
- Foreign key: `hero_team_id_fkey`, where `team_id` references `team(id)`

Compared with the manual table from Part 1, the SQLModel-generated table adds the `secret_name` column and an index on `name`.

The primary key and foreign key relationships are the same in meaning, but PostgreSQL gives them generated constraint names. The `id` column also shows the sequence used to generate new IDs.

## Question 8

After restarting the server, `CREATE TABLE` was not printed again.

`SQLModel.metadata.create_all(engine)` first checks whether the tables already exist. Since the `hero` and `team` tables were already present, it did not create them again.

`create_all()` creates missing tables, but it does not modify or recreate existing tables.

## Question 9

The line that makes sure the `Hero` and `Team` models are registered is:

```python
from app.models import Hero, Team
```

Importing these models registers their table metadata in `SQLModel.metadata`, so `create_all()` knows that the `hero` and `team` tables should exist.

## Part 5 — CRUD Endpoints for Heroes

## Question 10

After commenting out `session.commit()` and trying to create a new hero, the API returned:

```text
500 Internal Server Error
```

I then checked the database with:

```sql
SELECT * FROM hero;
```

The new hero was not present in the database. Only the previously committed rows remained.

`session.add(hero)` only adds the object to the current SQLAlchemy session. It does not permanently save the row to PostgreSQL by itself.

`session.commit()` commits the transaction and permanently saves the changes to the database.

`session.refresh(hero)` reloads the object from the database after the commit so that the Python object contains the latest database-generated values, such as the generated `id`.

## Question 11

When I sent a PATCH request with:

```json
{
  "age": 18
}
```

SQLAlchemy generated an `UPDATE` statement that updated only the `age` column for the selected hero.

The reason is that the PATCH endpoint uses:

```python
hero_in.model_dump(exclude_unset=True)
```

This includes only the fields that the client actually sent in the request. Therefore, since only `age` was provided, only the `age` field was changed instead of updating every column.

## Question 12

The JSON returned by `GET /heroes/{id}` does not include `secret_name`.

The endpoint uses:

```python
@app.get("/heroes/{hero_id}", response_model=HeroPublic)
```

`HeroPublic` does not contain the `secret_name` field, so FastAPI filters it out of the response before sending the JSON to the client.

## Part 6 — Teams, Filtering, Pagination and Errors

## Question 13

When I called:

```text
GET /heroes?min_age=18&team_id=1
```

SQLAlchemy generated:

```sql
WHERE hero.age >= %(age_1)s::INTEGER
AND hero.team_id = %(team_id_1)s::INTEGER
ORDER BY hero.id
LIMIT %(param_1)s::INTEGER
OFFSET %(param_2)s::INTEGER
```

with parameters:

```text
{'age_1': 18, 'team_id_1': 1, 'param_1': 10, 'param_2': 0}
```

The values `18` and `1` appear in the parameter dictionary as `age_1` and `team_id_1`, rather than being inserted directly into the SQL string.

This is safe against SQL injection because SQLAlchemy uses bound parameters. The SQL statement and the values are sent separately, so PostgreSQL treats the values as data instead of executable SQL code.

## Question 14

Filtering in the database is more efficient than loading all rows into Python and filtering them afterwards.

When filtering in the database, PostgreSQL only returns the rows that match the condition. This reduces the amount of data transferred from the database to the application and uses less memory in Python.

The database can also optimize `WHERE` conditions and use indexes when available, which makes filtering more efficient, especially when the table contains many rows.

## Part 7 — Many-to-Many: Missions

## Question 15

`SQLModel.metadata.create_all(engine)` creates tables that do not already exist in the database.

When the application restarted after adding `Mission` and `HeroMissionLink`, the `mission` and `heromissionlink` tables were created because they were new.

The existing `hero` and `team` tables were not recreated because they already existed.

Therefore, `create_all()` creates missing tables, but it does not modify or recreate existing tables.

## Part 8 — Seed Script

## Question 16

When I ran the seed script, the relevant INSERT statements were executed in this order:

```sql
INSERT INTO team ...
INSERT INTO mission ...
INSERT INTO hero ...
INSERT INTO heromissionlink ...
```

For example, SQLAlchemy inserted the teams first:

```text
Avengers -> id 1
X-Men -> id 2
```

Then the hero INSERT used the generated team IDs:

```text
Peter   -> team_id = 1
Tony    -> team_id = 1
Natasha -> team_id = 1
Logan   -> team_id = 2
Scott   -> team_id = 2
```

I did not manually assign `team_id` in the seed script. Instead, I assigned the relationship, for example:

```python
team=avengers
```

SQLAlchemy inserted the `Team` object first, PostgreSQL generated its primary key, and SQLAlchemy then used that generated ID as the corresponding hero's `team_id`.

The mission relationships worked similarly. After the heroes and missions had IDs, SQLAlchemy inserted rows into `heromissionlink`, such as:

```text
hero 1 -> mission 1
hero 2 -> mission 1
hero 2 -> mission 2
hero 3 -> mission 2
```

So the foreign-key values were populated automatically from the Python relationships rather than being manually typed.

## Part 9 — Migrations with Alembic

## Question 17

After adding:

```python
power: str | None = None
```

to `HeroBase` and restarting the application, the `hero` table still did not contain a `power` column.

The current database schema still contained only:

```text
name
age
team_id
id
secret_name
```

This happens because `SQLModel.metadata.create_all(engine)` only creates tables that do not exist. It does not modify the schema of an existing table.

Therefore, the Python model and the PostgreSQL table become out of sync after adding `power`.

Dropping all tables and running `create_all()` again is not an acceptable solution in production because it would delete existing data. Database migrations should be used instead so the schema can be changed while preserving the existing records.

## Question 18

### `upgrade()`

```python
def upgrade() -> None:
    """Upgrade schema."""
    op.add_column(
        'hero',
        sa.Column(
            'power',
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=True
        )
    )
```

`upgrade()` adds a new nullable `power` column to the `hero` table.

### `downgrade()`

```python
def downgrade() -> None:
    """Downgrade schema."""
    op.drop_column('hero', 'power')
```

`downgrade()` reverses the migration by removing the `power` column from the `hero` table.

## Question 19

Alembic stores the current database revision in the `alembic_version` table.

For example:

```text
version_num
--------------
7f7884903876
```

The `migrations/` folder should be committed to Git because it contains the history of database schema changes.

This allows every developer and deployment environment to apply the same migrations in the same order and keep the database schema consistent.

## Question 20

When I renamed `secret_name` to `alias` in the `Hero` model, Alembic autogenerated the following migration:

### upgrade()

```python
def upgrade() -> None:
    op.add_column(
        'hero',
        sa.Column(
            'alias',
            sqlmodel.sql.sqltypes.AutoString(),
            nullable=False
        )
    )
    op.drop_column('hero', 'secret_name')
```

### downgrade()

```python
def downgrade() -> None:
    op.add_column(
        'hero',
        sa.Column(
            'secret_name',
            sa.VARCHAR(),
            autoincrement=False,
            nullable=False
        )
    )
    op.drop_column('hero', 'alias')
```

Alembic treated the change as adding a new `alias` column and removing the existing `secret_name` column, instead of recognizing it as a column rename.

This is dangerous because dropping `secret_name` would delete the existing data stored in that column.

To preserve the data, the migration should be edited manually to rename the existing column instead of dropping and recreating it.

## Part 10 — Project Integration

This part has no separate numbered question. It applies the work from Parts 1–9 to the group project.
