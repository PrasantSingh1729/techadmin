from flask import Flask, jsonify, request , render_template, redirect, url_for, session, flash
from Forms.forms import Login_form, Change_password_form, Schedule_movie_form, Delete_schedule_form, Filter_movie_form
from flask_mysqldb import MySQL
from functools import wraps

app = Flask(__name__) 

app.config['SECRET_KEY'] = "secret_key" 
app.config['MYSQL_HOST']= "localhost" 
app.config['MYSQL_USER'] = "root" 
app.config['MYSQL_PASSWORD'] = "" 
app.config['MYSQL_DB'] = "Movie_Booking" 
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql=MySQL(app)

#check if user logged in
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('techadmin_login'))
	return wrap

def validate_techadmin_login(username, password):
	connection = mysql.connection
	cursor = connection.cursor()
	try:
		cursor.execute("SELECT user_name, password, role FROM user where email_address=%s and role=%s",(username,'tech_admin'))
		data = cursor.fetchone()
		print(data)
		if not data:
			return 1
		elif data['password']!=password:
			return 2
		
		return data['user_name']
	
	finally:
		cursor.close()

def get_theater_names():
	connection = mysql.connection
	cursor = connection.cursor()
	try:
		cursor.execute("SELECT theater_name FROM theater")
		data = cursor.fetchall()
		data = [entry['theater_name'] for entry in data]
		return data
	finally:
		cursor.close()
	
def get_movie_names():
	connection = mysql.connection
	cursor = connection.cursor()
	try:
		cursor.execute("SELECT movie_name FROM movie")
		data = cursor.fetchall()
		data = [entry['movie_name'] for entry in data]
		return data
	finally:
		cursor.close()

def get_schedule_list_filter(movie_name, theater_name, start_date):
	connection = mysql.connection
	cursor = connection.cursor()
	try:
		query = "SELECT * FROM schedule WHERE 1=1"
		params = []
		if movie_name:
			query += " AND movie_name=%s"
			params.append(movie_name)
		if theater_name:
			query += " AND theater_name=%s"
			params.append(theater_name)
		if start_date:
			query += " AND start_date=%s"
			params.append(start_date)

		cursor.execute(query,params)
		data = cursor.fetchall()
		return data
	finally:
		cursor.close()

@app.route("/techadmin/logout")
def techadmin_logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('techadmin_login'))

@app.route('/techadmin/login', methods=['GET','POST']) 
def techadmin_login():
	login_form = Login_form()
	connection = mysql.connection
	cursor = connection.cursor()
	try:
		if login_form.validate_on_submit():
			username = login_form.username.data
			password = login_form.password.data
			print(username,password)
			validation = validate_techadmin_login(username,password)
			if validation==1:
				flash("You are not authorized to login!")
			elif validation==2:
				flash("Please enter the correct password!")

			if validation==1 or validation==2:
				return render_template('login.html', form=login_form)
			
			session['logged_in'] = True
			session['user_name'] = validation
			return redirect(url_for('techadmin_home'))
		
		if 'logged_in' in session:
			return redirect(url_for('techadmin_home'))
		
		return render_template('login.html', form=login_form)
	finally:
		cursor.close()

@app.route('/techadmin/changepassword', methods=['GET','POST']) 
def techadmin_change_password():
	change_password_form = Change_password_form()
	if change_password_form.validate_on_submit():
		# check if user exist in database with role as tech admin
		# Complete the code
		return redirect(url_for('techadmin_login'))
	return render_template('change_password.html', form=change_password_form)

@app.route('/techadmin/home', methods=['GET'])
@is_logged_in
def techadmin_home(): 
	return render_template('home.html')

@app.route('/techadmin/schedule', methods=['GET'])
@is_logged_in
def schedule_movie():
	form = Schedule_movie_form()
	form.movie_name.choices = get_movie_names()
	form.theater_name.choices = get_theater_names()
	return render_template('schedule_movie.html', form=form)

@app.route('/techadmin/delete', methods=['GET'])
@is_logged_in
def delete_schedule():
	form = Delete_schedule_form()
	form.movie_name.choices = get_movie_names()
	form.theater_name.choices = get_theater_names()
	return render_template('delete_schedule.html', form=form)

@app.route('/techadmin/view', methods=['GET','POST'])
@is_logged_in
def techadmin_view_schedule():
	form = Filter_movie_form()
	form.movie_name.choices = [""] + get_movie_names()
	form.theater_name.choices = [""] + get_theater_names()
	if form.validate_on_submit():
		movie_name = form.movie_name.data
		theater_name = form.theater_name.data
		start_date = form.start_date.data
		movie_list = get_schedule_list_filter(movie_name, theater_name, start_date)
	else:
		movie_list = get_schedule_list_filter(None,None,None)
	return render_template('view_schedule.html', form=form, movie_list=movie_list)

if __name__ == '__main__': 
	app.run(debug=True) 
