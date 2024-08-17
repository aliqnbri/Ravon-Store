
import { makePostRequest } from './post.js'; // Assuming the makePostRequest function is in api.js file




// Add event listener to the verify button
verifyButton.addEventListener('click', async () => {
  try {
    // Extract OTP values from input fields
    const otp = Array.from(otpInputs).map((input) => input.value).join('');
    console.log(otp)

    // Use the makePostRequest function to send a POST request
    const response = await makePostRequest('http://localhost:80/account/verify-otp/', { otp });

    console.log(response);
  } catch (error) {
    console.error(error);
  }
});