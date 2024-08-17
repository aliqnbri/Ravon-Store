// console.log("from js");
// Async function to make a POST request
import { makePostRequest } from './post.js'
const base_url = `http://localhost:8000`
const registrationEndpoint = `${base_url}/account/register/`;

  // Form submission event listener
  document.getElementById("signupform").addEventListener('submit', async function (event) {
    event.preventDefault(); // Prevent default form submission
  
    // Extract data from form fields using destructuring
    const { first_name, last_name, phone_number, email, password, password2 } = {
  
      first_name: document.getElementById('first_name').value,
      last_name: document.getElementById('last_name').value,
      phone_number: document.getElementById('phone_number').value,
      email: document.getElementById('email').value,
      password: document.getElementById('password').value,
      password2: document.getElementById('password2').value,
    };
  
    // Validate if passwords match
    if (password !== password2) {
      alert("Passwords do not match");
      return;
    }
  
    // Prepare data for API call
    const requestData = {
      first_name: first_name,
      last_name: last_name,
      phone_number: phone_number,
      email: email,
      password: password,
      password2: password2
    };
  
    // API endpoint for registration
    // const registrationEndpoint = 'http://localhost:8000/account/register/';
  
    try {
      // Use async/await instead of .then() for better readability
      const response = await axios.post(registrationEndpoint, requestData);
      console.log('Registration successful:', response);
      alert('Registration successful!');
      if (response.status === 201) {
        window.location.href = "/account/verify-otp/";
      }
    } catch (error) {
      console.error('Registration failed:', error.message);
      alert('Registration failed. Please try again later.');
    }
  });



