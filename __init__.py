from flask import Flask
from flask import request,render_template,url_for,jsonify
import subprocess 
import signal
import sys
import json
import mongo_conector_for_flask as mongo_conector
from django.utils.safestring import mark_safe
from dateutil.relativedelta import relativedelta
import datetime
import wikipedia
try: 
    from BeautifulSoup import BeautifulSoup
except ImportError:
    from bs4 import BeautifulSoup

collections = mongo_conector.get_collection_names()
with_media_state = False
if len(collections)>0:
	mongo_conector.current_collection = collections[0]

################################################################################################################################
################################################ GET MONGO SPECIAL FILES DICT ##################################################
################################################################################################################################
def get_mongo_special_files_dict():
	docs_dict = {}
	docs_dict["statistics_dict"] = mongo_conector.get_statistics_file_from_collection(mongo_conector.current_collection)
	docs_dict["query_file"] = mongo_conector.get_query_file(mongo_conector.current_collection)
	docs_dict["searched_users_file"] = mongo_conector.get_searched_users_file(mongo_conector.current_collection)
	docs_dict["streamming_file"] = mongo_conector.get_streamming_file(mongo_conector.current_collection)
	docs_dict["likes_list_file"] = mongo_conector.get_likes_list_file(mongo_conector.current_collection)	
	docs_dict["users_file"] = {"info":"Deprecated. Now the info is saved in likes_counts_files"}
	return docs_dict

def get_article_summary(person_name,topic=""):
	resumen = ""
	url = ""
	try:
		wikipedia.set_lang("es")
		article = wikipedia.search("{} {}".format(person_name,topic))[0]
		pg = wikipedia.page(article)
		resumen = pg.summary
		resumen = ".".join(resumen.split(".")[0:4])
	except wikipedia.DisambiguationError as e:
		try:
			pg = wikipedia.page(e.options[0])
			resumen = pg.summary
			resumen = ".".join(resumen.split(".")[0:4])
		except wikipedia.DisambiguationError:
			pg = wikipedia.page(e.options[1])
			resumen = pg.summary
			resumen = ".".join(resumen.split(".")[0:4])
	return resumen,pg.url


def get_main_image(person_name,topic=""):
	main_image_url = ""
	try:
		wikipedia.set_lang("es")
		article = wikipedia.search("{} {}".format(person_name,topic))[0]
		pg = wikipedia.page(article)
		main_image_url = pg.images[0]
	except wikipedia.DisambiguationError as e:
		try:
			pg = wikipedia.page(e.options[0])
			main_image_url = pg.images[0]
		except wikipedia.DisambiguationError:
			pg = wikipedia.page(e.options[1])
			main_image_url = pg.images[0]
	return main_image_url

def get_main_image2(person_name,topic=""):
	main_image_url = ""
	try:
		wikipedia.set_lang("es")
		article = wikipedia.search("{} {}".format(person_name,topic))[0]
		pg = wikipedia.page(article)
		soup = BeautifulSoup(str(pg.html),'html.parser')
		main_image_url = soup.select_one(".infobox.biography.vcard>tr>td>a.image")
	except wikipedia.DisambiguationError as e:
		print("ex1")
		try:
			pg = wikipedia.page(e.options[0]) 
			soup = BeautifulSoup(pg.html,'html.parser')
			main_image_url = soup.select_one(".infobox.biography.vcard>tr>td>a.image")
		except wikipedia.DisambiguationError:
			print("ex2")
			pg = wikipedia.page(e.options[1]) 
			soup = BeautifulSoup(pg.html,'html.parser')
			main_image_url = soup.select_one(".infobox.biography.vcard>tr>td>a.image")
	print(main_image_url)
	return main_image_url

