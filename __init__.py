from flask import Flask
from flask import request,render_template,url_for
import subprocess
import signal
import sys


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

	title = "Epic title"
	paragraph = [ "pargraph1","paragraph222","paragraph333"]

	try:
		return render_template("index.html", title = title, paragraph=paragraph)
	except Exception as e:
		return str(e)


@app.route('/about')
def aboutpage():

	title = "About this site"
	paragraph = [ "pargraph1","paragraph222","paragraph333"]
	page_type = 'about'

	try:
		return render_template("index_boot.html", title = title, paragraph=paragraph, page_type=page_type)
	except Exception as e:
		return str(e)

@app.route('/about/contact')
def aboutcontactpage():

	title = "About this site"
	paragraph = [ "pargraph1","paragraph222","paragraph333"]
	page_type = 'about'

	try:
		return render_template("index_boot.html", title = title, paragraph=paragraph, page_type=page_type)
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

if __name__ == "__main__":
	try:
		app.run(debug=True,host='127.0.0.1',port=8000)
	except Exception as e:
		print(e.__cause__)
		subprocess.call("sudo lsof -i:8000",shell=True)

