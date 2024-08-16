const base_url = `http://localhost:80`
const categories_url = `${base_url}/products/api/category/`
const product_url = `${base_url}/products/api/product/`
const cart_url = `${base_url}/cart/api/`

async function makeGetRequest(path,prams) {
    const response = await axios.get(path)
    return response.data 
}

async function makePostRequest(path, requestData) {
    const response = await axios.post(path, requestData);
    return response.data;
}

const createProductCard = async (category, searchTerm = '') => {
    let params = '';
    if (searchTerm) {
        params = `?search=${searchTerm}`;
    } else if (category) {
        params = `?category_slug=${category.toLowerCase()}`;
    }
    const productlist = await makeGetRequest(`${product_url}${params}`);
    let content = ``;
    
    productlist.forEach(product => {
        content += `
            <div class="col-xl-4 col-lg-4 col-md-6 col-sm-6">
                <div class="single-popular-items mb-50 text-center">
                    <div class="popular-img">
                        <img src=${product.images} alt="">
                        <div class="img-cap">
                            <span onclick="addToCart(${product.id})">Add to cart</span>
                        </div>
                        <div class="favorit-items">
                            <span class="flaticon-heart"></span>
                        </div>
                    </div>
                    <div class="popular-caption">
                        <h3><a href=${product.url}>${product.name}</a></h3>
                        <span>${product.brand.name}</span>
                        <span>$ ${product.price}</span>
                    </div>
                </div>
            </div>
        `;
    });
    // Update the HTML element where you want to display the products
    const productContainer = document.getElementById('productContainer');
    productContainer.innerHTML = content;
};

// Example usage when clicking on a category link
navtab.addEventListener('click', (event) => {
    if (event.target.classList.contains('nav-link')) {
        const selectedCategory = event.target.innerText.trim();
        createProductCard(selectedCategory.toLowerCase());
    }
});

// Initial load with all products

const getCategoryList = async()=>{
    const categoryList =await makeGetRequest(categories_url);
    let content = ``;
    categoryList.forEach(category => {
        content += `
        <a class="nav-item nav-link " id="nav-home-tab" data-toggle="tab" href="#nav-home" role="tab" aria-controls="nav-home" aria-selected="true">${category.name}</a>    
        `;
        
    });
    navtab.innerHTML = content;
};


document.addEventListener("DOMContentLoaded", function() {
    const searchInput = document.getElementById("searchInput");
    const searchIcon = document.getElementById("searchIcon");

    function callApi(searchTerm) {
        createProductCard('', searchTerm);
    }

    searchIcon.addEventListener("click", function() {
        const searchTerm = searchInput.value.trim();
        callApi(searchTerm);
    });

    searchInput.addEventListener("keypress", function(event) {
        if (event.key === "Enter") {
            const searchTerm = searchInput.value.trim();
            callApi(searchTerm);
        }
    });
});



getCategoryList();
createProductCard(null);


async function addToCart(productId) {
    // Get the current pathname from the URL
    const product = await makeGetRequest(`${product_url}${productId}`);
    console.log(product)
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
        "quantity": 1
    };

    const responseData = await makePostRequest(cart_url, postData);
    getCount()
}