def get_likes_per_party_info():
	likes_count_files_cursor =mongo_conector.get_likes_count_files_cursor(mongo_conector.current_collection)
	captured_likes_tweets = {"PP":0,"PSOE":0,"PODEMOS":0,"CIUDADANOS":0,"VOX":0,"COMPROMIS":0}
	registry_dict_by_verified = {"PP":{},"PSOE":{},"PODEMOS":{},"CIUDADANOS":{},"COMPROMIS":{},"VOX":{}}
	registry_dict_by_num_tweets = {"PP":{},"PSOE":{},"PODEMOS":{},"CIUDADANOS":{},"COMPROMIS":{},"VOX":{}}
	registry_dict_by_antiquity = {"PP":{},"PSOE":{},"PODEMOS":{},"CIUDADANOS":{},"COMPROMIS":{},"VOX":{}}
	votantes_por_partido = {"PP":{},"PSOE":{},"PODEMOS":{},"CIUDADANOS":{},"COMPROMIS":{},"VOX":{}}
	for like_count_file in likes_count_files_cursor:
		for e in like_count_file:
			if e !="_id":
				registry_dict = like_count_file[e]
				print(registry_dict)
				joined = get_antiquity_range(registry_dict.get("joined",None))
				tweets_metric = get_range(registry_dict.get("tweets",0))

				if registry_dict.get("verified",False):
					verified = "verified"
				else:
					verified = "not verified"
				
				print("\n\n\n{} {} {} ".format(joined,verified,tweets_metric))

				likes_per_party_list = [registry_dict["likes_to_PP"],registry_dict["likes_to_PSOE"],registry_dict["likes_to_PODEMOS"],registry_dict["likes_to_CIUDADANOS"],registry_dict["likes_to_COMPROMIS"],registry_dict["likes_to_VOX"]]
				max_amount_likes_to_party = max(likes_per_party_list)
				most_voted_party = ["PP","PSOE","PODEMOS","CIUDADANOS","COMPROMIS","VOX"][likes_per_party_list.index(max_amount_likes_to_party)]
				if joined not in votantes_por_partido[most_voted_party]:
					votantes_por_partido[most_voted_party][joined] = {}
				if verified not in votantes_por_partido[most_voted_party][joined]:
					votantes_por_partido[most_voted_party][joined][verified] = {}
				if tweets_metric not in votantes_por_partido[most_voted_party][joined][verified]:
					votantes_por_partido[most_voted_party][joined][verified][tweets_metric] = []
				votantes_por_partido[most_voted_party][joined][verified][tweets_metric].append(max_amount_likes_to_party)


				for party in ["PP","PSOE","PODEMOS","CIUDADANOS","COMPROMIS","VOX"]:
					if registry_dict["likes_to_" + party] >0:
						captured_likes_tweets[party] += registry_dict["likes_to_" + party]
						registry_dict_by_verified[party][verified] = registry_dict_by_verified[party].get(verified,0) + 1
						registry_dict_by_num_tweets[party][tweets_metric] = registry_dict_by_num_tweets[party].get(tweets_metric,0) + 1
						registry_dict_by_antiquity[party][joined] = registry_dict_by_antiquity[party].get(joined,0) + 1

	return captured_likes_tweets,registry_dict_by_verified,registry_dict_by_num_tweets,registry_dict_by_antiquity,votantes_por_partido


app = Flask(__name__)
def signal_handler_control_c(sig, frame):
	print('Ctrl+C handled')
	sys.exit(0)
signal.signal(signal.SIGINT, signal_handler_control_c)

def signal_handler_control_z(sig, frame):
	print('Ctrl+Z handled')
	sys.exit(0)
signal.signal(signal.SIGTSTP,signal_handler_control_z)

@app.route('/')
def homepage():
	special_doc_dict = get_mongo_special_files_dict()
	if special_doc_dict["statistics_dict"] == None:
		special_doc_dict["statistics_dict"] = False
		last_update = "Sin fichero de estadísticas"
	else:
		last_update = special_doc_dict["statistics_dict"]["ultima_modificación"]

	try:
		return render_template("home.html", collections=collections,collection=mongo_conector.current_collection,
		last_update=last_update,likes_count_files_list=mongo_conector.get_likes_count_files_dict(mongo_conector.current_collection),
		**special_doc_dict)
	except Exception as e:
		return str(e)


@app.route('/rankings')
def rankings():
	global with_media_state
	user_screen_name_dict = None
	users_dict = None
	special_doc_dict = get_mongo_special_files_dict()

	if special_doc_dict["statistics_dict"] == None:
		special_doc_dict["statistics_dict"] = False
	else:
		user_screen_name_dict = mongo_conector.get_users_screen_name_dict_of_tweet_ids_for_tops_in_statistics_file(special_doc_dict["statistics_dict"],mongo_conector.current_collection)
		users_dict = special_doc_dict["statistics_dict"]["users_dict"]
	try:
		return render_template("rankings.html", users_dict=users_dict,user_screen_name_dict=user_screen_name_dict,
		collections=collections,collection=mongo_conector.current_collection,with_media=with_media_state,**special_doc_dict)
	except Exception as e:
		return str(e)

