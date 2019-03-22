$('#collection_dropdown_menu').click(function(event) {
	var current_collection = $(event.target).text();
	alert("Current collection : "+current_collection)
    e.preventDefault();// prevent the default anchor functionality
});