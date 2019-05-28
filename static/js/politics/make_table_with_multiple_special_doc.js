function put_table_header(fields,table_id){
	var table_header = "<thead><tr>"
	for( var field_index in fields){
		field_name = fields[field_index];
		table_header+="<th scope='col' class='sort col' data-sort='"+field_name+"'>"+field_name.replace(/_/g," ")+"</th>";
	}
	table_header+="</tr></thead>";
	document.getElementById(table_id).innerHTML = table_header;
}
function make_search_bar(fields,table_id){
	var html_base = "<table><thead><tr>" 
	html_base +="<input class='search list_input col' placeholder='Search' />"
	html_base+="</tr></thead></table>";
	return html_base;	
}

// NECESSARY https://cdnjs.cloudflare.com/ajax/libs/lodash.js/4.17.11/lodash.core.min.js

function make_table_with_multiple_special_doc(container_id,table_header_container,table_id,fields_to_get,special_doc_dict) {

	// make search bar with buttons

	put_table_header(fields_to_get,table_header_container);
	var html_of_search_bar = make_search_bar(fields_to_get,table_id)

	var old_inner_html = document.getElementById(container_id).innerHTML;
	document.getElementById(container_id).innerHTML = html_of_search_bar + old_inner_html;


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
	for( var key in special_doc_dict){
		special_doc = special_doc_dict[key]
		for (var index in special_doc){
			if(index!='_id' && index != 'total_captured_tweets'){
				var aux = {}
				var current = special_doc[index]
				for( var field_index in fields_to_get){
					field_name = fields_to_get[field_index];
					aux[field_name] = _.get(current, field_name).toString(); // this is use to access directly to nested elements ( user.id)
				}
				values.push(aux);
			}
		}
	}

	// alert(JSON.stringify(values, null, 3));
	// alert(JSON.stringify(options, null, 3));

	new List(container_id,options,values);
}