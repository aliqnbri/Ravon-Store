const base_url = `http://localhost:80`
const order_url = `${base_url}/orders/api/order/`


async function makeGetRequest(path) {
    const response = await axios.get(path)
    return response.data
    
};


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
    return "";};


document.addEventListener('DOMContentLoaded', function (){

    ordersTable()

});

const ordersTable = async () =>{
    
    orders = await makeGetRequest(order_url);
    let content = ``;
    orders.forEach(order => {
        let itemsHtml = "";
        order.items.forEach(item => {
            itemsHtml += `<div>${item.product.name} - Quantity: ${item.quantity} - Price: ${item.price}</div>`;
        });
    
        content += `
            <tr>
                <th><span>${order.id}</span></th>
                <th>${itemsHtml}</th>
                <th><span>${order.country}, ${order.city}, ${order.address}</span></th>
                <th>${order.status}</th>
            </tr>`;
    });
    // orders.forEach(order => {
    //     content += `
    //     <tr>
    //     <th><span>${order.id}</span></th>
    //     <th>${order.items.forEach(item => {
    //         item
    //     })}</th>
    //     <th> <span>${order.country} , ${order.city} , ${order.address}</span></th>
    //     <th>${order.status}</th>
    //     </tr>
    //     `
        
    // });
    const tableBody = document.getElementById('tablebody');
    tableBody.innerHTML = content

}