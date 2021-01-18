const diet_name = document.getElementById('diet_name');
const limit_calorie = document.getElementById('limit_calorie');
const limit_fat = document.getElementById('limit_fat');
const limit_carbohydrate = document.getElementById('limit_carbohydrate');
const limit_protein = document.getElementById('limit_protein');
const select_diet = document.getElementById('select_diet');
const button_submit = document.getElementById('button_submit');


function changeSelected(data) {
    let diet = data[get_option() - 1];
    diet_name.textContent = diet.name;
    limit_calorie.textContent = diet.calorie.toString() + "kcal";
    limit_fat.textContent = diet.fat.toString() + "g";
    limit_carbohydrate.textContent = diet.carbohydrate.toString() + "g";
    limit_protein.textContent = diet.protein.toString() + "g";
    button_submit.value = diet.id;
}

function get_option() {
    return select_diet.value
}
