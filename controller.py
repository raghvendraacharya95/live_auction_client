from flask import Flask
from flask import render_template,request,make_response,abort,redirect,url_for,session
from live_auction_client.handlers.auth import Auth,SessionAuth,SingupUser,global_key
import os
from flask import jsonify
from live_auction_client.db import transactional_db_operation as tran_db
from flask_cors import CORS

app = Flask(__name__)
app.secret_key = os.urandom(24)
app.config['SESSION_TYPE'] = 'filesystem'
cors = CORS(app, resources={r"/api/*": {"origins": "*"}})

@app.route('/')
@SessionAuth
def index(*args,**kwargs):
	resp = '<a id="btn-login" href="/login" class="btn btn-success">Login  </a> <span> </span> <a id="btn-login" href="/signup" class="btn btn-success">Signup</a>'
	resp = make_response(resp)
	print session,"session...."
	print kwargs,"kwargs"
	if kwargs and "user" in session:
		if kwargs["verified"] == True:
			user_id = str(session["user_id"])
			print user_id
			r = """<span> Hi <a href="/user">"""+str(session["user"])+"""</a>!!</span>  <span> </span> <a href="/logout">Logout </a> <span> </span> <a href="/">Home</a> <span> <a href="/all_unsold_items">Get All Items On Auction </a></span> """
			# r = """<span> <a href="/user">"""+str(session["user_id"])+"""</a></span>  <span> </span> <a href="/logout">Logout </a> <span> </span> <a href="/">Home</a>"""
			resp = make_response(r)
	return resp
	

@app.route('/login', methods=['GET', 'POST'])
@Auth(request)
def login(*args,**kwargs):
	if kwargs:
		if kwargs["is_success"] == True:
			session["key"] = global_key
			session["user"] = str(kwargs["u_name"])
			session["user_id"] = str(kwargs["user_id"])
			return redirect(url_for('index'))
	return render_template('login.html')

@app.route('/logout', methods=['GET', 'POST'])
def logout(*args,**kwargs):
	session.pop("key",None)
	session.pop("user",None)
	return redirect(url_for('index'))

@app.route('/signup', methods=['GET', 'POST'])
# @SessionAuth
@SingupUser(request)
def signup(*args,**kwargs):
	if request.method == 'POST':
		if kwargs:
			if "verified" in kwargs:
				if kwargs["verified"] == True:
					return index()
			else:
				if "is_success" in kwargs:
					if kwargs["is_success"] == True:
						return login(*args,**kwargs)
				else:
					return index()
		return index()
	else:
		return render_template('signup.html')

@app.route('/user')
@SessionAuth
def show_user_profile(*args,**kwargs):
	if "verified" in kwargs:
		if kwargs["verified"] == True:
			r = "<span> Hello - <b>"+str(session["user"])+"""</b></span> <span> </span> <a href="/logout">Logout </a> <span> </span> <a href="/">Home</a>"""
			resp = make_response(r)
			return resp
	return logout()


@app.route('/all_unsold_items')
@SessionAuth
def show_item_list(*args,**kwargs):
	if "verified" in kwargs:
		if kwargs["verified"] == True:
			user_id = str(session["user_id"])
			print user_id
	return render_template('unsold_items.html')

@app.route('/all_unsold_items_list', methods=['GET', 'POST'])
def get_all_unsold_items(*args,**kwargs):
	all_item_list = tran_db.get_all_available_items_for_auction()
	return jsonify(all_item_list)

@app.route('/auction_room/<item_id>')
# @SessionAuth
def auction_room(item_id=None,*args,**kwargs):
	print "hello"
	user_id = str(session["user_id"])
	print user_id
	print item_id,"item_id"
	# item_id = item_id
		# item_id = request.args['item_id']
	return render_template('base_auction_room.html', user_id=user_id,item_id=item_id)
	# return render_template('base_auction_room.html', user_id=100,item_id=item_id)

@app.route('/bid', methods=['GET', 'POST'])
def update_price_of_a_item(*args,**kwargs):
	# print request.args
	user_id =  request.form["user_id"]
	item_id = request.form["item_id"]
	bid_price = request.form["price"]
	flag = tran_db.update_bid_of_item(user_id,item_id,bid_price)
	return jsonify({"is_success":flag})
