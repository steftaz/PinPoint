//Searches through table rows based on user input

$(document).ready(function () {
    $("#search-table").on("keyup", function () {
        let input = $(this).val();
        $("#table tr").filter(function () {
            if ($(this).parent().is("tbody")) {
                $(this).toggle($(this).text().indexOf(input) > -1)
            }

        });
    });

});