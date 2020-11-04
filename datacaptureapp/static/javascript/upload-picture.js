$('#id_picture').attr({'hidden': 'hidden'});
const pictureInput = document.getElementById("id_picture");
const pictureButton = document.getElementById("picture-button");
const chosenFile = document.getElementById("chosen-file");

pictureButton.addEventListener("click", function () {
    pictureInput.click();
});

pictureInput.addEventListener("change", function () {
    if (pictureInput.value) {
        chosenFile.innerHTML = pictureInput.value.match(/[\/\\]([\w\d\s\.\-\(\)]+)$/)[1];
    } else {
        chosenFile.innerHTML = "No picture chosen";
    }
});