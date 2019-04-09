function put_file_image(container_id,file,file_name,error_image,sucess_image){
	if (file == null){
		document.getElementById(container_id).innerHTML="<img src='"+error_image+"' alt='File not found'>"
	}else{
		var href ="javascript:void(0);"
		switch (file_name) {
			case 'statistics_file':
				href = "/special_file/statistics_dict";
			  break;
			case 'query_file':
				href = "/special_file/query_file";
			  break;
			case 'searched_users_file':
				href = "/special_file/searched_users_file";
			  break;
			case 'streamming_file':
				href = "/special_file/streamming_file";
			  break;
			case 'likes_file':
				href = "/special_file/likes_list_file";
			  break;
			case 'users_file':
				href = "/special_file/users_file";
			  break;
			default:
			  console.log('default');
		  } 
		document.getElementById(container_id).innerHTML="<a href='"+href+"'><img class='sucess_file' src='"+sucess_image+"' alt='File retrieved correctly'></a>"
	}
}