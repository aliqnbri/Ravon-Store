const base_url = `http://127.0.0.1:8000`
const product_url = `${base_url}/products/api/product/`
const cart_url = `${base_url}/cart/api/cart/`

  
async function makeGetRequest(path) {
    const response = await axios.get(path)
    return response.data
    
};

async function makePostRequest(path, requestData) {
    const response = await axios.post(path, requestData);
    return response.data;
};

const createProductCard = async () => {
    // Get the current pathname from the URL
    const pathname = window.location.pathname;

    // Split the pathname into parts using '/' as the delimiter
    const parts = pathname.split('/');

    // Get the last part of the pathname, which should be the value "2"
    const productId = parts[parts.length - 1];
    console.log(productId);
    console.log(product_url);
    const product = await makeGetRequest(`${product_url}${productId}`);
    console.log(product);
    
    // const images = product.images.map(image => `<div class="single_product_img"><img src="${image}" alt="#" class="img-fluid"></div>`).join('');
    let content = 
            `
                <div class="row justify-content-center">
                    <div class="col-lg-6">
                        <div  >
                            
                            <img src=${product.images}  class="img-fluid">
                        
                        </div>
                    </div>
                    <div class="col-lg-8">
                        <div class="single_product_text text-center">
                            <h3>${product.name}</h3>
                            <h5>${product.brand.name}</h5>
                            <p>${product.description}</p>
                            <div class="card_area">
                                <div class="product_count_area">
                                    <p>Quantity</p>
                                    <div class="product_count">
                                        <i class="ti-minus" onclick ="minus()"></i>
                                        <input id="quantity" class="input-number justify-content-center" type="text" value="1" min="0" max="100">
                                         <i class="ti-plus" onclick="plus()"></i>
                                    </div>
                                    <p>$${product.price}</p>
                                </div>
                                <div class="add_to_cart">
                                    <a onclick ="addToCart()"class="btn_3">add to cart</a>
                                </div>
                            </div>
                        </div>
                    </div>
                </div>
            `;
   
    const productContainer = document.getElementById('detail');
    productContainer.innerHTML = content;
};

document.addEventListener('DOMContentLoaded', function (){

    createProductCard()

});


async function plus() {
    const quantity = document.getElementById('quantity')
    const count = parseInt(quantity.value) +1
    quantity.value = count
}

async function minus() {
    const quantity = document.getElementById('quantity')
    const count = parseInt(quantity.value) - 1
    quantity.value = count
}


async function addToCart() {
    // Get the current pathname from the URL
    const pathname = window.location.pathname;

    // Split the pathname into parts using '/' as the delimiter
    const parts = pathname.split('/');

    // Get the last part of the pathname, which should be the value "2"
    const productId = parts[parts.length - 1];
    
    const product = await makeGetRequest(`${product_url}${productId}`);
    // const quantity = document.getElementById(quantity);
    // Get the quantity input element from the HTML
    const quantityInput = document.getElementById('quantity');
    
    // Extract the quantity value from the input element
    const quantity = parseInt(quantityInput.value);
    const postData = {
        "product": {
            "id": product.id,
            "name": product.name,
            "price": product.price,
            "images": product.images,
            "description": product.description,
            "discount": product.discount,
            "brand": product.brand,
            "url": product.url
        },
        "quantity": quantity
    };

    const responseData = await makePostRequest(cart_url, postData);
    getCount()
}




