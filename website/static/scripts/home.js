var imgContainer = document.querySelectorAll('imgContainer');


const title = document.getElementById('imgTitle');
const cover = document.getElementById('galleryImg');
const contentList = document.getElementById('contentList');


let clicked = null;
var files = [];

async function get_files(){
   removeAllChildNodes(contentList);
   await fetch("images", {
      headers: {
        "Content-Type": "application/json",
      },
    method: "get",
  }).then(response=>{
      console.log(response)
      return response.json();
  }).then(data =>{
      console.log(data.images)
      data.images.forEach(x => {
         files.push(x); 
      })
  }).catch(err => console.log(err));
  createImageDiv();
}


async function createImageDiv(){
 counter = 0;
 await files.forEach(x=>{
   var li = document.createElement('li');
   var imgCont = document.createElement('div');
   var divImg = document.createElement('div');
   var divTitle = document.createElement('div');
   var img = document.createElement("img");

   imgCont.classList.add("imgContainer");
   divImg.setAttribute("id", "cover-div");
   divImg.classList.add("d-flex", "justify-content-center", "align-items-center", "p-2");
   divTitle.classList.add("imgTitle","d-flex", "justify-content-center", "align-items-center", "p-2");
   divTitle.setAttribute("id", "imgTitle-"+counter);
   img.classList.add("galleryImg");

   contentList.appendChild(li);
   li.appendChild(imgCont);
   imgCont.appendChild(divImg);
   divImg.appendChild(img);
   imgCont.appendChild(divTitle);
   
   str = x.split(".")
   divTitle.innerText = str[0];
   img.src = `static/uploads/${x}`;

   counter++;
})
}

function removeAllChildNodes(parent) {
  while (parent.firstChild) {
      parent.removeChild(parent.firstChild);
  }
}
// filter search
function filter(){
 var input, filter, ul, li, a, i, txtValue;
 input = document.getElementById('searchInput');
 filter = input.value.toUpperCase();
 ul = contentList;
 li = ul.getElementsByTagName('li');

 for (i = 0; i < li.length; i++) {
  imgTitle = li[i].querySelectorAll(".imgTitle")[0];
  txtValue = imgTitle.textContent || imgTitle.innerText;
  if (txtValue.toUpperCase().indexOf(filter) > -1) {
    li[i].style.display = "";
  } else {
    li[i].style.display = "none";
  }
}
}

get_files();