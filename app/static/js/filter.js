function toggleDropdownShow() {
    var dropdownActual = document.getElementById("dropdownContentShow");
    var dropdownOther = document.getElementById("dropdownContentOrderBy");
    if (dropdownActual.style.display === "block") {
        dropdownActual.style.display = "none";
    } else {
        if (dropdownOther.style.display == "block") {
            dropdownOther.style.display = "none";
        }
        dropdownActual.style.display = "block";
    }
}

function toggleDropdownOrderBy() {
    var dropdownOther = document.getElementById("dropdownContentShow");
    var dropdownActual = document.getElementById("dropdownContentOrderBy");
    if (dropdownActual.style.display === "block") {
        dropdownActual.style.display = "none";
    } else {
        if (dropdownOther.style.display == "block") {
            dropdownOther.style.display = "none";
        }
        dropdownActual.style.display = "block";
    }
}

function combineAndSendForms(action) {
    var showFormData = new FormData(document.getElementById('showForm'));
    var orderByFormData = new FormData(document.getElementById('orderByForm'));

    for (var pair of orderByFormData.entries()) {
        showFormData.append(pair[0], pair[1]);
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