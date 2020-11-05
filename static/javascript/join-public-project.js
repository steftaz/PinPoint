function joinPublicProject() {
    $.ajax({
        type: "POST",
        url: url_project,
        headers: {"X-CSRFToken": csrf},
        data: '',
        success: function (response) {
            $("#div_messages").append("<div class='alert alert-success' role='alert'>" + response.messages[0]['message'] + "</div>");
            $("#join-public-project").hide()
        }

    });
}