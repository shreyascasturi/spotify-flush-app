from flask import Flask
app = Flask(__name__)

@app.route('/')
def display():
    return "looks like it works!"

if __name__=='__main__':
    app.run()
