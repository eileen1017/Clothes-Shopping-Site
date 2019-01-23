from flask import Flask, json, request, jsonify, session
from flask_mysqldb import MySQL
from flask_cors import CORS
from flask_bcrypt import Bcrypt
from flask_jwt_extended import JWTManager
from flask_jwt_extended import (create_access_token)
import json, ast

app = Flask(__name__)
app.secret_key = 'secret'

app.config['MYSQL_USER'] = 'lilin1'
app.config['MYSQL_PASSWORD'] = 'lilin1017'
app.config['MYSQL_DB'] = 'Shopping2'
app.config['MYSQL_HOST'] = 'localhost'
app.config['MYSQL_CURSORCLASS'] = 'DictCursor'
app.config['JWT_SECRET_KEY'] = 'secret'


mysql = MySQL(app)
bcrypt = Bcrypt(app)
jwt = JWTManager(app)
CORS(app)



@app.route('/users/register', methods=['POST'])
def register():
	cur = mysql.connection.cursor()
	firstname = request.get_json()['firstname']
	lastname = request.get_json()['lastname']
	email = request.get_json()['email']
	password = bcrypt.generate_password_hash(request.get_json()['password']).decode('utf-8')
	response = cur.execute("INSERT INTO users (firstname,lastname, email, password) VALUES ('" +
		str(firstname) + "','" +
		str(lastname) + "','" +
		str(email) + "','" +
		str(password) + "')")

	mysql.connection.commit()

	if response > 0: 
		result = jsonify({
			"firstname": firstname,
			"lastname": lastname,
			"email": email,
			"password": password
		})
	else:
		result = jsonify({"error": "Please change another email."})

	return result

@app.route('/users/login', methods=['POST'])
def login():
	cur = mysql.connection.cursor()
	email = request.get_json()['email']
	password = request.get_json()['password']
	result = ""
	cur.execute("SELECT * FROM users where email = '" + str(email) + "'")
	rv = cur.fetchone()
	user_match = check_user_exits(email)
	if user_match == True:
		if bcrypt.check_password_hash(rv['password'],password):
			access_token = create_access_token(identity = {'userid':rv['userid'],'firstname': rv['firstname'], 'lastname':rv['lastname'], 'email':rv['email']})
			session['token'] = access_token
			session['userid'] = rv['userid']
			print(session['userid'])
			result = jsonify({"token": access_token})
		else:
			result = jsonify({"error": "Invalid username and password"})
	else:
		result = jsonify({"error": "Please check your email."})
	return result

@app.route('/users/changePassword', methods=['POST'])
def changePassword():
	cur = mysql.connection.cursor()
	email = request.get_json()['email']
	email = ast.literal_eval(json.dumps(email))
	print("this is email in changePassword: ", email)
	userid = session.get('userid')
	password = request.get_json()['password']
	newPassword = request.get_json()['newPassword']
	newPassword = bcrypt.generate_password_hash(newPassword).decode('utf-8')
	cur.execute("SELECT * FROM users where email = '" + str(email) + "' and userid = '" + str(userid) + "'")
	rv = cur.fetchone()

	if bcrypt.check_password_hash(rv['password'],password):
		cur2 = mysql.connection.cursor()
		response = cur2.execute("UPDATE users SET password = '" + str(newPassword) + "' WHERE email = '" + str(email) + "' and userid = '" + str(userid) + "'")
		mysql.connection.commit()
		if response > 0:
			result = {"message": "You have successfully updated your password. Please log in again."}
	else:
		result = {"message": "Error: Please check your inputs."}
	return jsonify({"result": result})





@app.route('/users/carts', methods=['GET'])
def cart():
	cur = mysql.connection.cursor()
	userid = session.get('userid')
	cur.execute("SELECT i.item_id, i.itemname, i.item_picture, i.item_type, i.item_price, c.quantity, c.userid FROM (items i) JOIN cart c ON i.item_id = c.itemid WHERE c.userid ='" + str(userid) + "'")
	return jsonify(items=[{
	 	"itemid": rv['item_id'],
	 	"userid": rv['userid'],
	 	"quantity": rv['quantity'],
	 	"itemname": rv['itemname'],
	 	"itempicture": rv['item_picture'],
	 	"itemtype": rv['item_type'],
	 	"itemprice": rv['item_price']
	 } for rv in cur.fetchall()])


