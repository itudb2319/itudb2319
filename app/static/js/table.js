// Function to create the table
function createTable(data) {
    const table = document.createElement('table');
    table.className = 'center';

    // Add caption
    const caption = document.createElement('caption');
    caption.className = 'table-caption'
    caption.textContent = data.caption_text;
    table.appendChild(caption);

    // Add header row
    const headerRow = document.createElement('tr');
    data.titles.forEach(title => {
        const th = document.createElement('th');
        th.textContent = title;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    // Add data rows
    data.context.forEach(rowData => {
        const row = document.createElement('tr');
        rowData.forEach(cellData => {
            const td = document.createElement('td');
            td.textContent = cellData;
            row.appendChild(td);
        });
        table.appendChild(row);
    });

    return table;
}
