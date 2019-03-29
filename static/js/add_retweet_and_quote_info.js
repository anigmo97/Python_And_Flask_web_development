function add_retweet_and_quote_info(tweet_id, tweets_owner_dict){
	var current_registry = tweets_owner_dict[tweet_id];
	//alert(JSON.stringify(current_registry, null, 2));
	if(current_registry["is_retweet"]){
		document.write('<div class="d-flex w-100 justify-content-between">'+
		'<h5 class="mb-1">retweeted_user: ' + current_registry["retweeted_user_screen_name"] +'</h5>'+
		'<p class="mb-1">retweeted_tweet_id: '+ current_registry["retweeted_tweet_id"] +'</p>'+
		'</div>');
	}
	if(current_registry["is_quote"]){
		document.write('<div class="d-flex w-100 justify-content-between"><h5 class="mb-1">quoted_user: ' + current_registry["quoted_user_screen_name"] +'</h5><p class="mb-1">quoted_tweet_id: '+ current_registry["quoted_tweet_id"] +'</p></div>');
	}
}