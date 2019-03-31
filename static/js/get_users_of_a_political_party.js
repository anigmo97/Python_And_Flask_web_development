function get_users_of_a_political_party(searched_users,political_party) {
	var lista_politicos = [];
	for (var key in searched_users) {
		if(key != "_id" && key != "total_captured_tweets"){
			if(searched_users[key].partido == political_party){
				lista_politicos.push(key);
			}
		}
	 }
	 return lista_politicos;
}