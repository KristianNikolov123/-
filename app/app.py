from flask import Flask, render_template, request, redirect, url_for, flash
from flask_sqlalchemy import SQLAlchemy
import bcrypt

app = Flask(__name__)
app.secret_key = "your_secret_key" 


app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://myuser:mypassword@localhost:5432/mydatabase'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
db = SQLAlchemy(app)

class User(db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(50), nullable=False)
    last_name = db.Column(db.String(50), nullable=False)
    email = db.Column(db.String(100), unique=True, nullable=False)
    password = db.Column(db.String(255), nullable=False)

    def __init__(self, first_name, last_name, email, password):
        self.first_name = first_name
        self.last_name = last_name
        self.email = email
        self.password = password

@app.route('/signIn', methods=['GET', 'POST'])
def signIn():
    if request.method == 'POST':
        first_name = request.form.get('first-name')
        last_name = request.form.get('last-name')
        email = request.form.get('email')
        password = request.form.get('password')

        
        if User.query.filter_by(email=email).first():
            return "Email address already exists. Please try logging in."

        
        hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt()).decode('utf-8')

        
        new_user = User(first_name, last_name, email, hashed_password)

       
        db.session.add(new_user)
        db.session.commit()

        return redirect(url_for('index'))
    return render_template('signIn.html')


@app.route('/logIn', methods=['GET', 'POST'])
def logIn():
    if request.method == 'POST':
        email = request.form.get('email')
        password = request.form.get('password')

       
        user = User.query.filter_by(email=email).first()

        if user:
            
            stored_password = user.password.encode('utf-8')

           
            if bcrypt.checkpw(password.encode('utf-8'), stored_password):
                flash("Successfully logged in!", "success")
                return redirect(url_for('index'))
            else:
                return "Invalid email or password. Please try again."
        else:
            return "Invalid email or password. Please try again."

    return render_template('logIn.html')



@app.route('/')
def index():
    return render_template('index.html')

@app.route('/builds')
def builds():
    return render_template('builds.html')

if __name__ == '__main__':
    app.run(debug=True, host='0.0.0.0', port=5000)
