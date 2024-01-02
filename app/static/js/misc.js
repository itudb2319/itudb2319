function toggleDropdownButton(actual, other1) {
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


document.addEventListener('DOMContentLoaded', function () {
    const xDiv = document.getElementById('layoutDropdownContent');
    const hoverElement = document.getElementById('layoutOthers');

    hoverElement.addEventListener('mouseover', function (e) {
        const dims = hoverElement.getBoundingClientRect();
        xDiv.style.left = dims.left + 'px';
        xDiv.style.top = dims.bottom + 'px';
        xDiv.style.display = 'flex';

    });

    hoverElement.addEventListener('mouseout', function (e) {
        xDiv.style.display = 'none';
        xDiv.addEventListener('mouseover', function (e) {
            xDiv.style.display = 'flex';
            xDiv.addEventListener('mouseout', function (e) {
                xDiv.style.display = 'none';
            });
        });
    });
});

document.addEventListener('DOMContentLoaded', function () {
    const h1Element = document.querySelector('h1');
    document.getElementById(h1Element.id).classList.add('active');
});

document.addEventListener("DOMContentLoaded", function () {
    var rows = document.querySelectorAll(".clickableRow");
    rows.forEach(function (row) {
        row.addEventListener("click", function () {
            var href = row.getAttribute('data-href');
            if (href) {
                window.location = href;
            }
        });
    });
});

document.addEventListener("DOMContentLoaded", function() {
    const tableElement = document.querySelector('table');
    var adminItems = tableElement.querySelectorAll(".admin");
    if (tableElement.id === "1") {
        adminItems.forEach(function(item) {
            item.style.display = "revert";
        });
    } else {
        adminItems.forEach(function(item) {
            item.style.display = "none";
        });     
    }
});

document.addEventListener("DOMContentLoaded", function() {
    var button = document.getElementById("createButton");
    button.addEventListener("click", function() {
        var element = document.getElementById("createArea")
        if (element.style.display == "revert") {
            element.style.display = "none";
        } else {
            element.style.display = "revert";
        }
    });
});


function changeVisibility(button){
    var element = document.getElementById("insertForm");

    if (element.style.visibility == "visible") {
        button.innerText = "Update Informations"
        element.style.visibility = "hidden";
    }
    else {
        button.innerText = "Hide"
        element.style.visibility = "visible";
    }
}