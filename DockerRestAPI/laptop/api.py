# Laptop Service
from flask import Flask, Flask, jsonify, redirect, url_for, request, render_template, abort
from flask_restful import Resource, Api
from pymongo import MongoClient
import pymongo
from psw import hash_password, verify_password
from createToken import generate_auth_token, verify_auth_token

# Instantiate the app
app = Flask(__name__)
api = Api(app)

app.config['SECRET_KEY'] = 'the quick brown fox jumps over the lazy dog'

# ACCESS DATABASE
client = MongoClient('db', 27017)
db = client.tododb # gets database
db2 = client.users # inserts another db doc called users

#db2.users.delete_many({})

@app.route('/api/register')
def register(): # takes you to the sign up page
	_items = db2.users.find()
	items = [item for item in _items]
	app.logger.debug(items)

	app.logger.debug("On Register Page")
	return render_template('register.html')

@app.route('/user', methods=['POST'])
def user():
	app.logger.debug("Creating User...")
	username = request.form['username']
	password = request.form['password']
	
	app.logger.debug("UserName=")
	app.logger.debug(username)
	app.logger.debug("Password=")
	app.logger.debug(password)

	if username is None or password is None:
		app.logger.debug("ENTER BOTH A USERNAME AND A PASSWORD")
		return render_template("400.html"), 400
	
	user = db2.users.find_one( { 'username': username })
	print("USER IS" + str(user))
	if user != None:
		app.logger.debug("USER ALREADY EXISTS!")
		return render_template("401.html"), 401
		

	hashed_pass = hash_password(password)

	user = { 'username': username, 'password': hashed_pass }
	
	app.logger.debug("User Entry =")
	app.logger.debug(user)

	db2.users.insert_one(user)
	app.logger.debug("DB CONTENTS:")
	_items = db2.users.find()
	items = [item for item in _items]
	app.logger.debug(items)

	user = db2.users.find_one({ 'username': username, 'password': hashed_pass })
	user_id = user['_id']
	result = { 'username': username, 'password': hashed_pass, '_id': str(user_id) }
	
	return jsonify(result=result), 201

	#return render_template("success.html"), 201

@app.route('/api/token')
def login(): # takes you to the sign up page
	return render_template('login.html')

@app.route('/makeToken', methods=['POST'])
def makeToken():
	app.logger.debug("MAKING TOKEN")	
	# get username and password
	username = request.form['username']
	password = request.form['password']
	
	app.logger.debug("UserName: " + str(username))
	app.logger.debug("Password: " + str(password))

	if username is None or password is None:
		app.logger.debug("ENTER BOTH A USERNAME AND A PASSWORD")
		return render_template("400.html"), 400

	# check to make sure user is in database
	if db2.users.find_one( { 'username': username } ) == None:
		app.logger.debug("USER IS NOT IN THE DATABASE")
		return render_template("401.html"), 401

	else:
		user = db2.users.find_one( { 'username': username })
		app.logger.debug("User Exists! " + str(user))
		hashed_pass = user['password']
		passVerify = verify_password(password,hashed_pass)
		app.logger.debug("Password Verified? " + str(passVerify))
		if passVerify == False:
			return render_template("401.html"), 401
		else:
			user_id = user['_id']
			id = {'id' : str(user_id)}
			app.logger.debug("USER ID " + str(id))
			token = generate_auth_token(app.config['SECRET_KEY'],id)
			
			app.logger.debug("Token: " + str(token))
			
			result = { 'token': str(token) , 'duration': 30 }
			return jsonify(result=result), 201

class all(Resource): # USE 5001 TO ACCESS!
	def get(self):
		app.logger.debug("CHECKING RESOURCE")
		token = request.args.get('token') 
		app.logger.debug("TOKEN " + str(token))

		if token == None: # makes sure a token was entered
			app.logger.debug("TOKEN NOT FOUND ")
			return render_template("401.html"), 401

		verified = verify_auth_token(token,app.config['SECRET_KEY'])
		app.logger.debug("VERIFIED IS " + str(verified))
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:	
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort([('open_times',pymongo.ASCENDING), ('close_times',pymongo.ASCENDING)]).limit(top)
			li_data = [item for item in _items]

			app.logger.debug("DATA IS")
			app.logger.debug(li_data)
		
			dic = {}
			otimes = []
			ctimes = []
		
			for item in li_data:
				otimes.append(item['open_times'])
				ctimes.append(item['close_times'])
			
			app.logger.debug("OPEN IS")
			app.logger.debug(otimes)
			app.logger.debug("CLOSE IS")
			app.logger.debug(ctimes)
		
			dic['open_times'] = otimes
			dic['close_times'] = ctimes
			
			app.logger.debug("DICTIONARY")
			app.logger.debug(dic)
		
			return dic
		
api.add_resource(all, '/listAll')

class all_json(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort([('open_times',pymongo.ASCENDING), ('close_times',pymongo.ASCENDING)]).limit(top)
			li_data = [item for item in _items]		
			dic = {}
			otimes = []
			ctimes = []		
			for item in li_data:
				otimes.append(item['open_times'])
				ctimes.append(item['close_times'])		
			dic['open_times'] = otimes
			dic['close_times'] = ctimes
			return dic

api.add_resource(all_json, '/listAll/json')

class all_csv(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort([('open_times',pymongo.ASCENDING), ('close_times',pymongo.ASCENDING)]).limit(top)
			li_data = [item for item in _items]
		
			csv_string = ""
			for item in li_data:
				csv_string += item['open_times'] + ", "
				csv_string += item['close_times'] + ", "
			return csv_string

api.add_resource(all_csv, '/listAll/csv')

class open_json(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort('open_times', pymongo.ASCENDING).limit(top)
			li_data = [item for item in _items]
		
			app.logger.debug("MADE IT HERE")
			dic = {}
			otimes = []	
			for item in li_data:
				otimes.append(item['open_times'])		
			dic['open_times'] = otimes
			return dic

api.add_resource(open_json, '/listOpenOnly/json')

class open_csv(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort('open_times', pymongo.ASCENDING).limit(top)
			li_data = [item for item in _items]
		
			csv_string = ""
			for item in li_data:
				csv_string += item['open_times'] + ", "
			return csv_string

api.add_resource(open_csv, '/listOpenOnly/csv')

class close_json(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort('close_times', pymongo.ASCENDING).limit(top)
			li_data = [item for item in _items]
		
			dic = {}
			ctimes = []		
			for item in li_data:
				ctimes.append(item['close_times'])		
				dic['close_times'] = ctimes
			return dic

api.add_resource(close_json, '/listCloseOnly/json')

class close_csv(Resource):
	def get(self):
		token = request.args.get('token') 
		if token == None: # makes sure a token was entered
			return render_template("401.html"), 401

		verified = verify_auth_token(token,app.config['SECRET_KEY'])
		if verified == False:
			return render_template("401.html"), 401

		if verified == True:
			
			num = request.args.get('top')
			if num == None:
				top = 50
			else:
				top = int(num)
			_items = db.tododb.find().sort('close_times', pymongo.ASCENDING).limit(top)
			li_data = [item for item in _items]
		
			csv_string = ""
			for item in li_data:
				csv_string += item['close_times'] + ", "
			return csv_string

api.add_resource(close_csv, '/listCloseOnly/csv')

# Run the application
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)
