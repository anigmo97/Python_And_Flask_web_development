function get_num_tweets_by_party(json_searched_users_file) {
	var dict_tweets = {PP : 0, PSOE :0, PODEMOS : 0, VOX:0 , COMPROMIS:0, CIUDADANOS:0}
	var partido = null
	for (var x in json_searched_users_file) {
		if(x!="_id" && x!= "total_captured_tweets"){
			partido = json_searched_users_file[x].partido
			dict_tweets[partido] = dict_tweets[partido] + json_searched_users_file[x]["captured_tweets"]
		}
	}
	return dict_tweets;
}