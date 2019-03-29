function put_one_user_screen_name_from_statistics_dict(user_id,users_dict) {
	//var str = JSON.stringify(embed_dict, null, 2);
	//alert("with media "+with_media);
	var registry = embed_dict[user_id];
	var screen_name_list = registry["screen-names"]
	if (screen_name_list.length >0){
	   return screen_name_list[0];
	} else {
		return null;
	}
}