@app.route('/politics_tweets')
def politics_tweets():
	special_doc_dict = get_mongo_special_files_dict()
	politicos_por_partido = {"PP" : 0, "PSOE":0,"CIUDADANOS":0,"PODEMOS":0, "COMPROMIS":0 ,"VOX":0}
	likes_por_partido = {"PP" : 0, "PSOE":0,"CIUDADANOS":0,"PODEMOS":0, "COMPROMIS":0 ,"VOX":0}
	linked_likes_info = mongo_conector.get_likes_info_for_flask(mongo_conector.current_collection)
	if special_doc_dict.get("searched_users_file",None) != None:
		for k,v in special_doc_dict["searched_users_file"].items():
			if k != '_id' and k != 'total_captured_tweets':
				if v["partido"] != None:
					politicos_por_partido[v["partido"]] += 1
	
	linked_aux = []
	if len(linked_likes_info)>0:
		for e in linked_likes_info:
			likes_info = e["likes_info"]
			linked_aux.append(likes_info)
			user_sreen_name = likes_info["user_screen_name"]
			if special_doc_dict["searched_users_file"][user_sreen_name]["partido"] != None:
				aux = likes_info["num_likes"]
				if type(aux) == int:
					likes_por_partido[special_doc_dict["searched_users_file"][user_sreen_name]["partido"]] += aux
				else:
					likes_por_partido[special_doc_dict["searched_users_file"][user_sreen_name]["partido"]] += int(aux.replace(',',''))	
	linked_likes_info=linked_aux
	captured_likes_por_partido,registry_dict_by_verified,registry_dict_by_num_tweets,registry_dict_by_antiquity,votantes_por_partido = get_likes_per_party_info()
	print(captured_likes_por_partido)
	print(json.dumps(votantes_por_partido))
		
	try:
		return render_template("politics_tweets.html",collections=collections,
		collection=mongo_conector.current_collection,**special_doc_dict,
		likes_por_partido=likes_por_partido, # likes de los tweets de un partido (no todos son capturados)
		captured_likes_por_partido =captured_likes_por_partido ,
		politicos_por_partido=politicos_por_partido,
		likes_count_files=mongo_conector.get_likes_count_files_dict(mongo_conector.current_collection),
		linked_likes_info=linked_likes_info,
		registry_dict_by_verified=registry_dict_by_verified,
		registry_dict_by_num_tweets=registry_dict_by_num_tweets,
		registry_dict_by_antiquity=registry_dict_by_antiquity,
		votantes_por_partido = votantes_por_partido
		)
	except Exception as e:
		return str(e)

@app.route('/statistics')
def statistics_page():
	special_doc_dict = get_mongo_special_files_dict()
	if special_doc_dict["statistics_dict"] == None:
		special_doc_dict["statistics_dict"] = False
	try:
		return render_template("general_statistics.html", collections=collections,collection=mongo_conector.current_collection,**special_doc_dict)
	except Exception as e:
		return str(e)

@app.route('/stop')
def stop():
	global run_flag
	run_flag = False


@app.route('/quit')
def quit():
	func = request.environ.get('werkzeug.server.shutdown')
	func()
	return "Quitting..."

@app.route('/flask_endpoint', methods=['POST'])
def get_names():
	if request.method == 'POST':
		names = request.get_json()
		if type(names) == str:
			mongo_conector.current_collection = names
			print("\n\n\n\n collection changed to {}".format(names))
		else:
			raise Exception("Unexpected collection name")		
	return '', 200

@app.route('/rankings_endpoint', methods=['POST'])
def get_with_media_state():
	if request.method == 'POST':
		global with_media_state
		state = request.get_json()
		with_media_state = state
		print("with media toogle_changed to {}".format(with_media_state))		
	return '', 200

@app.route('/getmethod/with_media_state',methods=['GET'])
def get_javascript_data():
	print("Send withm_media_state to html: {}".format(with_media_state))
	return  jsonify({"with_media_state":with_media_state})


@app.route('/special_file/',defaults={'path':''})
@app.route('/special_file/<path:path>')
def show_statistics_file(path): 
	special_doc_dict = get_mongo_special_files_dict()
	special_doc = special_doc_dict.get(path,None)
	if special_doc == None:
		special_doc_dict = mongo_conector.get_likes_count_files_dict_with_id_as_key(mongo_conector.current_collection)
		special_doc = special_doc_dict.get(path,None)
	return jsonify(special_doc)

@app.route('/search/',defaults={'path':''})
@app.route('/search/<path:path>')
def show_tweet_search_result(path): 
	if(len(path) >0 and path[-1]=='?'):
		path = path[0:-1]
	dict_result = mongo_conector.get_tweet_dict_by_tweet_id_using_regex(path,mongo_conector.current_collection)
	try:
		return render_template("search.html", collections=collections,collection=mongo_conector.current_collection,dict_result=dict_result,len_result=len(dict_result))
	except Exception as e:
		return str(e)

