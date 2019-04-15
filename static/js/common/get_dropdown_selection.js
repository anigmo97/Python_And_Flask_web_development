// cuando se selecciona la coleccion obtenemos el texto y se lo pasamos a la parte de flask
// con una consulta post
$('#collection_dropdown_menu').click(function(event) {
	var current_collection = $(event.target).text();
	alert("Current collection : "+current_collection)
	$.ajax({
		type: "POST",
		contentType: "application/json;charset=utf-8",
		url: "/flask_endpoint",
		traditional: "true",
		data: JSON.stringify(current_collection),
		dataType: "json",
		 success: function(data){
			alert(data);
		 },
	});
	
	e.preventDefault();// prevent the default functionality
});

