// con una consulta post
$('#switch_media').change(function(event) {
	var with_media = $('#switch_media').is(':checked');
	$.ajax({
		type: "POST",
		contentType: "application/json;charset=utf-8",
		url: "/rankings_endpoint",
		traditional: "true",
		data: JSON.stringify(with_media),
		dataType: "json",
		 success: function(data){
			
		 },
	});
	location.reload()
	//e.preventDefault();// prevent the default functionality
	
});