const base_url = `http://localhost:80`
const logout_url = `${base_url}/accounts/logout/`
// addEventListener.
function logout() {
    axios.post(logout_url,'',{
        headers: {
          'Content-Type': 'text/html; charset=utf-8'
        }
      })
    .then(response => {
      console.log(response);
        // console.log(document.cookie);
        if(response.status = 200) {window.location.href = "/"}
        // Store the JWT token in localStorage or sessionStorage
        // localStorage.setItem('token', response.data.access);
        // localStorage.setItem('token', response.data.refresh);
        // console.log("Login successful. Token:", response.data.access);
        
    })
    .catch(error => {
        console.error('Error:', error);
    });
}