def get_range(value):
	if value>= 0 and value < 50:
		return "Menos de 50 tweets"
	elif value>= 50 and value < 100:
		return "Entre 50 y 99 tweets"
	elif value >= 100 and value < 250:
		return "Entre 100 y 249 tweets"
	elif value>= 250 and value < 500:
		return "Entre 250 y 499 tweets"
	elif value >=500 and value < 1000:
		return "Entre 500 y 999 tweets"
	else:
		return "1000 tweets o más"

def get_antiquity_range(date_str):
	if date_str == None or date_str == "desconocido":
		return "desconocido"
	input_format="%Y/%m/%d %H:%M"
	date_time_obj = datetime.datetime.strptime(date_str,input_format)
	date_time_obj_now = datetime.datetime.now()
	if (date_time_obj + relativedelta(months=3) )>date_time_obj_now:
		return "Menos de tres meses"
	elif (date_time_obj + relativedelta(months=6) )>date_time_obj_now:
		return "Entre 3 y 6 meses"
	elif (date_time_obj + relativedelta(months=12) )>date_time_obj_now:
		return "Entre 6 y 12 meses"
	elif (date_time_obj + relativedelta(months=24) )>date_time_obj_now:
		return "Entre 1 y 2 años"
	elif (date_time_obj + relativedelta(months=36) )>date_time_obj_now:
		return "Entre 2 y 3 años"
	else:
		return "Más de 3 años"


@app.route('/searched_user_registry/',defaults={'path':''})
@app.route('/searched_user_registry/<path:path>')
def show_searched_user_registry(path): 
	if(len(path) >0 and path[-1]=='?'):
		path = path[0:-1]
	try:
		splitted_path = path.split("&")
		print(path)
		print(splitted_path)
		name = splitted_path[0]
		screen_name = splitted_path[1] 
	except Exception as e:
		print("EXCEP {}".format(e))
	resumen,url = get_article_summary(name,"politica españa")
	searched_user_registry = mongo_conector.get_searched_users_file(mongo_conector.current_collection)[screen_name]
	num_captured_likes = mongo_conector.get_num_of_captured_likes_for_user(screen_name.lower(),mongo_conector.current_collection)
	registry_dict,num_verified,num_no_verified = mongo_conector.get_searched_user_registry_info_for_ui(screen_name,mongo_conector.current_collection)
	registry_dict_by_num_likes = {}
	registry_dict_by_num_tweets = {}
	registry_dict_by_antiquity = {}
	for e in registry_dict:
		print(registry_dict[e])
		if registry_dict[e]["num_likes"] in registry_dict_by_num_likes:
			registry_dict_by_num_likes[registry_dict[e]["num_likes"]] += 1
		else:
			registry_dict_by_num_likes[registry_dict[e]["num_likes"]] = 1

		correct_range = get_range(registry_dict[e].get("tweets",0))
		if  correct_range in registry_dict_by_num_tweets:
			registry_dict_by_num_tweets[correct_range] += 1
		else:
			registry_dict_by_num_tweets[correct_range] = 1

		correct_range = get_antiquity_range(registry_dict[e].get("joined",None))
		if correct_range in registry_dict_by_antiquity:
			registry_dict_by_antiquity[correct_range] +=1
		else:
			registry_dict_by_antiquity[correct_range] = 1



	try:
		return render_template("searched_user_registry.html", collections=collections,collection=mongo_conector.current_collection,
		name=name,screen_name=screen_name,resumen=resumen,searched_user_registry=searched_user_registry,
		num_captured_likes=num_captured_likes,url=url,registry_dict=registry_dict,num_verified=num_verified,
		num_no_verified=num_no_verified,registry_dict_by_num_likes=registry_dict_by_num_likes,registry_dict_by_num_tweets=registry_dict_by_num_tweets,
		registry_dict_by_antiquity=registry_dict_by_antiquity)
	except Exception as e:
		return str(e)

@app.route('/show_file/',defaults={'path':''})
@app.route('/show_file/<path:path>')
def show_file(path): 
	if(len(path) >0 and path[-1]=='?'):
		path = path[0:-1]
	doc = mongo_conector.get_tweet_by_id(path,mongo_conector.current_collection)
	return jsonify(doc)



if __name__ == "__main__":
	try:
		app.run(debug=True,host='127.0.0.1',port=8000)
	except Exception as e:
		print(e.__cause__)
		subprocess.call("sudo lsof -i:8000",shell=True)

