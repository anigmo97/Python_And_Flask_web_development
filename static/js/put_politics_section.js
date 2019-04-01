function put_politics_section(politics_list,political_party,container_id,json_searched_users_file) {

	var inner_html_to_add = "<div class='d-flex w-100 p-3 rounded mb-3 justify-content-between flex-row space-between "+political_party+"_members '>"
	// 	<img src='https://avatars.io/twitter/{{ users_dict[e[0]]["screen-names"][0] }}' class="rounded-circle" alt="twt_profile" border="0" width="200" height="200"/>
	// </div>
	var i = 0
	for (var x in politics_list) {
		if (i > 0 && i%5==0){
			inner_html_to_add += "</div>" + "<div class='d-flex w-100 p-3 rounded mb-3 justify-content-between flex-row space-between "+political_party+"_members '>"
		}
		inner_html_to_add += "<div class='member p-2' align='center'>"
		+"<img src='https://avatars.io/twitter/"+politics_list[x]+
		"' class='rounded-circle' alt='twt_profile' border='0' width='100' height='100'/>"+
		"<h5>"+politics_list[x]+"</h5>"+
		"<small>"+json_searched_users_file[politics_list[x]]["captured_tweets"]+" tweets</small>"
		+"</div>"
		i++;
	}

	inner_html_to_add += "</div><br>"
	var old_inner_html = document.getElementById(container_id).innerHTML;
	document.getElementById(container_id).innerHTML =  old_inner_html + inner_html_to_add;
}
