const verify_url = 'http://localhost:80/accounts/login-OTP/'


function verify() {
    // Simulated login request, replace with your actual login API call
    const otp = document.getElementById("otp").value;
    
    console.log(otp);
    // Make a POST request to your backend to authenticate user and obtain JWT token
    axios.post(verify_url, { "otp":otp })
    .then(response => {
        console.log(response);
        if(response.status = 200) {window.location.href = "/"}
       
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}