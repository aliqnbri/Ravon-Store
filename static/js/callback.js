const base_url = `http://localhost:80`
document.addEventListener("DOMContentLoaded", () => {
    
    axios.get(`${base_url}/zarinpal/verify/`).then(response => {
        console.log(response);
        if (response.data.status == true) {
            setTimeout(() => {
                window.location.href = '/orders/conformation'
                
            }, 10000);
            
        }
        else{
            window.location.href = '/'
        }
    })
   
  });