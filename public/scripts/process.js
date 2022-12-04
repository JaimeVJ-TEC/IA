window.onload = function(){
    document.getElementById('btnSubmit').addEventListener("click",process)
    document.getElementById('btnSubmitAlt').addEventListener("click",process)

    const imgInput = document.getElementById("refImg");
    const img = document.getElementById("imgPerro");
    const URL = "http://localhost:8082/"

    imgInput.addEventListener("change", function(){
        getImgData();
    })

    function process(e) {
        var divNombre = document.getElementById('divNombre');
        if(imgInput.files.length == 0){
            window.alert("Sube una foto");
        }
        else{
            divNombre.innerHTML = '<img src="./images/loading.gif" style="width:15%;height:auto display: block; margin-left: auto;margin-right: auto;">'
            let photo = imgInput.files[0];
            let formData = new FormData();
            formData.append("photo",photo);
            if(e.target.id == 'btnSubmit'){
                formData.append("alt",false)
            }
            else {
                formData.append("alt",true)
            }
            fetch(URL, {method: 'POST', body:formData})
            .then((response) => response.json())
            .then((result) => {
                var divDesc = document.getElementById('divDescripcion');
                var imgRaza = document.getElementById('imgRaza');
                nombre = result[0].nombre.charAt(0).toUpperCase() + result[0].nombre.slice(1);
                descripcion = result[0].descripcion;
                divNombre.innerHTML = `<h1>${nombre.replace(/_/g," ")}</h1>`
                divDesc.innerText = descripcion;
                imgRaza.src = `./images/${nombre}.png`
            })
            .catch((error) => {
                window.alert("Error al procesar la foto");
            })
        }
    };

    function getImgData(){
        const file = imgInput.files[0];
        if(file){
            const fileReader = new FileReader();
            fileReader.readAsDataURL(file);
            fileReader.addEventListener("load",function(){
                img.src = this.result
            });
        }
    };
}