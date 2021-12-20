from flask import Flask,render_template, request , jsonify
from flask_cors import CORS,cross_origin
import pickle

'''
import os
import importlib
import ctypes
import _thread
import win32api

# Load the DLL manually to ensure its handler gets
# set before our handler.
#basepath = imp.util.find_loader('numpy')[1]

toolbox_specs = importlib.util.find_spec("numpy")[1]
toolbox = importlib.util.module_from_spec(toolbox_specs)
toolbox_specs.loader.exec_module(toolbox)


ctypes.CDLL(os.path.join(toolbox, 'core', 'libmmd.dll'))
ctypes.CDLL(os.path.join(toolbox, 'core', 'libifcoremd.dll'))

# Now set our handler for CTRL_C_EVENT. Other control event
# types will chain to the next handler.
def handler(dwCtrlType, hook_sigint=thread.interrupt_main):
	if dwCtrlType == 0: # CTRL_C_EVENT
		hook_sigint()
		return 1 # don't chain to the next handler
	return 0 # chain to the next handler

win32api.SetConsoleCtrlHandler(handler, 1)

'''



app = Flask(__name__)

@app.route('/',methods = ['GET'])
@cross_origin()
def homePage():
	return render_template("index.html")

@app.route('/predict',methods = ['POST','GET'])
@cross_origin()

def index():
	if request.method == 'POST':
		try:
			is_Pclass = (request.form['Pclass'])
			if (is_Pclass == 1):
				Pclass = 1
			elif (is_Pclass == 2):
				Pclass = 2
			else:
				Pclass = 3

			
			age  = float(request.form['Age'])
			SibSp  = float(request.form['SibSp'])
			Parch  = float(request.form['Parch'])
			Fare  = float(request.form['Fare'])

			is_male = (request.form['male'])
			if (is_male == 'yes'):
				male = 1
			else:
				male = 0
			


			#load the model
			filename_2  = 'modelForPrediction.sav'
			loaded_model = pickle.load(open(filename_2, 'rb')) #loading the model file from the storage

			#make predictions on the test set
			prediction = loaded_model.predict([[Pclass,age,SibSp,Parch,Fare,male]])
			print('\nprediction is', prediction[0])
			if prediction[0] == 0:
				result = 'not survived'
			else:
				result = 'survived'
			#Showing the prediction results in the UI
			return render_template('results.html',prediction=result)
		except Exception as e:
			print('The exception message is :',e)
			return'something is wrong'
	else:
		return render_template('index.html')

if __name__ == "__main__":
	app.run(debug = True)