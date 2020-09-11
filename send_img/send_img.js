//url of a our API
//const url = 'http://speedest.herokuapp.com';
const url = 'http://0.0.0.0:5000/';
//image element I've put on our view that will later display our result
const canv = document.getElementById('test_canvas');
const ctx = canv.getContext("2d");
//a timer that will help us measure apps performance
var timer; var mlsec = 0;

//function that gets triggered once the user decides to upload an image
function show_img(upload) {
  //timer starts
  timer = setInterval(()=> mlsec++, 1);
  //getting this img as a file
  let img_file = upload.files[0];
  //converting it to a bytes array with base64 encoding
  to_base64(img_file);
}

//function that converts our img file to base64 bytes
async function to_base64(img_file) {
    //FileReader that will help us convert our image file
    var reader = new FileReader();

    //function that will be triggered once the conversion is done
    reader.onloadend = function() {
      //removing the header from byte image as the server don't accept them and it shortens the json a bit
      //PS this is not ideal since images might be JPEG
      var b64_img = reader.result.replace("data:image/jpeg;base64,", "");
      //displaing how much time it took
      console.log("converting to base64 took: " + mlsec); mlsec = 0;
      //sending the result to the server
      post_img(b64_img);
    }
    //converting our img file
    reader.readAsDataURL(img_file);
}

//function that posts converted images to the server, gets the result and display it in the view
function post_img(b64_img){
  //creating an AJAX request
  var xhr = new XMLHttpRequest();
  xhr.open('POST', url + '/img', true);
  xhr.setRequestHeader('Content-Type', 'application/json');

  //function that will be triggered once the request will be filled
  xhr.onreadystatechange = function () {
      if (xhr.readyState === 4 && xhr.status === 201) {
        //displaing how much time it took
        console.log("sending request took: " + mlsec); mlsec = 0; clearInterval(timer);

        console.log(xhr.responseText);

        let vehicles = JSON.parse(xhr.responseText).vehicles

        //displaying an img that was received and sent back by the server
        //again, not ideal, might not be JPEG
        var image = new Image();
        image.onload = function() {
          ctx.drawImage(image, 0, 0, canv.width, canv.height);

          for (let i = 0 ; i < vehicles.length; i++){
            let vehicle = vehicles[i];
            ctx.beginPath();
            ctx.lineWidth = "3";
            ctx.strokeStyle = "red";
            ctx.rect(vehicle[0], vehicle[1], vehicle[2], vehicle[3]);
            ctx.stroke();
          }
        };
        image.src = "data:image/jpeg;base64," + b64_img;
      }
  };
  //serializing our img data
  var data = JSON.stringify({'img': b64_img, 'size': "12,12"});
  //sending request
  xhr.send(data);
}
