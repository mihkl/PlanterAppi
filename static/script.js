console.log("loaded");

const fileInput = document.getElementById('file-input');
console.log(fileInput);

fileInput.addEventListener('change', (e) =>
  doSomethingWithFiles(e.target.files),
);

function doSomethingWithFiles(fileList) {
  console.log("ok");
  let file = null;
  for (let i = 0; i < fileList.length; i++) {
    if (fileList[i].type.match(/^image\//)) {
      file = fileList[i];
      break;
    }
  }
  if (file !== null) {
    console.log(URL.createObjectURL(file));
  }
}