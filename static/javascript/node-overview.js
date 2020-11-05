function set_data_type(type) {
    let elem = document.getElementById("data_type");
    elem.value = type;
    elem.form.submit();
}

function remove_node(id) {
    let elem = document.getElementById("remove_node");
    elem.value = id;
    elem.form.submit();
}