ADD_NEW_USER = """
INSERT INTO users(user_name,email_id,mobile,password)
VALUES(%s,%s,%s,%s);
"""

VALIDATE_USER = """
SELECT USER_ID,USER_NAME FROM users
WHERE email_id = %s and password = %s
"""

GET_ALL_AVAILABLE_ITEMS_FOR_AUCTION = """
SELECT item_id as ITEM_ID,
item_name as ITEM_NAME
FROM items where COALESCE(status,'') != 'S'
"""

UPDATE_BID_PRICE_OF_ITEM = """
UPDATE live_bidding set current_price = %s,last_bid_time = %s
where user_id = %s and item_id = %s
"""

GET_USERNAME = """
SELECT user_name FROM users  where user_id = %s
"""

CHECK_BIDDER_ORDER = """
SELECT order_id from live_bidding where user_id = %s and item_id = %s
"""

CREATE_A_LIVE_BID = """
INSERT INTO live_bidding(current_price,last_bid_time,user_id,item_id)
VALUES(%s,%s,%s,%s)
"""