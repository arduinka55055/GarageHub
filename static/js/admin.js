

function filter_car_models() {
    var manufacturer_id = document.querySelector('#id_manufacturer option:checked');
    var model_options = document.getElementById('id_model_car').options;
    for (var i = 0; i < model_options.length; i++) {
        var option = model_options[i];
        console.log(option.innerText, manufacturer_id.innerText, option.dataset.manufacturer);
        if (option.innerText.includes (manufacturer_id.innerText) || option.dataset.manufacturer === '') {
            option.style.display = '';
        } else {
            option.style.display = 'none';
        }
    }
}

document.addEventListener('DOMContentLoaded', function() {
    filter_car_models();
    document.getElementById('id_manufacturer').addEventListener('change', filter_car_models);
});