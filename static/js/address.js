const base_url = `http://localhost:80`
const adderess_url = `${base_url}/customer/api/addresses/`


async function makeGetRequest(path) {
    const response = await axios.get(path)
    return response.data
    
};
async function makePostRequest(path, requestData) {
    const response = await axios.post(path, requestData);
    return response.data;
};

async function makeDeleteRequest(path) {
    const response = await axios.delete(path)
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

    addressesTable()

});

const addressesTable = async () =>{

    adresses = await makeGetRequest(adderess_url);
    let content = ``;
    adresses.forEach(address => {
    
        content += 
            `<tr>
            <th><span>${address.name}</span></th>
            <th>${address.country} </th>
            <th>${address.state}</th>
            <th>${address.city}</th>
            <th>${address.postal_code}</th>
            <th>${address.address}</th>
            <th><button class='btn  btn-sm' onclick ='deleteAddress(${address.id})'>Remove</button></th>

          </tr>`
    });

    const tableBody = document.getElementById('tablebody');
    tableBody.innerHTML = content

}

const deleteAddress = async (addressId) => {
    response = await makeDeleteRequest(`${adderess_url}${addressId}`)
    console.log(response);
    addressesTable();

}

const addNewAddress = async () => {
    const data = new FormData();
    data.append('name', document.getElementById('name').value);
    data.append('country', document.getElementById('country').value);
    data.append('state', document.getElementById('state').value);
    data.append('city', document.getElementById('city').value);
    data.append('address', document.getElementById('address').value);
    data.append('postal_code', document.getElementById('postal_code').value);




    
    response = await makePostRequest(adderess_url,data)
    console.log(response);
    addressesTable()
}
