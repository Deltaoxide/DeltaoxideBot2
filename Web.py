from flask import Flask, request
import json

app = Flask(__name__)

@app.route('/')
def foo():
   return "HelloWorld"

if __name__ == '__main__':
   app.run()
