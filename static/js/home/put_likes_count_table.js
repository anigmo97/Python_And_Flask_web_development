function put_likes_count_table(container_id,likes_count_files_dict){
	var html_to_add=""
	var num_docs = Object.keys(likes_count_files_dict).length
	var e = null
	var num_users= null
	for (var i=0;i<num_docs;i++) {
		e = likes_count_files_dict[i];
		num_users = Object.keys(e).length - 1;
		html_to_add+="<tr>"
		html_to_add+="<td>"+e["_id"]+"</td>"
		html_to_add+="<td>"+ num_users.toString()+"</td>"
		html_to_add+="<td id='"+e["_id"]+"'></td>"
		html_to_add+="</tr>"
	}
	document.getElementById(container_id).innerHTML= html_to_add	
}