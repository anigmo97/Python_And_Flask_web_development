function make_search_bar(fields){
	var html_base = "<div class='d-flex w-100 mb-3 flex-row'>" + 
		"<input class='search list_input col' placeholder='Search' />";

	for( var field_index in fields){
			field_name = fields[field_index];
			html_base+="<button class='sort col' data-sort='"+field_name+"'>Sort by "+field_name+"</button>";
		}
	html_base+="</div>";
	html_base+= "<div class='d-flex mb-5 center flex-row'>"
	for( var field_index in fields){
		field_name = fields[field_index];
		html_base+="<h3 class='col'>"+field_name+"</h3>";
	}
	html_base+="</div>";
	return html_base;	
}



function make_table_with_special_doc(container_id,fields_to_get,special_doc) {

	// make search bar with buttons
	var html_of_search_bar = make_search_bar(fields_to_get)

	var old_inner_html = document.getElementById(container_id).innerHTML;
	document.getElementById(container_id).innerHTML = html_of_search_bar + old_inner_html;


	var template_for_data = "<li class='d-flex w-100 mb-3 flex-row'>"
	for( var field_index in fields_to_get){
		field_name = fields_to_get[field_index];
		template_for_data+="<h3 class=' col "+field_name+"'></h3>";	
	}
	template_for_data+="</li>"
	var options = { valueNames : fields_to_get ,  item: template_for_data};
	var values = []
	for (var index in special_doc){
		if(index!='_id' && index != 'total_captured_tweets'){
			var aux = {}
			for( var field_index in fields_to_get){
				field_name = fields_to_get[field_index];
				aux[field_name] = special_doc[index][field_name];
			}
			values.push(aux);
		}
	}

	// alert(JSON.stringify(values, null, 3));
	// alert(JSON.stringify(options, null, 3));

	new List(container_id,options,values);
}