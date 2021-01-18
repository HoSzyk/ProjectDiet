const product_name = document.getElementById('product_name');
const calorie_100g = document.getElementById('calorie_100g');
const calorie_250g = document.getElementById('calorie_250g');
const fat_100g = document.getElementById('fat_100g');
const fat_250g = document.getElementById('fat_250g');
const carbohydrate_100g = document.getElementById('carbohydrate_100g');
const carbohydrate_250g = document.getElementById('carbohydrate_250g');
const protein_100g = document.getElementById('protein_100g');
const protein_250g = document.getElementById('protein_250g');
const select_product = document.getElementById('select_product');

function changeSelected(data) {
    let product = data[get_option() - 1];
    product_name.textContent = product.name;
    calorie_100g.textContent = product.calorie.toString() + "kcal";
    calorie_250g.textContent = (product.calorie * 2.5).toString() + "kcal";
    fat_100g.textContent = product.fat.toString() + "g";
    fat_250g.textContent = (product.fat * 2.5).toString() + "g";
    carbohydrate_100g.textContent = product.carbohydrate.toString() + "g";
    carbohydrate_250g.textContent = (product.carbohydrate * 2.5).toString() + "g";
    protein_100g.textContent = product.protein.toString() + "g";
    protein_250g.textContent = (product.protein * 2.5).toString() + "g";
}

function get_option() {
    return select_product.value
}
