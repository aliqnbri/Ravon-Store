const login_url = `http://localhost:80/accounts/login-OTP/`



function login() {
    // Simulated login request, replace with your actual login API call
    const username = document.getElementById("username").value;
    const password = document.getElementById("password").value;
    console.log("inside login");
    // Make a POST request to your backend to authenticate user and obtain JWT token
    axios.patch(login_url, { "username":username, "password":password })
    .then(response => {
        
        if(response.status = 200) {window.location.href = "/accounts/verifyotp"}
       
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}

// // Function to get data using the JWT token
// function getData() {
//     // Get the JWT token from localStorage or sessionStorage
//     const token = localStorage.getItem('token');

//     // Make a GET request to your protected API endpoint with the JWT token
//     axios.get('http://your-api.com/data/', {
//     headers: {
//         'Authorization': `Bearer ${token}`
//     }
//     })
//     .then(response => {
//     console.log("Data received:", response.data);
//     // Display the received data
//     alert(JSON.stringify(response.data));
//     })
//     .catch(error => {
//     console.error('Error:', error);
//     alert("Error occurred. Please log in first.");
//     });
// }
