function getUcucuga(searchForm){
    let formData = new FormData(searchForm);
    let search = new URLSearchParams(formData);
    let queryString = search.toString();

    var token = document.URL.split('/')[3] 
    const url = `/${token}/api/get-ucucuga?${queryString}`;
    fetch(url, {
        method: 'GET',
    })
    .then(response => {
        if (response.ok) {
            return response.json();
        } else {
            console.error('Request failed');
        }
    })
    .then( result => {
        parseJson(result)
    })
    .catch(error => {
        console.error('An error occurred:', error);
    });
}

function parseJson(data){
    const tableContainer = document.getElementById('result-table');
    tableContainer.innerHTML = '';
    if (data["data"].length == 0){
        document.getElementById('error_message').innerHTML = 'Уцуцуга не найдена!';
        return;
    }
    else{
        document.getElementById('error_message').innerHTML = '';
    }
    const table = document.createElement('table');
    const headerRow = document.createElement('tr');
    const properties = data["order"]; 
    properties.forEach((property) => {
        const headerCell = document.createElement('th');
        headerCell.textContent = property;
        headerRow.appendChild(headerCell);
    });

    table.appendChild(headerRow);

    data["data"].forEach((element) => {
        const row = document.createElement('tr');

        properties.forEach((property) => {
            const cell = document.createElement('td');
            cell.textContent = element[property];
            row.appendChild(cell);
            });

        table.appendChild(row);
    });
    
    tableContainer.appendChild(table);
}