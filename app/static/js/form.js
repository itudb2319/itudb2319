function combineAndSendForms(action, ...formNames) {
    var showFormData = new FormData(document.getElementById(formNames[0]));

    for (var i = 1; i < formNames.length; i++) {
        var formData = new FormData(document.getElementById(formNames[i]));
        for (var pair of formData.entries()) {
            showFormData.append(pair[0], pair[1]);
        }
    }

    var combinedForm = document.createElement('form');
    combinedForm.method = 'POST';
    combinedForm.action = action;

    for (var pair of showFormData.entries()) {
        var input = document.createElement('input');
        input.type = 'hidden';
        input.name = pair[0];
        input.value = pair[1];
        combinedForm.appendChild(input);
    }

    document.body.appendChild(combinedForm);
    combinedForm.submit();
}

document.addEventListener('DOMContentLoaded', function () {
    var searchBox = document.getElementById('searchBoxArea');
    if (searchBox) {
        searchBox.addEventListener('keypress', function (e) {
            if (e.key === 'Enter') {
                e.preventDefault();
                action = document.getElementById('searchBoxForm').getAttribute('action')
                combineAndSendForms(action, 'showForm', 'orderByForm', 'searchBoxForm', 'limitterForm')
            }
        });
    }
});

document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("deleteOperation").addEventListener("click", function(event) {
        event.preventDefault();

        const checkboxes = document.querySelectorAll('#checkboxDelete:checked');
        if (checkboxes.length > 0) {
            const form = document.createElement('form');
            form.method = 'POST';
            action = document.getElementById('searchBoxForm').getAttribute('action');
            form.action = action;

            checkboxes.forEach(function(checkbox) {
                const input = document.createElement('input');
                input.type = 'checkbox';
                input.name = checkbox.name;
                input.value = checkbox.value;
                form.appendChild(input);
                input.checked = true;
            });

            document.body.appendChild(form);
            form.setAttribute('id', 'deleteForm');
            combineAndSendForms(action, 'showForm', 'orderByForm', 'searchBoxForm', 'deleteForm', 'limitterForm');
        }
    });
});

function postInputs(row, tableName) {
    var inputElements = row.querySelectorAll('.shrink');
    var form = document.getElementById('updateForm');

    var tnInput = document.createElement('input');
    tnInput.type = 'hidden';
    tnInput.name = 'table';
    tnInput.value = tableName;
    form.appendChild(tnInput);

    var idInput = document.createElement('input');
    idInput.type = 'hidden';
    idInput.name = 'id';
    idInput.value = row.getAttribute('id');
    form.appendChild(idInput);

    var button = document.getElementById('updateButton');
    var buttonValue = button.value; 
    
    inputElements.forEach(function(inputElement) {
        var newInput = document.createElement('input');
        newInput.type = 'hidden';
        newInput.name = inputElement.name + "_" + inputElement.value + "_" + buttonValue;
        newInput.value = "updateElement";
        form.appendChild(newInput);
    });
    
    form.type = 'hidden';
    form.setAttribute('id', 'updateForm')
    action = document.getElementById('searchBoxForm').getAttribute('action')
    combineAndSendForms(action, 'showForm', 'orderByForm', 'searchBoxForm', 'updateForm', 'limitterForm')
}


function insertRowAfter(button, tableName) {
    var currentRow = button.parentNode.parentNode;
    
    if ((currentRow.nextSibling && currentRow.nextSibling.className !== 'updateRow') || !currentRow.nextSibling) {
        var newRow = document.createElement('tr');
        newRow.id = currentRow.getAttribute('id');
        newRow.className = 'updateRow';
        var newCell = document.createElement('td');
        newRow.appendChild(newCell);
        
        for (var i = 0; i < currentRow.cells.length; i++) {
            var currentCell = currentRow.cells[i];
            
            if (currentCell.className != 'admin') {
                var newCell = document.createElement('td');
                var inputElement = document.createElement('input');
                inputElement.classList.add('shrink');
                inputElement.name = currentCell.getAttribute('titlename');
                inputElement.value = currentCell.textContent;
                newCell.appendChild(inputElement);
                newRow.appendChild(newCell);
            }
        }

        var submitButton = document.createElement('button');
        submitButton.value = currentRow.id;
        submitButton.textContent = 'Apply';

        submitButton.onclick = function() { postInputs(newRow, tableName); };
        submitButton.className = 'f1-button';
        newRow.appendChild(submitButton);
        
        currentRow.parentNode.insertBefore(newRow, currentRow.nextSibling);
        
    }
    return false;
}


document.addEventListener("DOMContentLoaded", function() {
    document.getElementById("createSendButton").addEventListener("click", function(event) {
        event.preventDefault();
        var insertElements = document.querySelectorAll('#insertElements');
        const form = document.createElement('form');
        form.method = 'POST';
        action = document.getElementById('searchBoxForm').getAttribute('action');
        form.action = action;

        insertElements.forEach(function (item) {
            var input = document.createElement('input');
            input.type = 'hidden';
            input.name = item.name + "_" + item.value
            input.value = item.id
            form.appendChild(input);
        });

        document.body.appendChild(form);
        form.setAttribute('id', 'createForm');
        combineAndSendForms(action, 'showForm', 'orderByForm', 'searchBoxForm', 'createForm', 'limitterForm');
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const selectElement = document.getElementById('limNumber');
    
    selectElement.addEventListener('change', function() {
        action = document.getElementById('searchBoxForm').getAttribute('action');
        combineAndSendForms(action, 'showForm', 'orderByForm', 'searchBoxForm', 'limitterForm')
    });
});