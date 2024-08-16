const base_url = `http://localhost:80`
const cart_url = `${base_url}/cart/api/`
const product_url = `${base_url}/products/api/product/`
async function makeGetRequest(path) {
    const response = await axios.get(path)
    return response.data
    
}

async function makePostRequest(path, requestData) {
    const response = await axios.post(path, requestData);
    return response.data;
}


const createCard = async () => {
    
    let content = ``;
    const cart = await makeGetRequest(`${cart_url}`);
    
    cart.data.forEach(item => {
        content += `
                        <tr>
                        <td>
                        <div class="media">
                            <div class="d-flex">
                            <img src=${item.product.images} alt="" />
                            </div>
                            <div class="media-body">
                            <p>${item.product.name}</p>
                            </div>
                        </div>
                        </td>
                        <td>
                        <h5>${item.product.price}</h5>
                        </td>
                        <td>
                        <div class="product_count">
                            <span class="input-number-decrement"> <i class="ti-minus"></i></span>
                            <input class="input-number" type="text" value=${item.quantity} min="0" max="100">
                            <span class="input-number-increment"> <i class="ti-plus"></i></span>
                        </div>
                        </td>
                        <td>
                        <h5>$${item.total_price}</h5>
                        </td>
                        <td>
                        <a class="btn_1" onclick="remove(${item.product.id})">remove</a>
                        </td>
                    </tr>
        `;
    });
    content += `
    
                <tr>
                    <td></td>
                    <td></td>
                    <td>
                    <h5>Subtotal</h5>
                    </td>
                    <td>
                    <h5>$${cart.cart_total_price}</h5>
                    </td>
                </tr>
    `;
    
    const tableBody = document.getElementById('tableBody');
    tableBody.innerHTML = content;
};

createCard();

const remove = async (productId) => {
    const product = await makeGetRequest(`${product_url}${productId}`);
    // Now you have the product information, you can proceed with the removal logic
    console.log("Removing product:", product);
    console.log(productId);
    const postData =
    {
        "product": product,
        "remove": true
      };
    const responseData = await makePostRequest(cart_url, postData);
    console.log(responseData);
    createCard(); // Output the response data received from the server
    // const response = makePostRequest(path, requestData)
};