from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def foo():
   return "HelloWorld"

if __name__ == '__main__':
   port = int(os.environ.get('PORT', 5000))
   app.run(host='0.0.0.0', port=port)
