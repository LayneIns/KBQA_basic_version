from flask import Flask, request
from main import generate_query

app = Flask(__name__)
@app.route('/')
def hello():
    user_q = request.args.get('user_q')
    print "user_q:", user_q
    return generate_query(user_q)

# @app.route('/')
# def hello_world():
#     return 'Hello World!'
# http://localhost:5000/?user_q=123456

if __name__ == '__main__':
    app.run(host='0.0.0.0')
