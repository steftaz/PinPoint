function remove_member(member_id) {
    $.ajax({
        url: url_remove_member,
        type: 'POST',
        headers: {'X-CSRFToken': csrf},
        data: {'action': 'remove_member', 'member-id': member_id},
        success: function (response) {
            $('.modal').modal('hide')
            $('#div_messages').append("<div class='alert alert-success' role='alert'>" + response.messages[0]['message'] + "</div>");
            $('#team-members tr').each(function () {
                $(this).find('#email').each(function () {
                    if ($(this).html() == response.removed_user) {
                        $(this).parent().remove()
                    }
                })
            })
        }


    })
};