
ppToggle = $("#public-private-toggle");
toggleLabel = $("#toggle-label");

if ($("#is-public").html() == 'True') {
    toggleLabel.html("Project is <b>public</b>")
    ppToggle.prop('checked', true);
} else {
    toggleLabel.html("Project is <b>private</b>");
}

//Changes project to public/private when clicked
ppToggle.on('change', function () {
        const url = $(this).attr('change-pp-url');
        const is_public = ppToggle.is(":checked") ? 'True' : 'False';
        $.ajax({
            type: 'POST',
            headers: {"X-CSRFToken": csrf},
            url: url,
            data: {'is_public': is_public},
            success: function (response) {
                if (response.is_public) {
                    toggleLabel.html("Project is <b>public</b>");
                } else {
                    toggleLabel.html("Project is <b>private</b>");
                }
            }

        })
    }
);