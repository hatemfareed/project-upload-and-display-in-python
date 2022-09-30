import os
from flask import  render_template, request, redirect ,flash
from werkzeug.utils import secure_filename
from flask import json
from flask_sqlalchemy import SQLAlchemy
from app import memcache , app , ALLOWED_EXTENSIONS



db = SQLAlchemy(app)

class Todo(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    key_img = db.Column(db.String(200), nullable=False , unique=True)
    file_path = db.Column(db.String(200), nullable=False )

    def __repr__(self):
        return '<Task %r>' % self.id

def allowed_file(filename):
	#print(filename.rsplit('.')[1])

	return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS
	
@app.route('/')
def upload_form():
	return render_template('upload.html' , title = "Upload Image")

@app.route('/', methods=['POST'])
def upload_image():
	file = request.files['file']
	key = request.form['key']
	file_path = os.path.join(app.config['UPLOAD_FOLDER'], secure_filename(file.filename))
	
	if file.filename == '':
		flash('No image selected for uploading')
		return redirect(request.url)
	if request.method == 'POST':
		if file and allowed_file(file.filename):
			new_task = Todo(key_img = key , file_path =file_path)	
			try:
				db.session.add(new_task)
				db.session.commit()	
				filename = secure_filename(file.filename)
				file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
				memcache[key] = os.path.join(app.config['UPLOAD_FOLDER'], filename)
				print('upload_image filename: ' + memcache[key])
				flash('Image successfully uploaded and displayed below')
				return render_template('upload.html', filename=filename)
			except:
				return 'There was an issue adding your img the key is already exist'
		else:
			flash('Allowed image types are -> png, jpg, jpeg, gif , PNG , JPG , JPEG , GIF')
			return redirect(request.url)
	# else:
	# 	tasks = Todo.query.order_by(Todo.key_img).all()
	# 	return render_template('img.html', tasks=tasks)	

@app.route('/display')
def display():
	return render_template("display.html")

@app.route('/display' ,methods=['POST' ,'GET'] )
def display_image():
	
	key = request.form['key']
	task = Todo.query.filter_by(key_img = key).first()
	if task is None:
		response = app.response_class(
		response=json.dumps("Unknown key"),
		status=400,
		mimetype='application/json'
	)
	else:
		response = app.response_class(
		response=json.dumps(key),
		status=200,
		mimetype='application/json' 
		)
		return render_template('index.html', filename=task.file_path)

	return response

@app.route('/img' )
def img():
	tasks = Todo.query.all()
	return render_template('img.html', tasks=tasks ,  titel = "Image")



@app.route('/delete/<int:id>')
def delete(id):
	key_to_delete = Todo.query.get_or_404(id)

	try:
		db.session.delete(key_to_delete)
		db.session.commit()
		os.remove(key_to_delete.file_path)
		return redirect('/img')
	
	except:
		return 'There was a problem deleting that KEY'

if __name__ == "__main__":
    app.run(debug=False)