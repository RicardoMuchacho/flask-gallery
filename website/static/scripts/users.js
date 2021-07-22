var editBtn = document.getElementById("editBtn");
var confirmBtn = document.getElementById("confirmBtn");
var deleteBtn = document.getElementById("deleteBtn");
var cancelBtn = document.getElementById("cancelBtn");
var nameInput = document.getElementById("name");
var emailInput = document.getElementById("email");
var passInput = document.getElementById("pass");
var userInput = document.getElementById("userid");
var div = document.getElementById("cont1");
var error = document.getElementById("error");

fetch("userinfo", {
    headers: {
        "Content-Type": "application/json",
    },
    method: "get",
}).then(data=>{
    console.log(data);
    return data.json();
}).then(r =>{
    console.log(r);
    nameInput.value = r.name;
    emailInput.value = r.email;
    passInput.value = r.password;
    userInput.value = r.id;
    //result.textContent=r.result;
}).catch(err => console.log(err));

function edit(){
	editBtn.disabled = true;
    confirmBtn.disabled = false;
    cancelBtn.disabled = false;
    deleteBtn.disabled = false;
    nameInput.disabled = false;
    emailInput.disabled = false;
    passInput.disabled = false;
 }

function deleteUser(){
    fetch("users", {
        method: "delete",
    }).then(response=>{
        if (response.redirected == true)
        {
          window.location.replace(response.url)
        }
        console.log(response);
     }).catch(err => console.log(err));
}

function confirm(){
	newName = nameInput.value;
	newEmail = emailInput.value;
	newPass = passInput.value;
	
    fetch('users',{
        method: 'PUT',
        headers: new Headers({
      // Encabezados
     'Content-Type': 'application/json'
      }),
        body: JSON.stringify(
      {
      "name": newName,
      "email": newEmail,
      "pass": newPass,
      })
      
    }).then(response=>{
      console.log(response);
      return response.json()
    }).then(r =>{
      if (r.error){
        error.textContent=r.error;
      }
      console.log(r);
      error.textContent=r.message;
  }).catch(e => console.log(e))
		
	//var p = document.createElement("p");
	//cont1.appendChild(p);
	//p.innerHTML = "Succesfully updated";
}

function cancel(){
	editBtn.disabled = false;
    confirmBtn.disabled = true;
    cancelBtn.disabled = true;
    deleteBtn.disabled = true;
    nameInput.disabled = true;
    emailInput.disabled = true;
    passInput.disabled = true;
}

