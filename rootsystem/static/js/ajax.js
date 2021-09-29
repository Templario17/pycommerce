function cargar(recurso, titulo){
    var xmlhttp;
    var layer;
    xmlhttp = new XMLHttpRequest();
    xmlhttp.onreadystatechange = function(){
        respuesta = xmlhttp.readyState;
        estado = xmlhttp.status;
        if (respuesta == 4 && estado == 200){
            layer = document.getElementById('respuesta');
            layer.innerHTML = xmlhttp.responseText;
            document.getElementById('titulo').innerHTML = titulo;
        } else {
            document.getElementById('respuesta').innerHTML = "Cargando ...";
        }
    }
    xmlhttp.open("GET", recurso, true);
    xmlhttp.send();
}
