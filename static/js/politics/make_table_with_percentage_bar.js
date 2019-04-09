function put_table_header_with_percentage(fields,divider,divisor,table_id){
	var table_header = "<thead><tr>";
	var table_length = fields.length;
	for( var field_index in fields){
		field_name = fields[field_index];
		if(field_index == table_length-1){
			table_header+="<th scope='col' class='sort col' data-sort='percentage'>Percentaje</th>";
			table_header+="<th scope='col' class='col' >Percentaje bar</th>";
		}
		table_header+="<th scope='col' class='sort col' data-sort='"+field_name+"'>"+field_name.replace(/_/g," ")+"</th>";

	}
	table_header+="</tr></thead>";
	document.getElementById(table_id).innerHTML = table_header;
};

function make_search_bar(fields,table_id){
	var html_base = "<table><thead><tr>" 
	html_base +="<input class='search list_input col' placeholder='Search' />"
	html_base+="</tr></thead></table>";
	return html_base;	
};

function get_item_template(fields_to_get){
	var template = "<tr>";
	var table_length = fields_to_get.length;
	for( var field_index in fields_to_get){
		field_name = fields_to_get[field_index];
		if(field_index == table_length-1){
			template+="<td class='col percentage'></td>";
			template+="<td class='col percentage_bar'></td>";
		}
		template+="<td class='col "+field_name+"'></td>";		
	}
	template+="</tr>";
	return template
};

function get_fields_to_get_with_additional_cols(fields_to_get){
	var table_length = fields_to_get.length;
	var fields_to_get_with_percentage = [];
	for( var field_index in fields_to_get){
		field_name = fields_to_get[field_index];
		if(field_index == table_length-1){
			fields_to_get_with_percentage.push("percentage");
			fields_to_get_with_percentage.push("percentage_bar");
		}
		fields_to_get_with_percentage.push(field_name);	
		
	}
	return fields_to_get_with_percentage;
}


function make_table_with_percentage_bar(container_id,table_header_container,table_id,fields_to_get,divider_field,divisor_field,special_doc) {

	// make search bar with buttons

	put_table_header_with_percentage(fields_to_get,divider_field,divisor_field,table_header_container);
	
	
	var html_of_search_bar = make_search_bar(fields_to_get,table_id)
	var old_inner_html = document.getElementById(container_id).innerHTML;
	document.getElementById(container_id).innerHTML = html_of_search_bar + old_inner_html;

	var fields_to_get_with_percentage = get_fields_to_get_with_additional_cols(fields_to_get);

	var template_for_data = get_item_template(fields_to_get);


		var options = { 
		valueNames : fields_to_get_with_percentage ,  
		item: template_for_data,
		// page: 10,
  		// pagination: true
	};
	var values = []
	var percentage_without_sign;
	var percentage_bar_html ;
	for (var index in special_doc){
		if(index!='_id' && index != 'total_captured_tweets'){
			var aux = {}
			for( var field_index in fields_to_get){
				field_name = fields_to_get[field_index];
				aux[field_name] = special_doc[index][field_name];
			}
			if (aux[divisor_field] > 0){
				percentage_without_sign = ((aux[divider_field] / aux[divisor_field])*100).toFixed(2)
				aux["percentage"] = percentage_without_sign + '%'
			}else{
				percentage_without_sign = '0.00'
				aux["percentage"] = '0.00%'
			}
			percentage_bar_html='<div style="list-style:none;" class="percentage_bar_div">'
			percentage_bar_html+='<li class="percentage_bar" style="list-style:none;">'
			percentage_bar_html+=percentage_without_sign+'</li></div>'
			aux["percentage_bar"] =percentage_bar_html
			values.push(aux);
		}
	}
	// alert(JSON.stringify(aux, null, 3));

	// alert(JSON.stringify(values, null, 3));
	// alert(JSON.stringify(options, null, 3));

	new List(container_id,options,values);

}




