const userId = getCookie('username');
const base_url = `http://127.0.0.1:8000`
const user_url = `${base_url}/account/users/${userId}/`

async function makeGetRequest(path) {
    const response = await axios.get(path)
    return response.data
    
};
async function makePutRequest(path, requestData) {
    const response = await axios.patch(path, requestData);
    return response.data;
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
    return "";
  };


const profileData = async () => {
    const user = await makeGetRequest(user_url);
    console.log(user);
    document.getElementById('firstname').value = user.first_name;
    document.getElementById('lastname').value = user.last_name;
    document.getElementById('email').value = user.email;
    document.getElementById('phone').value = user.phone;
    document.getElementById('avatar').src = user.image;
};

const updateProfile = async () => {

    const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
    if (document.getElementById("avatar-file").files[0] == null){}
    const data = new FormData();
    data.append('first_name', document.getElementById('firstname').value);
    data.append('last_name', document.getElementById('lastname').value);
    data.append('email', document.getElementById('email').value);
    data.append('phone', document.getElementById('phone').value);
    const fileInput = document.getElementById('avatar-file');
    if (fileInput.files.length > 0) {
      data.append('image', fileInput.files[0]);
    }
    response = await makePutRequest(user_url,data)
  
};


document.addEventListener('DOMContentLoaded', function (){
  profileData();  
  });

//   function getCookie(name) {
//     const value = `; ${document.cookie}`;
//     const parts = value.split(`; ${name}=`);
//     if (parts.length === 2) return parts.pop().split(';').shift();
//   }
//     const user_id = getCookie('user_id');
//     console.log(user_id);
//     // Make an HTTP PUT Request 
//     async function put() { 
//       const url = `/core/users/${user_id}/`
//       const csrfToken = document.querySelector('[name=csrfmiddlewaretoken]').value;
      
//       if (document.getElementById("avatar-file").files[0] == null){}
//       const data = new FormData();
//     data.append('first_name', document.getElementById('firstname').value);
//     data.append('last_name', document.getElementById('lastname').value);
//     data.append('email', document.getElementById('email').value);
//     data.append('phone', document.getElementById('phone').value);
//     const fileInput = document.getElementById('avatar-file');
//     if (fileInput.files.length > 0) {
//       data.append('user_image', fileInput.files[0]);
//     }
     
//      const response = await fetch(url, { 
//        method: 'PUT', 
//        headers: { 
//          'X-CSRFToken': csrfToken,
//        }, 
//        body: data, 
//      }); 
       
//      // Awaiting response.json() 
//      const resData = await response.json(); 
//      console.log(resData);
//      // Return response data  
//      return resData; 
//    } 