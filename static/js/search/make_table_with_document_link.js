function put_table_header_with_doc(fields,table_id){
	var table_header = "<thead><tr>"
	for( var field_index in fields){
		field_name = fields[field_index];
		table_header+="<th scope='col' class='sort col' data-sort='"+field_name+"'>"+field_name.replace(/_/g," ")+"</th>";
		if(field_index == fields.length-1){
			table_header+="<th scope='col' class='col'>Show file</th>";
		}
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

function make_table_with_document_link(container_id,table_header_container,table_id,fields_to_get,special_doc,url) {

	// make search bar with buttons

	put_table_header_with_doc(fields_to_get,table_header_container);
	var html_of_search_bar = make_search_bar(fields_to_get,table_id)

	var old_inner_html = document.getElementById(container_id).innerHTML;
	document.getElementById(container_id).innerHTML = html_of_search_bar + old_inner_html;

	var template_for_data = "<tr>"
	for( var field_index in fields_to_get){
		field_name = fields_to_get[field_index];
		if(field_index == 0){
			template_for_data+="<td class='id_col col "+field_name+"'></td>";	
		}else{
			template_for_data+="<td class='col "+field_name+"'></td>";	
		}

		if(field_index == fields_to_get.length-1){
			var td_with_image = "<td class='col file_col'>"
			td_with_image+="<a class='file_link' href='#' target='_blank'><img class='file_img' src='"+url+"' alt='Show file'></a>"
			td_with_image+="</td>";
			template_for_data+=td_with_image;
		}
	}
	template_for_data+="</tr>"
	var options = { 
		valueNames : fields_to_get ,  
		item: template_for_data,
		page: 20,
  		pagination: true
	};
	var values = []
	for (var index in special_doc){
		if(index!='_id' && index != 'total_captured_tweets'){
			var aux = {}
			var current = special_doc[index]
			for( var field_index in fields_to_get){
				field_name = fields_to_get[field_index];
				try {
					aux[field_name] = _.get(current, field_name).toString() ; // this is use to access directly to nested elements ( user.id)
				  }
				  catch(error) {
					console.error(error);
					aux[field_name] = null;
				  }
			}
			values.push(aux);
		}
	}

	// alert(JSON.stringify(values, null, 3));
	// alert(JSON.stringify(options, null, 3));

	new List(container_id,options,values);
}