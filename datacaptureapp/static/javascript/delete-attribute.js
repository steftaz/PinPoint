function delete_attribute(id) {
    let elem = document.getElementById("remove_attribute");
    elem.value = id;
    elem.form.submit();
}