@app.route('/users/cart/<id>',methods=['PUT'])
def update_cart(id):
	cur = mysql.connection.cursor()
	userid = session.get('userid')
	quantity = request.get_json()['quantity']
	response = cur.execute("UPDATE cart SET quantity = '" + str(quantity) + "' WHERE itemid = " + str(id) + " and userid = " + str(userid))
	mysql.connection.commit()
	if response > 0: 
		result = {"quantity": quantity}
	else: 
		result = {"message": "not success"}
	return jsonify({"result": result})


@app.route('/users/cart/<id>',methods=['DELETE'])
def delete_cart(id):
	cur = mysql.connection.cursor()
	userid = session.get('userid')
	response = cur.execute("DELETE FROM cart where itemid = " + str(id) + " and userid = " + str(userid))
	mysql.connection.commit()

	if response > 0: 
		result = {"message": "record deleted"}
	else: 
		result = {"message": "no record found"}
	return jsonify({"result": result})



@app.route('/users/wishlists', methods=['GET'])
def wishlist():
	cur = mysql.connection.cursor()
	userid = session.get('userid')
	cur.execute("SELECT i.item_id, i.itemname, i.item_picture, i.item_type, i.item_price, w.userid FROM (items i) JOIN wishlist w ON i.item_id = w.itemid WHERE w.userid ='" + str(userid) + "'")
	return jsonify(items=[{
	 	"itemid": rv['item_id'],
	 	"userid": rv['userid'],
	 	"itemname": rv['itemname'],
	 	"itempicture": rv['item_picture'],
	 	"itemtype": rv['item_type'],
	 	"itemprice": rv['item_price']
	 } for rv in cur.fetchall()])

@app.route('/users/friend', methods=['GET'])
def friendlist():
	cur = mysql.connection.cursor()
	userid = session.get('userid')
	cur.execute("SELECT userid, friend_email FROM friends WHERE userid ='" + str(userid) + "'")
	return jsonify(items=[{
	 	"userid": rv['userid'],
	 	"friendemail": rv['friend_email']
	 } for rv in cur.fetchall()])



@app.route('/users/comments', methods=['POST'])
def commentlist():
	itemid = request.get_json()['itemid']
	cur = mysql.connection.cursor()
	cur.execute("SELECT u.firstname, u.lastname, u.email, c.commenttext, c.commentid FROM (comments c) JOIN users u ON c.userid = u.userid WHERE c.itemid ='" + str(itemid) + "'")
	return jsonify(items=[{
	 	"userfirstname": rv['firstname'],
	 	"userlastname": rv['lastname'],
	 	"useremail": rv['email'],
	 	"commenttext": rv['commenttext'],
	 	"commentid": rv['commentid']
	 } for rv in cur.fetchall()])

@app.route('/users/item', methods=['POST'])
def getItemById():
	itemid = request.get_json()['itemid']
	cur = mysql.connection.cursor()
	print("this is itemid in getItemById: ",itemid)
	cur.execute("SELECT * FROM items WHERE item_id ='" + str(itemid) + "'")
	rv = cur.fetchone()
	return jsonify(items={
        "itemid": rv['item_id'],
        "itemname": rv['itemname'],
        "itempicture": rv['item_picture'],
        "itemtype": rv['item_type'],
        "itemprice": rv['item_price']
    })

@app.route('/users/friendPurchased', methods=['POST'])
def viewFriendPurchased():
	friendemail = request.get_json()['friendemail']
	friendemail = ast.literal_eval(json.dumps(friendemail))
	cur = mysql.connection.cursor()
	cur.execute("SELECT DISTINCT p.quantity, i.itemname, i.item_picture, i.item_type, i.item_price, i.item_id FROM items i, users u, purchased p WHERE u.userid = p.userid and p.itemid = i.item_id and u.email ='" + str(friendemail) + "'")
	return jsonify(items=[{
        "itemid": rv['item_id'],
        "itemname": rv['itemname'],
        "itempicture": rv['item_picture'],
        "itemtype": rv['item_type'],
        "itemprice": rv['item_price'],
        "quantity": rv['quantity']
    } for rv in cur.fetchall()])



