function toggleDropdownButton(actual, other1, other2) {
    var dropdownActual = document.getElementById(actual);
    var dropdownOther1 = document.getElementById(other1);
    if (dropdownActual.style.display === "block") {
        dropdownActual.style.display = "none";
    } else {
        if (dropdownOther1.style.display == "block") {
            dropdownOther1.style.display = "none";
        }
        dropdownActual.style.display = "block";
    }
}

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
                combineAndSendForms(action, 'showForm', 'orderByForm', 'searchBoxForm')
            }
        });
    }
});