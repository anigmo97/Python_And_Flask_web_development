function get_member_html(user_screen_name,amount,measure,index,image_1,image_2,image_3){
	if(index==1){
		var aux = "<div class='p-2 member member_1 justify-content-center'  align='center'>";
		aux+="<img src='"+image_1+ "' align=left class='row px-1 medal' >"
		aux += "<img src='https://avatars.io/twitter/" + user_screen_name + "' class='rounded-circle' alt='twt_profile' style='margin-top:20px' border='0' width='100' height='100'/>"

	}else if(index ==2){
		var aux = "<div class='p-2 member member_2' align='center'>";
		aux+="<img src='"+image_2+ "' align=left class='row px-1 medal' >"
		aux += "<img src='https://avatars.io/twitter/" + user_screen_name + "' class='rounded-circle' style='margin-top:20px' alt='twt_profile' border='0' width='100' height='100'/>"

	}else if(index==3){
		var aux = "<div class='p-2 member member_3' align='center'>";
		aux+="<img src='"+image_3+ "' align=left class='row px-1 medal' >"
		aux += "<img src='https://avatars.io/twitter/" + user_screen_name + "' class='rounded-circle' style='margin-top:20px' alt='twt_profile' border='0' width='100' height='100'/>"

	}else{
		var aux = "<div class='p-2 member' align='center'>";
		aux+="<small align=left class='row px-3' >"+index+"</small>"
		aux += "<img src='https://avatars.io/twitter/" + user_screen_name + "' class='rounded-circle'  alt='twt_profile' border='0' width='100' height='100'/>"

	}
	
	
	aux +="<h5>"+user_screen_name+"</h5>";
	aux +="<small>"+amount+measure+"</small>";
	aux +="</div>";
	return aux;
}

function get_new_row(initial){
	var aux =null;
	if(!initial){
		aux = "</div>" 
	}
	aux += "<div class='d-flex w-100 p-3 rounded mb-3 justify-content-between flex-row space-between top_members '>"
	return aux
}

function put_top_users_section(top_list,measure,container_id,users_dict,image_1,image_2,image_3) {
	var inner_html_to_add = get_new_row(true)
	var screen_name = null;
	var user_id = null;
	var amount = null;
	for (var index in top_list) {
		if (index > 0 && index%5==0){
			inner_html_to_add+= get_new_row(false)
		}
		user_id = top_list[index][0];
		if( user_id != 0){
			amount = top_list[index][1];
			screen_name = users_dict[user_id]["screen-names"][0];
			inner_html_to_add += get_member_html(screen_name,amount,measure,parseInt(index)+1,image_1,image_2,image_3)
		}
	}

	inner_html_to_add += "</div><br>"
	var old_inner_html = document.getElementById(container_id).innerHTML;
	document.getElementById(container_id).innerHTML =  old_inner_html + inner_html_to_add;
}