@app.route('/users/wishlist/<id>',methods=['DELETE'])
def delete_wishlist(id):
	cur = mysql.connection.cursor()
	userid = session.get('userid')
	response = cur.execute("DELETE FROM wishlist where itemid = " + str(id) + " and userid = " + str(userid))
	mysql.connection.commit()

	if response > 0: 
		result = {"message": "record deleted"}
	else: 
		result = {"message": "no record found"}
	return jsonify({"result": result})

@app.route('/users/comment/<id>',methods=['DELETE'])
def delete_comment(id):
	cur = mysql.connection.cursor()
	userid = session.get('userid')
	response = cur.execute("DELETE FROM comments where commentid = " + str(id))
	mysql.connection.commit()

	if response > 0: 
		result = {"message": "record deleted"}
	else: 
		result = {"message": "no record found"}
	return jsonify({"result": result})


@app.route('/users/purchase', methods=['POST'])
def add_purchase():
	userid = session.get('userid')
	print(session.get('userid'))
	cur = mysql.connection.cursor()
	response = cur.execute("INSERT INTO purchased (itemid, userid, quantity) SELECT itemid, userid, quantity FROM cart WHERE userid = '" + str(userid) +"'")
	removeCartByID(userid)
	mysql.connection.commit()
	if response > 0:
		removeCartByID(userid)
		result = {"message": "You have successfully purchased these items."}
	else:
		result = {"message": "Some error occur!"}
	return jsonify({"result": result})



def removeCartByID(userid):
	cur = mysql.connection.cursor()
	response = cur.execute("DELETE FROM cart where userid = '" + str(userid)+ "'")
	mysql.connection.commit()
	if response > 0:
		result = {"message": "record deleted"}
	else: 
		result = {"message": "no record found"}
	return jsonify({"result": result})

@app.route('/users/friend/<id>',methods=['DELETE'])
def delete_friend(id):
	cur = mysql.connection.cursor()
	id = ast.literal_eval(json.dumps(id))
	print("this is delete friend: ",id)
	userid = session.get('userid')
	response = cur.execute("DELETE FROM friends where friend_email = '" + str(id) + "' and userid = '" + str(userid)+ "'")
	mysql.connection.commit()

	if response > 0: 
		result = {"message": "record deleted"}
	else: 
		result = {"message": "no record found"}
	return jsonify({"result": result})


@app.route('/users/cart', methods=['POST'])
def add_cart():
	itemid = request.get_json()['itemid']
	userid = session.get('userid')
	print(session.get('userid'))
	match = check_exists(itemid, userid)
	if match == False:
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO cart (itemid, userid, quantity) VALUES ('" +
		str(itemid) + "','" +
		str(userid) + "','" +
		str(1) + "')")
		mysql.connection.commit()
		result = {"message": "You have successfully added this item to your cart."}
	else:
		result = {"message": "The item is already in your cart, check it in your cart."}
	return jsonify({"result": result})

@app.route('/users/friend', methods=['POST'])
def add_friend():
	friendemail = request.get_json()['friendemail']
	friendemail = ast.literal_eval(json.dumps(friendemail))
	userid = session.get('userid')
	print(session.get('userid'))
	print("friendemail in add_friend ", friendemail)
	match_user = check_user_exits(friendemail)
	match_friend = check_friend_exists(friendemail, userid)
	print(match_user)
	print(match_friend)
	if match_user == True:
		if match_friend == False:
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO friends (userid, friend_email) VALUES ('" +
			str(userid) + "','" +
			str(friendemail) + "')")
			mysql.connection.commit()
			result = {"message": "You have successfully added " + friendemail + " ."}
		else:
			result = {"message": "You are already friends with each other."}
	else:
		result = {"message": "User does not exist."}
	return jsonify({"result": result})


