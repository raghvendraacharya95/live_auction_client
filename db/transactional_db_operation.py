from transactional_db import DB
from db_queries import *
global_server = "localhost"
import json
from datetime import datetime,timedelta

def create_meta_data_user(signup_data):
	user_name = "{}{}{}".format(str(signup_data["firstname"])," ",str(signup_data["lastname"]))
	email_id = str(signup_data["email"])
	password = str(signup_data["passwd"])
	meta_data = {"user_name" : user_name,
	"email_id" : email_id,
	"password" : password}
	return meta_data

def user_signup(signup_data):
	db = DB(global_server)
	##Create Meta Data
	meta = create_meta_data_user(signup_data)
	# user_name,email_id,mobile,password
	singup_res = {"is_success":False}
	db.execute_query(ADD_NEW_USER,params=(meta["user_name"],meta["email_id"],"",meta["password"]),execute_query=True,commit=True,return_result=True,return_id=True)
	validation_res = validate_user(meta["email_id"],meta["password"])
	if validation_res["is_validate"] == True:
		singup_res["is_success"] = True
		singup_res["user_name"] = validation_res["user_name"]
		return singup_res
	return singup_res

def validate_user(email_id,user_password):
	##validate User
	db = DB(global_server)
	validation_response  = dict()
	is_validate = False
	u_name = None
	validation_data = db.execute_query(VALIDATE_USER,params=(email_id,user_password),execute_query=True,commit=True,return_result=True,return_id=True)
	if len(validation_data) > 0:
		if "USER_ID" in validation_data[0]:
			if validation_data[0]["USER_ID"] != None:
				is_validate = True
				u_name = validation_data[0]["USER_NAME"]
				user_id = validation_data[0]["USER_ID"]
				if u_name is not None:
					validation_response.update({"user_name":u_name})
					validation_response.update({"user_id":user_id})
	validation_response.update({"is_validate":is_validate})
	return validation_response 


def get_all_available_items_for_auction():
	db = db = DB(global_server)
	item_list = []
	all_items_list = db.execute_query(GET_ALL_AVAILABLE_ITEMS_FOR_AUCTION,execute_query=True,commit=True,return_result=True,return_id=True)
	for item in all_items_list:
		item_id = str(item["ITEM_ID"])
		item_name = str(item["ITEM_NAME"])
		item_list.append(" ".join([item_name,item_id]))
	return item_list

def update_bid_of_item(user_id,item_id,bid_price):
	db = DB(global_server)
	# 
	ist_now =  datetime.now().utcnow() +timedelta(hours=5,minutes=30)
	##Check bidder already biddding or not
	order_dtl = db.execute_query(CHECK_BIDDER_ORDER,params=(user_id,item_id),execute_query=True,commit=True,return_result=True,return_id=True)
	print order_dtl,"order_dtl"
	is_update = False
	if order_dtl:
		if order_dtl["ORDER_ID"] is not None:
			is_update = True
			db.execute_query(UPDATE_BID_PRICE_OF_ITEM,params=(bid_price,ist_now,user_id,item_id),execute_query=True,commit=True,return_result=True,return_id=True)
	if is_update == False:
		flag = db.execute_query(CREATE_A_LIVE_BID,params=(bid_price,ist_now,user_id,item_id),execute_query=True,commit=True,return_result=True,return_id=True)
		print flag
	return True

def get_user_name(user_id):
	db = DB(global_server)
	user_name = db.execute_query(UPDATE_BID_PRICE_OF_ITEM,params=(user_id),execute_query=True,commit=True,return_result=True,return_id=True)
	if user_name:
		return user_name[0]["user_name"]
	return None