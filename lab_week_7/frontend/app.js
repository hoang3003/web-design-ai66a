const tableBody = document.querySelector("#items-table-body");
const fetchButton = document.querySelector("#fetch-button");

async function fetchData() {
  try {
    const response = await fetch("/items");
    if (!response.ok) {
      const error = await response.json();
      throw new Error(error.detail || "Could not fetch items");
    }

    const data = await response.json();
    tableBody.innerHTML = "";

    data.items.forEach((item) => {
      const row = document.createElement("tr");

      const idCell = document.createElement("td");
      idCell.textContent = item.id;

      const nameCell = document.createElement("td");
      nameCell.textContent = item.name;

      const priceCell = document.createElement("td");
      priceCell.textContent = item.price;

      const actionCell = document.createElement("td");
      const deleteButton = document.createElement("button");
      deleteButton.type = "button";
      deleteButton.className = "delete-button";
      deleteButton.textContent = "Delete";
      deleteButton.addEventListener("click", () => deleteItem(item.id));
      actionCell.appendChild(deleteButton);

      row.append(idCell, nameCell, priceCell, actionCell);
      tableBody.appendChild(row);
    });
  } catch (error) {
    alert(error.message);
  }
}

async function deleteItem(itemId) {
  const response = await fetch(`/items/${itemId}`, { method: "DELETE" });

  if (response.ok) {
    await fetchData();
    return;
  }

  let message = "Could not delete item";
  try {
    const error = await response.json();
    message = error.detail || message;
  } catch {
    // Keep the default message when the server does not return JSON.
  }
  alert(message);
}

fetchButton.addEventListener("click", fetchData);