@app.route('/users/comment', methods=['POST'])
def add_comment():
	commenttext = request.get_json()['commenttext']
	itemid = request.get_json()['itemid']
	print("this is itemid in add_comment ",itemid)
	commenttext = ast.literal_eval(json.dumps(commenttext))
	itemid = ast.literal_eval(json.dumps(itemid))
	userid = session.get('userid')
	print(session.get('userid'))
	print("itemid in add_comment ", itemid)
	print("commenttext in add_comment ", commenttext)
	match_comment = check_comment_exits(itemid, userid)
	match_purchase = check_purchase_exits(itemid, userid)
	if match_purchase == True:
		if match_comment == False:
			cur = mysql.connection.cursor()
			cur.execute("INSERT INTO comments (commenttext, userid, itemid) VALUES ('" +
			str(commenttext) + "','" +
			str(userid) + "','" +
			str(itemid) + "')")
			mysql.connection.commit()
			result = {"message": "You have successfully added your comment."}
		else:
			result = {"message": "You have already commented on this item."}
	else:
		result = {"message": "Please purchase before commenting."}
	return jsonify({"result": result})


def check_purchase_exits(itemid, userid):
	cur = mysql.connection.cursor()
	print("this is userid ", userid)
	cur.execute("SELECT purchaseid FROM purchased where itemid = '" + str(itemid)+ "' and userid = '" + str(userid)+ "'")
	response = cur.fetchone()
	print(response)
	if response: 
		return True
	else: 
		return False


def check_comment_exits(itemid, userid):
	cur = mysql.connection.cursor()
	print("this is userid ", userid)
	cur.execute("SELECT commentid FROM comments where itemid = '" + str(itemid)+ "' and userid = '" + str(userid)+ "'")
	response = cur.fetchone()
	print(response)
	if response: 
		return True
	else: 
		return False



def check_user_exits(friendemail):
	cur = mysql.connection.cursor()
	cur.execute("SELECT * FROM users where email = '" + str(friendemail) + "'")
	rv = cur.fetchone()
	if rv: 
		return True
	else: 
		return False

def check_friend_exists(friendemail, userid):
	cur = mysql.connection.cursor()
	print("this is userid ", userid)
	print("this is friendemail ", friendemail)
	cur.execute("SELECT relationid FROM friends where friend_email = '" + str(friendemail)+ "' and userid = '" + str(userid)+ "'")
	response = cur.fetchone()
	print(response)
	if response: 
		return True
	else: 
		return False


@app.route('/users/wishlist', methods=['POST'])
def add_wishlist():
	itemid = request.get_json()['itemid']
	userid = session.get('userid')
	print(session.get('userid'))
	match = check_wishlist_exists(itemid, userid)
	if match == False:
		cur = mysql.connection.cursor()
		cur.execute("INSERT INTO wishlist (itemid, userid) VALUES ('" +
		str(itemid) + "','" +
		str(userid) + "')")
		mysql.connection.commit()
		result = {"message": "You have successfully added this item to your wishlist."}
	else:
		result = {"message": "The item is already in your wishlist, check it in your wishlist."}
	return jsonify({"result": result})


def check_wishlist_exists(itemid, userid):
	cur = mysql.connection.cursor()
	print("this is userid ", userid)
	cur.execute("SELECT wishid FROM wishlist where itemid = " + str(itemid)+ " and userid = " + str(userid))
	response = cur.fetchone()
	print(response)
	if response: 
		return True
	else: 
		return False


def check_exists(itemid, userid):
	cur = mysql.connection.cursor()
	print("this is userid ", userid)
	cur.execute("SELECT cartid FROM cart where itemid = " + str(itemid)+ " and userid = " + str(userid))
	response = cur.fetchone()
	print(response)
	if response: 
		return True
	else: 
		return False

@app.route('/users/womenitems', methods=['GET'])
def displayWomenItems():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items WHERE item_type = 'f'")
    return jsonify(items=[{
        "itemid": rv['item_id'],
        "itemname": rv['itemname'],
        "itempicture": rv['item_picture'],
        "itemtype": rv['item_type'],
        "itemprice": rv['item_price']
    } for rv in cur.fetchall()])


@app.route('/users/menitems', methods=['GET'])
def displayMenItems():
    cur = mysql.connection.cursor()
    cur.execute("SELECT * FROM items WHERE item_type = 'm'")
    return jsonify(items=[{
        "itemid": rv['item_id'],
        "itemname": rv['itemname'],
        "itempicture": rv['item_picture'],
        "itemtype": rv['item_type'],
        "itemprice": rv['item_price']
    } for rv in cur.fetchall()])








if __name__ == '__main__':
    app.run(debug=True)