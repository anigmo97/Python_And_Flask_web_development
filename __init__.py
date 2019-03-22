from flask import Flask
from flask import request,render_template,url_for
import subprocess
import signal
import sys

collections=['test2', 'test', 'prueba', 'tweets'] #TODO CALL MONGO

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

	# title = "Epic title"
	paragraph = [ "pargraph1","paragraph222","paragraph333"]

	try:
		return render_template("index.html", paragraph=paragraph, collections=collections)
	except Exception as e:
		return str(e)


@app.route('/rankings')
def rankings():

	paragraph = [ "pargraph1","paragraph222","paragraph333"]
	page_type = 'about'

	try:
		return render_template("index.html", paragraph=paragraph, page_type=page_type,collections=collections)
	except Exception as e:
		return str(e)

@app.route('/politics_tweets')
def politics_tweets():

	paragraph = [ "pargraph1","paragraph222","paragraph333"]
	page_type = 'about'

	try:
		return render_template("index.html", paragraph=paragraph, page_type=page_type,collections=collections)
	except Exception as e:
		return str(e)

@app.route('/statistics')
def statistics_page():

	paragraph = [ "pargraph1","paragraph222","paragraph333"]
	page_type = 'about-contact'

	try:
		return render_template("general_statistics.html", paragraph=paragraph, page_type=page_type,collections=collections)
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
		print(names)		
	return '', 200

if __name__ == "__main__":
	try:
		app.run(debug=True,host='127.0.0.1',port=8000)
	except Exception as e:
		print(e.__cause__)
		subprocess.call("sudo lsof -i:8000",shell=True)

