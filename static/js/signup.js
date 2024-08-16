// console.log("from js");
// Async function to make a POST request
const base_url = `http://localhost:80`
// API endpoint for registration
const registrationEndpoint = `${base_url}/accounts/users/`;
async function makePostRequest(path, requestData) {
    try {
        const response = await axios.post(path, requestData);
        return response.data;
    } catch (error) {
        console.error('Error occurred:', error);
        throw new Error('Error occurred while making POST request');
    }
}

// Form submission event listener
document.getElementById("signupform").addEventListener('submit', async function(event) {
    event.preventDefault(); // Prevent default form submission

    // Extract data from form fields
    var username = document.getElementById('username').value;
    var firstname = document.getElementById('firstname').value;
    var lastname = document.getElementById('lastname').value;
    var phone = document.getElementById('phone').value;
    var email = document.getElementById('email').value;
    var password = document.getElementById('password').value;
    var password2 = document.getElementById('password2').value;

    // Validate if passwords match
    if (password !== password2) {
        alert("Passwords do not match");
        return;
    }

    // Prepare data for API call
    var requestData = {
        username : username,
        first_name : firstname,
        last_name : lastname,
        phone: phone,
        email: email,
        password: password
    };

    

    axios.post(registrationEndpoint, requestData)
    .then(response => {
        console.log('Registration successful:', response);
        alert('Registration successful!');
        if(response.status = 201) {window.location.href = "/accounts/login/"} 
        
    })
    .catch(error => {
        console.error('Registration failed:', error.message);
        alert('Registration failed. Please try again later.');
    });
});