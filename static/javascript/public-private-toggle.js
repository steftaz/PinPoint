ppToggle = $("#public-private-toggle");
toggleLabel = $("#toggle-label");
ppToggle.on('change', function () {
    if (ppToggle.is(':checked')) {
        toggleLabel.html("<b>Public</b> project");

    } else {
        toggleLabel.html("<b>Private</b> project");
    }
});