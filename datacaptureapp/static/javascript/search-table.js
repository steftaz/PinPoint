$(document).ready(function () {
    $("#search-table").on("keyup", function () {
        let input = $(this).val();
        $("#data-nodes tr").filter(function () {
            if ($(this).parent().is("tbody")) {
                $(this).toggle($(this).text().indexOf(input) > -1)
            }

        });
    });

});