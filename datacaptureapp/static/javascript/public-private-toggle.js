ppToggle = $("#public-private-toggle");
toggleLabel = $("#toggle-label");
ppToggle.on('change', function () {
    if (ppToggle.is(':checked')) {
        console.log("if");
        toggleLabel.html("<b>Public</b> project");

    } else {
        console.log("else");
        toggleLabel.html("<b>Private</b> project");
    }
});