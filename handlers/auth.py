# email_id = "admin-raghvendra"
# pwd = "1234"
global_key = "kunkka"

from functools import wraps
from flask import session
from live_auction_client.db import transactional_db_operation as tran_db

class Auth(object):
	"""docstring for Auth"""
	def __init__(self,request ,*args,**kwargs):
		self.request = request

	def __call__(self,func,*args,**kwargs):
		def authenticate(*args,**kwargs):
			# try:
			req = self.request
			##CallDb ToDo
			dict_ = {}
			if req.method == "POST":
				validation_res = tran_db.validate_user(str(req.form["email"]),str(req.form["passwd"]))
				if validation_res["is_validate"] == True:
					dict_["is_success"] = True
					dict_["u_name"] = validation_res["user_name"]
					dict_["user_id"] = validation_res["user_id"]
				else:
					dict_["is_success"] = False
			return func(**dict_)
			# except Exception as e:
				# raise e
		return authenticate

def SessionAuth(func):
	@wraps(func)
	def wrapper(*args,**kwargs):
		verified = {}
		if "key" in session and "user" in session:
			if session["key"] == global_key:
				verified["verified"] = True
				return func(*args,**verified)
		verified["verified"] = False
		return func(*args,**verified)
	return wrapper


class SingupUser(object):
	"""docstring for SingupUser"""
	def __init__(self,request, *arg,**kwargs):
		self.request = request

	def __call__(self,func,*args,**kwargs):
		def do_singup():
			dict_ = {"is_success":False}
			if self.request.method == "POST":
				singup_data = self.request.form
				#ToDo
				singup_res = tran_db.user_signup(singup_data)
				if singup_res["is_success"] == True:
					dict_["is_success"] = True
					dict_["u_name"] = singup_res["user_name"]
				else:
					dict_["is_success"] = False
				return func(**dict_)
			return func(**dict_)
		return do_singup