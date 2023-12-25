function createTable(data, idNames) {
    const table = document.createElement('table');
    table.className = 'center';

    const caption = document.createElement('caption');
    caption.className = 'tableCaption'
    caption.textContent = data.caption_text;
    table.appendChild(caption);

    const headerRow = document.createElement('tr');
    data.titles.forEach(title => {
        const th = document.createElement('th');
        th.textContent = title;
        headerRow.appendChild(th);
    });
    table.appendChild(headerRow);

    data.context.forEach(rowData => {
        const row = document.createElement('tr');
        idNames.forEach(idName => {
            row.setAttribute(idName, rowData.pop())
        });
        rowData.forEach(cellData => {
            const td = document.createElement('td');
            td.textContent = cellData;
            row.appendChild(td);
        });
        table.appendChild(row);
    });

    return table;
}
