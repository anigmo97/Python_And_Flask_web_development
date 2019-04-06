from flask import Flask
from flask import request,render_template,url_for,jsonify
import subprocess 
import signal
import sys
import json
import mongo_conector_for_flask as mongo_conector
from django.utils.safestring import mark_safe

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
	docs_dict["users_file"] = mongo_conector.get_users_file(mongo_conector.current_collection)
	return docs_dict


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
		return render_template("home.html", collections=collections,collection=mongo_conector.current_collection,last_update=last_update,**special_doc_dict)
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
	try:
		return render_template("politics_tweets.html",collections=collections,collection=mongo_conector.current_collection,**special_doc_dict)
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

