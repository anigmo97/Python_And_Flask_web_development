// function put_table_header(fields,container_id){
// 	var table_header = "<table class='table table-striped table-dark'><thead><tr>"
// 	for( var field_index in fields){
// 		field_name = fields[field_index];
// 		table_header+="<th scope='col'>"+field_name+"</th>";
// 	}
// 	table_header+="</tr></thead></table>";
// 	alert(table_header)
// 	var old_inner_html = document.getElementById(container_id).innerHTML;
// 	document.getElementById(container_id).innerHTML = table_header + old_inner_html;
// }
function put_table_header(fields,table_id){
	var table_header = "<thead><tr>"
	for( var field_index in fields){
		field_name = fields[field_index];
		table_header+="<th scope='col' class='sort col' data-sort='"+field_name+"'>"+field_name.replace(/_/g," ")+"</th>";
	}
	table_header+="</tr></thead>";
	alert(table_header)
	document.getElementById(table_id).innerHTML = table_header;
}
// function make_search_bar(fields,table_id){
// 	var html_base = "<div class='d-flex w-100 mb-3 flex-row'>" + 
// 		"<input class='search list_input col' placeholder='Search' />";

// 	for( var field_index in fields){
// 			field_name = fields[field_index];
// 			html_base+="<button class='sort col' data-sort='"+field_name+"'>Sort by "+field_name+"</button>";
// 		}
// 	html_base+="</div>";
// 	alert(html_base)
// 	return html_base;	
// }



function make_table_with_special_doc(container_id,table_header_container,table_id,fields_to_get,special_doc) {

	// make search bar with buttons

	put_table_header(fields_to_get,table_header_container);
	// var html_of_search_bar = make_search_bar(fields_to_get,table_id)

	// var old_inner_html = document.getElementById(container_id).innerHTML;
	// alert(old_inner_html)
	// document.getElementById(container_id).innerHTML = html_of_search_bar + old_inner_html;


	var template_for_data = "<tr>"
	for( var field_index in fields_to_get){
		field_name = fields_to_get[field_index];
		template_for_data+="<td class='col "+field_name+"'></td>";	
	}
	template_for_data+="</tr>"
	var options = { 
		valueNames : fields_to_get ,  
		item: template_for_data,
		page: 10,
  		pagination: true
	};
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