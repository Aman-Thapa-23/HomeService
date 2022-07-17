const SearchField = document.querySelector("#SearchField");
const appTable = document.querySelector(".app-table");
const tableOutput = document.querySelector(".table-output");
const tableOutputBody = document.querySelector(".table-output-body");
const paginationContainer = document.querySelector(".pagination-container");
const noResults = document.querySelector(".no-results");

tableOutput.style.display = "none";

SearchField.addEventListener("keyup", SearchValue);

function SearchValue(event) {
  const searchVal = event.target.value;

  if (searchVal.trim().length > 0) {
    paginationContainer.style.display = "none";

    tableOutputBody.innerHTML = "";

    fetch("/service/search-worker", {
      body: JSON.stringify({ searchText: searchVal }),
      method: "POST",
    })
      .then((response) => response.json())
      .then((data) => {
        console.log("data", data);
        appTable.style.display = "none";
        tableOutput.style.display = "block";

        console.log("data.length", data.length);

        if (data.length === 0) {
          noResults.style.display = "block";
          tableOutput.style.display = "none";
        } else {
          noResults.style.display = "none";

          data.forEach((item) => {
            tableOutputBody.innerHTML += `
                  <tr>
                    <td>${item.worker.category_name}</td>
                    <td>${item.worker.user.name}</td>
                    <td>${item.worker.user.phone_number}</td>
                    <td>${item.worker.user.address}</td>
                    <td>${item.booking_date}</td>
                    <td>${item.booking_time}</td>
                    <td>${item.status}</td>
                    <td>${item.is_complete}</td>
                  </tr>
                  `;
          });
        }
      });
  } else {
    tableOutput.style.display = "none";
    appTable.style.display = "block";
    paginationContainer.style.display = "block";
  }
}
