
from flask import render_template, redirect, url_for, flash, request, Flask, jsonify

app = Flask(__name__)

@app.route('/')
@app.route('/index')
def index():
    return render_template('index.html')

# Run app #
if __name__ == '__main__':
    app.run(host='0.0.0.0', port=80, debug=True)