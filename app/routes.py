from app import app,jwt,connection_cursor,connection,CREATE_IKEA_TABLE,CREATE_USERS_TABLE,INSERT_IKEA
from flask import jsonify, request, make_response
from flask_bcrypt import generate_password_hash, check_password_hash
from flask_jwt_extended import create_access_token, jwt_required, get_jwt_identity
from datetime import timedelta

@app.post("/api/ikea")
def create_table_ikea():
    with connection.cursor() as cursor:
        cursor.execute(CREATE_IKEA_TABLE)
        cursor.execute(INSERT_IKEA)
        connection.commit()
        return make_response(jsonify({"message": "Users table created"}), 201)

@app.post("/api/users")
def create_table_ikea():
    with connection.cursor() as cursor:
        cursor.execute(CREATE_USERS_TABLE)
        connection.commit()
        return make_response(jsonify({"message": "Users table created"}), 201)

# register
@app.route("/api/v1/register", methods=["POST"])
def register():
    username = request.json.get('username', None)
    password = request.json.get('password', None)

    connection_cursor.execute("select * from users where username=%s", (username,))
    user = connection_cursor.fetchone()
    if user:
        return jsonify({'message': 'user already exists'}), 409

    hashed_password = generate_password_hash(password).decode('utf-8')

    connection_cursor.execute("insert into users (username, password) values (%s,%s)", (username, hashed_password))
    connection.commit()

    return jsonify({'message': 'registered successfully'}), 200

# login
@app.route("/api/v1/login", methods=["POST"])
def login():
    autho = request.authorization

    if not autho or not autho.username or not autho.password:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    connection_cursor.execute("select * from users where username=%s", (autho.username,))
    user = connection_cursor.fetchone()
    if not user:
        return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})

    if check_password_hash(user[1], autho.password):
        access_token = create_access_token(identity=user[0], expires_delta=timedelta(seconds=30))
        return jsonify({'token': access_token}), 200
    return make_response('could not verify', 401, {'WWW.Authentication': 'Basic realm: "login required"'})


# get all ikea
@app.route("/api/v1/ikea", methods=["GET"])
@jwt_required()
def read():
    connection_cursor.execute("select * from ikea")
    return jsonify(connection_cursor.fetchall())

@app.route("/api/v1/ikea", methods=["POST"])
@jwt_required()
def create():
    data = request.get_json()
    connection_cursor.execute("insert into ikea (id,item_id,name,category,price,old_price,sellable_online,link,other_colors,short_description,designer,depth,height,width) values (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (data['id'], data['item_id'], data['name'], data['category'], data['price'], data['old_price'], data['sellable_online'], data['link'], data['other_colors'], data['short_description'], data['designer'], data['depth'], data['height'], data['width']))
    connection.commit()
    return jsonify({'ikea': data}),200

@app.route("/api/v1/ikea", methods=["PUT"])
@jwt_required()
def update():
    data = request.get_json()
    connection_cursor.execute("update ikea set name=%s, category=%s, price=%s, old_price=%s, sellable_online=%s, link=%s, other_colors=%s, short_description=%s, designer=%s, depth=%s, height=%s, width=%s where id=%s", (data['name'], data['category'], data['price'], data['old_price'], data['sellable_online'], data['link'], data['other_colors'], data['short_description'], data['designer'], data['depth'], data['height'], data['width'], data['id']))
    connection.commit()
    return jsonify({'ikea': data}),200

@app.route("/api/v1/ikea", methods=["DELETE"])
@jwt_required()
def delete():
    data = request.get_json()
    connection_cursor.execute("delete from ikea where id=%s", (data['id'],))
    connection.commit()
    return jsonify({'ikea': data}),200