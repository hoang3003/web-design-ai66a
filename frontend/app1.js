async function greet() {
    return "Hello";
}
console.log(greet());

//c1
function getData() {
    let text = "";
    greet().then((response) => {
    text = response;
});
return text;
}
console.log(getData());

//c2
async function getData() {
    const response = await greet();
    return text;
}


console.log(getData());

async function fetchUsers() {
    try {
        const res = await fetch('https://jsonplaceholder.typicode.com/users');
        const users = await res.json();
        renderUsers(users);
    } catch (err) {
        console.error('Error fetching users:', err);
    } finally {
        renderUsers(users);
    }
}

// fetchUsers();