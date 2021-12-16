
from flask import Flask

# Variables with underscores before and after them 
# are called magic methods in Python

app = Flask(__name__)

# define the starting point, also known as the root
@app.route('/')
def hello_world():
    return 'Hello world'
