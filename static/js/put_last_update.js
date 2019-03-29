function put_last_update(tweet_id, tweets_owner_dict) {

	// alert(tweet_id);
	// alert(tweets_owner_dict);
	var current_registry = tweets_owner_dict[tweet_id];
	var last_update = current_registry["last_update"]
	var content = '<small>Last update: '+ last_update + ' </small>'
	document.write(content);

}