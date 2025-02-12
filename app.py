from flask import Flask, jsonify, request , render_template, redirect, url_for
from Forms.forms import Login_form, Change_password_form, Schedule_movie_form, Delete_schedule_form, Filter_movie_form

app = Flask(__name__) 

app.config['SECRET_KEY'] = "secret_key"

@app.route('/techadmin/login', methods=['GET','POST']) 
def techadmin_login():
	login_form = Login_form()
	if login_form.validate_on_submit():
		# check if user exist in database with role as tech admin
		# Complete the code
		return render_template('home.html')
	return render_template('login.html', form=login_form)

@app.route('/techadmin/changepassword', methods=['GET','POST']) 
def techadmin_change_password():
	change_password_form = Change_password_form()
	if change_password_form.validate_on_submit():
		# check if user exist in database with role as tech admin
		# Complete the code
		return redirect(url_for('techadmin_login'))
	return render_template('change_password.html', form=change_password_form)

@app.route('/techadmin/home', methods=['GET'])
def home(): 
	return render_template('home.html')

@app.route('/techadmin/schedule', methods=['GET'])
def schedule_movie():
	schedule_form = Schedule_movie_form()
	return render_template('schedule_movie.html', form=schedule_form)

@app.route('/techadmin/delete', methods=['GET'])
def delete_schedule():
	form = Delete_schedule_form()
	return render_template('delete_schedule.html', form=form)

@app.route('/techadmin/view', methods=['GET'])
def view_schedule():
	form = Filter_movie_form()
	# entring dummy data for now
	movie_list = [{'movie_name':'DDL', 'theater_name':'PVR Nexus', 'start_date':'12/03/24','end_date': '12/04/24'}]
	return render_template('view_schedule.html', form=form, movie_list=movie_list)

if __name__ == '__main__': 
	app.run(debug=True) 
