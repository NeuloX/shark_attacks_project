
function shark_facts(){
var shark = document.getElementById('shark_type').textContent;
console.log(shark);
if (shark != ""){
  for (var x in shark_deets.Shark_Details){
    //console.log(shark_deets.Shark_Details[x].species)
    if (shark_deets.Shark_Details[x].species.includes(shark)){
      shark_sci = shark_deets.Shark_Details[x].scientific_name;
      shark_det = shark_deets.Shark_Details[x].details;
      shark_img = shark_deets.Shark_Details[x].img_url;
      shark_diet = shark_deets.Shark_Details[x].diet;
      document.getElementById('shark_type').innerHTML = "The " + shark;
      document.getElementById('shark_sci').innerHTML = "("+shark_sci+")";
      document.getElementById('shark_deets').innerHTML = shark_det;
      document.getElementById('shark_url').src = shark_img;
      document.getElementById('shark_hunth3').innerHTML = "Diet";
      document.getElementById('shark_diet').innerHTML = shark_diet;
      console.log(shark_img);
    }
  
  }
}
}
