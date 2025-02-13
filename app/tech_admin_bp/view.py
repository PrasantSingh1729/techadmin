from flask import Flask, jsonify, request , render_template, redirect, url_for, session, flash
from app.tech_admin_bp.form_impl import Login_form, Change_password_form, Schedule_movie_form, Delete_schedule_form, Filter_movie_form
from flask_mysqldb import MySQL
from functools import wraps
from app.extension import mysql
from flask import Blueprint

tech_admin_bp = Blueprint(
    'tech_admin_bp', 
    __name__,
	url_prefix='/tech_admin',
    template_folder='templates',
	static_folder='static'
)


######################################
#  Helper Functions                  #
######################################
def is_logged_in(f):
	@wraps(f)
	def wrap(*args,**kwargs):
		if 'logged_in' in session:
			return f(*args,**kwargs)
		else:
			flash('Unauthorized, Please Login','danger')
			return redirect(url_for('tech_admin_bp.techadmin_login'))
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

######################################
# Routes                             #
######################################
@tech_admin_bp.route("/logout")
@is_logged_in
def techadmin_logout():
	session.clear()
	flash('You are now logged out','success')
	return redirect(url_for('tech_admin_bp.techadmin_login'))

@tech_admin_bp.route('/login', methods=['GET','POST']) 
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
				return render_template('tech_admin_login.html', form=login_form)
			
			session['logged_in'] = True
			session['user_name'] = validation
			return redirect(url_for('tech_admin_bp.techadmin_home'))
		
		if 'logged_in' in session:
			return redirect(url_for('tech_admin_bp.techadmin_home'))
		
		return render_template('tech_admin_login.html', form=login_form)
	finally:
		cursor.close()

@tech_admin_bp.route('/changepassword', methods=['GET','POST']) 
def techadmin_change_password():
	form = Change_password_form()
	if form.validate_on_submit():
		username = form.username.data
		password = form.old_password.data
		new_password = form.new_password.data
		print(username,password)
		validation = validate_techadmin_login(username,password)
		if validation==1:
			flash("You are not authorized to login!")
		elif validation==2:
			flash("Please enter the correct password!")

		if validation==1 or validation==2:
			return render_template('tech_admin_change_password.html', form=form)
		
		connection = mysql.connection
		cursor = connection.cursor()
		cursor.execute("UPDATE user SET password=%s WHERE email_address=%s",(new_password,username))
		connection.commit()
		cursor.close()

		flash('Password changed successfully')
		return redirect(url_for('tech_admin_bp.techadmin_login'))
	return render_template('tech_admin_change_password.html', form=form)

@tech_admin_bp.route('/home', methods=['GET'])
@is_logged_in
def techadmin_home(): 
	return render_template('tech_admin_home.html')

@tech_admin_bp.route('/schedule', methods=['GET'])
@is_logged_in
def techadmin_schedule_movie():
	form = Schedule_movie_form()
	form.movie_name.choices = get_movie_names()
	form.theater_name.choices = get_theater_names()
	return render_template('tech_admin_schedule_movie.html', form=form)

@tech_admin_bp.route('/delete', methods=['GET','POST'])
@is_logged_in
def techadmin_delete_schedule():
	form = Delete_schedule_form()
	form.movie_name.choices = get_movie_names()
	form.theater_name.choices = get_theater_names()
	if form.validate_on_submit():
		movie_name = form.movie_name.data
		theater_name = form.theater_name.data
		start_date = form.start_date.data
		print(movie_name,theater_name,start_date)
		connection = mysql.connection
		cursor = connection.cursor()
		cursor.execute('SELECT schedule_id FROM schedule WHERE movie_name=%s AND theater_name=%s AND start_date=%s',(movie_name, theater_name, start_date))
		data = cursor.fetchone()
		if not data:
			flash("No data is available")
		else:
			cursor.execute('DELETE FROM schedule where schedule_id=%s',(data['schedule_id'],))
			connection.commit()
			flash("Deleted Successfully")
		cursor.close()
	return render_template('tech_admin_delete_schedule.html', form=form)

@tech_admin_bp.route('/view', methods=['GET','POST'])
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
	return render_template('tech_admin_view_schedule.html', form=form, movie_list=movie_list)
