function get_num_likes_by_party(json_users_file) {
	var dict_likes = {PP : 0, PSOE :0, PODEMOS : 0, VOX:0 , COMPROMIS:0, CIUDADANOS:0}
	for (var x in json_users_file) {
		if(x!="_id" && x!= "total_captured_tweets"){
			dict_likes["PP"] = dict_likes["PP"] + json_users_file[x]["likes_to_PP"]
			dict_likes["PSOE"] = dict_likes["PSOE"] + json_users_file[x]["likes_to_PSOE"]
			dict_likes["PODEMOS"] = dict_likes["PODEMOS"] + json_users_file[x]["likes_to_PODEMOS"]
			dict_likes["CIUDADANOS"] = dict_likes["CIUDADANOS"] + json_users_file[x]["likes_to_CIUDADANOS"]
			dict_likes["VOX"] = dict_likes["VOX"] + json_users_file[x]["likes_to_VOX"]
			dict_likes["COMPROMIS"] = dict_likes["COMPROMIS"] + json_users_file[x]["likes_to_COMPROMIS"]
		}
	}
	return dict_likes;
}