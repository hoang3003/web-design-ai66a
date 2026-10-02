from sqlmodel import Session, SQLModel, select

from app.database import engine
from app.models import Hero, Mission, Team


def seed():
    SQLModel.metadata.create_all(engine)

    with Session(engine) as session:
        existing_team = session.exec(select(Team)).first()

        if existing_team:
            print("Database already seeded.")
            return

        avengers = Team(
            name="Avengers",
            headquarters="New York",
        )

        xmen = Team(
            name="X-Men",
            headquarters="Westchester",
        )

        mission1 = Mission(
            title="Battle of Sokovia"
        )

        mission2 = Mission(
            title="Save New York"
        )

        peter = Hero(
            name="Peter",
            age=18,
            secret_name="Spider-Man",
            team=avengers,
            missions=[mission1],
        )

        tony = Hero(
            name="Tony",
            age=45,
            secret_name="Iron Man",
            team=avengers,
            missions=[mission1, mission2],
        )

        natasha = Hero(
            name="Natasha",
            age=35,
            secret_name="Black Widow",
            team=avengers,
            missions=[mission2],
        )

        logan = Hero(
            name="Logan",
            age=150,
            secret_name="Wolverine",
            team=xmen,
        )

        scott = Hero(
            name="Scott",
            age=32,
            secret_name="Cyclops",
            team=xmen,
        )

        session.add(avengers)
        session.add(xmen)

        session.add(peter)
        session.add(tony)
        session.add(natasha)
        session.add(logan)
        session.add(scott)

        session.commit()

        print("Database seeded successfully.")


if __name__ == "__main__":
    seed()
