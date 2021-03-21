from flask import Flask, redirect, url_for, render_template, request, jsonify
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import secure_filename
from base64 import b64encode

#create instance of flask web application
app = Flask(__name__)

app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:admin@localhost/imagedetails'

app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

db = SQLAlchemy(app)

class Imagedetails(db.Model):
	_id = db.Column("id",db.Integer, primary_key = True)
	category = db.Column(db.String(30))
	image = db.Column(db.LargeBinary)

@app.route('/')
def gallerypage():
	result = Imagedetails.query.all()
	return render_template('gallerypage.html', final_list = final_result(result))

@app.route("/uploadpage")
def uploadpage():
	return render_template("uploadpage.html")

@app.route("/upload",methods=['POST'])
def upload_file():
	#This method is to upload the file and category to the db. 
	if request.method == 'POST':
		image = request.files['file']
		category = request.form['category']
		imgdetails = Imagedetails(category = category, image = image.read())
		db.session.add(imgdetails)
		db.session.commit()
		return redirect(url_for("gallerypage"))

@app.route("/filter/<category>")
def filter(category):
	#This method is to filter data based on selected category 
	if category == "clear":
		result = Imagedetails.query.all()
	else:
		result = Imagedetails.query.filter(Imagedetails.category == category).all()
	return render_template('gallerypage.html', final_list = final_result(result))

def final_result(result):
	#This method is to loop through the result, to decode image file and form final result list 
	final_list = []
	for i in result:
		image = b64encode(i.image).decode("utf-8")
		category = i.category
		final_list.append({'image':image, 'category':category})
	return reversed(final_list)

#to run web site
if __name__ == "__main__":
	db.create_all()
	app.run(debug = True)

