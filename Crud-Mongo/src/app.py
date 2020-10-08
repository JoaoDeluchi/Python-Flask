from flask import Flask, request
from flask_pymongo import PyMongo
from werkzeug.security import generate_password_hash, check_password_hash

app = Flask(__name__)
app.config["MONGO_URI"] = 'mongodb://localhost/pymongodb'
database = PyMongo(app)


@app.route('/users', methods=['POST'])
def create_user():
    data = request.get_json()
    username = data['username']
    age = data['age']
    email = data['email']
    password = data['password']
    if username and age and email and password:
        hashed_password = generate_password_hash(password)
        id = database.db.users.insert({
                'username': username,
                'age': age,
                'email': email,
                'password': hashed_password,
                })
        response = {
            'id': str(id),
            'username': username,
            'age': age,
            'email': email,
            'password': hashed_password,    
        }
        return response
    else:
        return {'message': 'error'}


if __name__ == "__main__":
    app.run(debug=True)
