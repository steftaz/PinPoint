// When someone tries to add a member (submit the form)
$("#addMember").submit(function (e) {

    e.preventDefault(); // avoid to execute the actual submit of the form.

    var form = $(this);
    var url = $(this).attr('data-url');

    $.ajax({
        type: "POST",
        url: url,
        data: form.serialize(), // serializes the form's elements.
        success: function (data) {
            success = data.success;
            update_messages(data.messages);
            if (data.email && data.username) {
                update_member_table(data.email, data.username, data.member_id)
            }
        }
    });


});

function update_messages(messages) {
    $("#div_messages").html("");
    $.each(messages, function (i, m) {
        switch (m.extra_tags) {
            case 'success':
                $("#div_messages").append("<div class='alert alert-success' role='alert'>" + m.message + "</div>");
                break;
            case 'error':
                $("#div_messages").append("<div class='alert alert-danger' role='alert'>" + m.message + "</div>");

        }

    });
}

function update_member_table(email, username, id) {
    $("#team-members tbody").append(
        '<tr><td>' + email + '</td><td>' + username + '</td>' +
        '<td style="border:none;"><a id="remove-member" data-toggle="modal" data-target="#remove' + id + '" class="close"' +
        'aria-label="Close" style=" color: red; opacity: 1;" type="button">' +
        '<span aria-hidden="true">&times;</span>' +
        '</a></td>' +
        '</tr>' +
        '<div class="modal fade" id="remove' + id + '" tabindex="-1" role="dialog"' +
        'aria-labelledby="removeMember' + id + '" aria-hidden="true">' +
        '<div class="modal-dialog" role="document">' +
        '<div class="modal-content">' +
        '<div class="modal-header">' +
        '<h5 class="modal-title" id="exampleModalLabel">Remove member</h5>' +
        '<button type="button" class="close" data-dismiss="modal" aria-label="Close">' +
        '<span aria-hidden="true">&times;</span>' +
        '</button>' +
        '</div>' +
        '<div class="modal-body">Are you sure you want to remove this member?</div>' +
        '<div class="modal-footer">' +
        '<a onclick="remove_member(' + id + ')" class="btn btn-danger" aria-label="Yes"' +
        'type="button">Yes</a>' +
        '<button type="button" class="btn btn-secondary" data-dismiss="modal">No</button>' +
        '</div>' +
        '</div>' +
        '</div>' +
        '</div>'
    )
}