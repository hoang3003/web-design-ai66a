const fetchUsersButton = document.querySelector('#fetch-users');
const userTableBody = document.querySelector('#user-table-body');

async function fetchUsers() {
    fetchUsersButton.disabled = true;
    fetchUsersButton.textContent = 'Loading...';

    try {
        const response = await fetch('https://jsonplaceholder.typicode.com/users');

        if (!response.ok) {
            throw new Error('Unable to fetch users.');
        }

        const users = await response.json();
        userTableBody.innerHTML = users.map((user) => `
            <tr>
                <td>${user.id}</td>
                <td>${user.name}</td>
                <td>${user.phone}</td>
                <td>${user.email}</td>
                <td>${user.website}</td>
                <td>${user.address.city}, ${user.address.street}</td>
            </tr>
        `).join('');
    } catch (error) {
        userTableBody.innerHTML = `
            <tr>
                <td colspan="6">${error.message}</td>
            </tr>
        `;
    } finally {
        fetchUsersButton.disabled = false;
        fetchUsersButton.textContent = 'Fetch Users';
    }
}

fetchUsersButton.addEventListener('click', fetchUsers);