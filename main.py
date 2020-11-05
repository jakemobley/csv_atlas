from flask import Flask, render_template
k
app = Flask(__name__)

@app.route('/')
def index():
	return render_template('index.html')

if __name__ == '__main__':
	app.run(debug=True)