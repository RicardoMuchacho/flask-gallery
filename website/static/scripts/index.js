const username =  document.getElementById("name");
const pass = document.getElementById("pass");
const error = document.getElementById("error");

function login(){
  fetch('login',{
      method: 'POST',
      headers: new Headers({
    // Encabezados
   'Content-Type': 'application/json'
    }),
      body: JSON.stringify(
    {
    "name": username.value,
    "pass": pass.value,
    })
    
  }).then(response=>{
    console.log(response);
    if (response.redirected == true)
    {
      window.location.replace(response.url)
    }
    return response.json()
  }).then(r =>{
    console.log(r);
    error.textContent=r;
}).catch(e => console.log(e))
}