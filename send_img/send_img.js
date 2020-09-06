const url = 'http://127.0.0.1:4040';

const canv = document.getElementById('canv');
const ctx = canv.getContext('2d');

const img1 = document.getElementById('img1');
const img2 = document.getElementById('img2');
const img3 = document.getElementById('img3');
const img4 = document.getElementById('img4');
const img5 = document.getElementById('img5');
var imgs = [img1,img2,img3,img4,img5];

ctx.font = '20px monospace'; ctx.fillStyle = '#5F6367';
ctx.fillText('Test', 20, 130);

show_img();
get_img();

function waitFPS(frames_per_second) {
  return new Promise(resolve => {
    setTimeout(() => {
      resolve(frames_per_second);
    }, 1000/frames_per_second);
  });
  //setTimeout(() =>{return 0;}, 1000/frames_per_second);
}

async function show_img() {
  let i = 0;
  while (true) {
    if (i > 4){i = 0;}

    var x = await waitFPS(5);
    //post_img(imgs[i]);
    ctx.drawImage(imgs[i], 0,0, canv.width, canv.height );

    i++
  }
}

function post_img(img){
  var xhr = new XMLHttpRequest();
  xhr.open('POST', url + '/img', true);
  xhr.setRequestHeader('Content-Type', 'application/json');
  //xhr.onreadystatechange = function () {
  //    if (xhr.readyState === 4 && xhr.status === 200) {
  //        var json = JSON.parse(xhr.responseText);
  //        console.log(json.email + ", " + json.password);
  //    }
  //};
  var data = JSON.stringify({'img': img, 'size': img.size});
  xhr.send(data);
}

function get_img(){
  var xhr = new XMLHttpRequest();
  xhr.open('GET', url + '/img', true);

  xhr.onload = function () {
    // Request finished. Do processing here.
    print(xhr.responseText);
  };

  xhr.send(null);
  // xhr.send('string');
  // xhr.send(new Blob());
  // xhr.send(new Int8Array());
  // xhr.send(document);
}
