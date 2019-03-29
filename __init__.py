from flask import Flask
from flask import request,render_template,url_for
import subprocess 
import signal
import sys
import json
import mongo_conector_for_flask as mongo_conector
from django.utils.safestring import mark_safe

collections = mongo_conector.get_collection_names()
if len(collections)>0:
	mongo_conector.current_collection = collections[0]


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

	statistics_dict = mongo_conector.get_statistics_file_from_collection(mongo_conector.current_collection)
	if statistics_dict == None:
		last_update = "Sin fichero de estadísticas"
	else:
		last_update = statistics_dict["ultima_modificación"]

	try:
		return render_template("home.html", collections=collections,collection=mongo_conector.current_collection,last_update=last_update)
	except Exception as e:
		return str(e)


@app.route('/rankings')
def rankings():

	user_screen_name_dict = None
	users_dict = None
	query_file = None
	query_user_file = None
	streamming_file = None
	statistics_dict = mongo_conector.get_statistics_file_from_collection(mongo_conector.current_collection)
	if statistics_dict == None:
		statistics_dict = False
	else:
		user_screen_name_dict = mongo_conector.get_users_screen_name_dict_of_tweet_ids_for_tops_in_statistics_file(statistics_dict,mongo_conector.current_collection)
		query_file = mongo_conector.get_query_file(mongo_conector.current_collection)
		query_user_file = mongo_conector.get_searched_users_file(mongo_conector.current_collection)
		streamming_file = mongo_conector.get_statistics_file_from_collection(mongo_conector.current_collection)
		users_dict = statistics_dict["users_dict"]
	try:
		return render_template("test.html", statistics_dict=statistics_dict,users_dict=users_dict,user_screen_name_dict=user_screen_name_dict,
		query_file = query_file, query_user_file=query_user_file, streamming_file=streamming_file,
		collections=collections,collection=mongo_conector.current_collection)
	except Exception as e:
		return str(e)

@app.route('/politics_tweets')
def politics_tweets():

	paragraph = [ "pargraph1","paragraph222","paragraph333"]
	page_type = 'about'

	try:
		return render_template("index.html", paragraph=paragraph, page_type=page_type,collections=collections,collection=mongo_conector.current_collection)
	except Exception as e:
		return str(e)

@app.route('/statistics')
def statistics_page():
	query_file = None
	query_user_file = None
	streamming_file = None
	statistics_dict = mongo_conector.get_statistics_file_from_collection(mongo_conector.current_collection)
	if statistics_dict == None:
		statistics_dict = False
	else:
		query_file = mongo_conector.get_query_file(mongo_conector.current_collection)
		query_user_file = mongo_conector.get_searched_users_file(mongo_conector.current_collection)
		streamming_file = mongo_conector.get_streamming_file(mongo_conector.current_collection)
	page_type = 'about-contact'


	try:
		return render_template("general_statistics.html", statistics_dict=statistics_dict, page_type=page_type,
		query_file = query_file, query_user_file=query_user_file, streamming_file=streamming_file,
		collections=collections,collection=mongo_conector.current_collection)
	except Exception as e:
		return str(e)

@app.route('/graph_example')
def graph(chartID = 'primer_chart', chart_type = 'line', chart_height = 500):
	webpage_title = "EPIC TITLE"
	chart = {"renderTo": chartID, "type": chart_type, "height": chart_height,}
	series = [{"name": 'Label1', "data": [1,2,3]}, {"name": 'Label2', "data": [4, 5, 6]}]
	title = {"text": 'My Title'}
	xAxis = {"categories": ['xAxis Data1', 'xAxis Data2', 'xAxis Data3']}
	yAxis = {"title": {"text": 'yAxis Label'}}
	return render_template('index.html', collections=collections,webpage_title=webpage_title,chartID=chartID, chart=chart, series=series, title=title, xAxis=xAxis, yAxis=yAxis)
 
 



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

if __name__ == "__main__":
	try:
		app.run(debug=True,host='127.0.0.1',port=8000)
	except Exception as e:
		print(e.__cause__)
		subprocess.call("sudo lsof -i:8000",shell=True)

