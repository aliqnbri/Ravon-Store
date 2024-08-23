const base_url = `http://127.0.0.1:8000`
const order_url = `${base_url}/orders/api/order/`
const filter = `?payment_id=${getCookie('order')}`;
// console.log(filter);
async function makeGetRequest(path,prams) {
    const response = await axios.get(path)
    return response.data 
}


function getCookie(cname) {
    let name = cname + "=";
    let decodedCookie = decodeURIComponent(document.cookie);
    let ca = decodedCookie.split(';');
    for(let i = 0; i <ca.length; i++) {
      let c = ca[i];
      while (c.charAt(0) == ' ') {
        c = c.substring(1);
      }
      if (c.indexOf(name) == 0) {
        return c.substring(name.length, c.length);
      }
    }
    return "";
  }

document.addEventListener("DOMContentLoaded", function(){
    if (getCookie('order') != "") {
        
        createOrder()
    }


})

const createOrder = async()=>{

    const order = await makeGetRequest(`${order_url}${filter}`);
    console.log(order);
    const orderId = document.getElementById('order_id');
    orderId.innerHTML = `: ${order[0].id}`;
    const date = document.getElementById('date')
    date.innerHTML = `: ${order[0].created_at}`;
    const total = document.getElementById('total')
    total.innerHTML = `: USD ${order[0].get_total_cost}`;
    const status = document.getElementById('status')
    status.innerHTML = `: ${order[0].status}`;
    const address = document.getElementById('address')
    address.innerHTML = `: ${order[0].address}`;
    const city = document.getElementById('city')
    city.innerHTML = `: ${order[0].city}`;
    const country = document.getElementById('country')
    country.innerHTML = `: ${order[0].country}`;
    const postal_code = document.getElementById('postal_code')
    postal_code.innerHTML = `: ${order[0].postal_code}`;

    let content = ``;
    order[0].items.forEach(item => {
        content +=  `
        <tr>
        <th colspan="2"><span>${item.product.name}</span></th>
        <th>x ${item.quantity}</th>
        <th> <span>$${item.price}</span></th>
        </tr>
      `
    });
    
    const tableBody = document.getElementById('tablebody')
    tableBody.innerHTML = content;

    const quantity = document.getElementById('quantity')
    quantity.innerHTML = `X ${order[0].__len__}`;
    const totalv = document.getElementById('totalv')
    totalv.innerHTML = `$${order[0].get_total_cost}`;




   

}