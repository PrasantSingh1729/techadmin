
from flask import Flask
from app.tech_admin_bp.view import tech_admin_bp
from app.extension import mysql

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'

# Register Blueprints
app.register_blueprint(tech_admin_bp, url_prefix='/tech_admin')

app.config['SECRET_KEY'] = "secret_key" 
app.config['MYSQL_HOST']= "localhost" 
app.config['MYSQL_USER'] = "root" 
app.config['MYSQL_PASSWORD'] = "" 
app.config['MYSQL_DB'] = "Movie_Booking" 
app.config['MYSQL_CURSORCLASS'] = "DictCursor"

mysql.init_app(app)

if __name__ == '__main__':
    app.run(debug=True)
