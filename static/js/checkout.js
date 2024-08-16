const base_url = `http://localhost:80`
const cart_url = `${base_url}/cart/api/`
const order_url = `${base_url}/orders/api/order/`
const address_url = `${base_url}/customer/api/addresses/`
async function makeGetRequest(path) {
    const response = await axios.get(path)
    return response.data
    
}

async function makePostRequest(path, requestData) {
    const response = await axios.post(path, requestData);
    return response.data;
}


const createOrderCart = async () => {
    
    let content = ` <li>
                        <a href="#">Product
                        <span>Total</span>
                        </a>
                    </li>
                  `;
    const cart = await makeGetRequest(cart_url);
    const addresses = await makeGetRequest(address_url);
    // console.log(addresses);
    let addressContent = '';
    addresses.forEach(address => { 
        addressContent +=`

         <input class='adrs' type="radio" id="${address.id}" name="options" value="${address.id}">
                <label for="${address.id}">${address.name} : ${address.country} , ${address.state} , ${address.city} , ${address.address} </label><br>
        
        
        `
        
    });
    // console.log(addressContent);
    const addressForm = document.getElementById('addresses');
    addressForm.innerHTML = addressContent
    
    cart.data.forEach(item => {
        content += `
                    <li>
                        <a href=${item.product.url} %}>F${item.product.name}
                        <span class="middle">x ${item.quantity}</span>
                        <span class="last">$${item.total_price}</span>
                        </a>
                    </li>
                    
        `;
    });
    content += `
    
                    <li>
                        <a>Total
                        <span>$${cart.cart_total_price}</span>
                        </a>
                    </li>
    `;
    
    const ordercart = document.getElementById('ordercart');
    ordercart.innerHTML = content;
};

createOrderCart();

const createOrder = async() => {
    
    var requestData = {
        address : addressID
    };
    axios.post(order_url, requestData)
    .then(response => {
        // console.log('Order Created successful:', response);
        alert('Order Created successful');
        if(response.status = 201) {
            // console.log(response.data);
            axios.get(`${base_url}/zarinpal/request/${response.data.id}`,{headers:{'Content-Type' : 'application/json'}}).then(payment => {
                console.log(payment.data.url);
                window.location.href = `${payment.data.url}`
            })
        } 
        
    })
    .catch(error => {
        console.error('Registration failed:', error.message);
        alert('Registration failed. Please try again later.');
    });


}

var addressID = '';


document.addEventListener("DOMContentLoaded", () => {
    setTimeout(()=> {


    const radioButtons = document.querySelectorAll(".adrs");
    console.log(radioButtons);
    // Add change event listener to each radio button
    radioButtons.forEach(radioButton => {
      radioButton.addEventListener('change', () => {
        // Log the value of the selected radio button
        addressID = radioButton.value
        console.log('Selected option:', radioButton.value);
      });
    });},
    2000
    )
    
  });


const addNewAddress = async () => {
    const data = new FormData();
    data.append('name', document.getElementById('name').value);
    data.append('country', document.getElementById('country').value);
    data.append('state', document.getElementById('state').value);
    data.append('city', document.getElementById('city').value);
    data.append('address', document.getElementById('address').value);
    data.append('postal_code', document.getElementById('postal_code').value);




    
    response = await makePostRequest(address_url,data)
    console.log(response);
    createOrderCart()
    setTimeout(()=> {


        const radioButtons = document.querySelectorAll(".adrs");
        console.log(radioButtons);
        // Add change event listener to each radio button
        radioButtons.forEach(radioButton => {
          radioButton.addEventListener('change', () => {
            // Log the value of the selected radio button
            addressID = radioButton.value
            console.log('Selected option:', radioButton.value);
          });
        });},
        100
        )
}
// console.log(radioButton.value);

// const remove = async (productId) => {
//     const product = await makeGetRequest(`${product_url}${productId}`);
//     // Now you have the product information, you can proceed with the removal logic
//     console.log("Removing product:", product);
//     console.log(productId);
//     const postData =
//     {
//         "product": product,
//         "remove": true
//       };
//     const paymentData = await makePostRequest(cart_url, postData);
//     console.log(responseData);
//     createCard(); // Output the response data received from the server
//     // const response = makePostRequest(path, requestData)
// };