console.log("AI Resume Screening System loaded");


document.addEventListener("DOMContentLoaded", function () {

    const uploadButton = document.querySelector(".upload-btn");

    if (uploadButton) {

        uploadButton.addEventListener("click", function () {

            console.log("Opening resume upload page");

        });

    }


    const tableRows = document.querySelectorAll(".resume-table tbody tr");

    tableRows.forEach(function (row) {

        row.addEventListener("click", function () {

            tableRows.forEach(function (item) {
                item.style.backgroundColor = "";
            });

            row.style.backgroundColor = "#fafaff";

        });

    });

});