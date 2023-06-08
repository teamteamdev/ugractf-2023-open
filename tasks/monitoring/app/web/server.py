from flask import Flask, render_template, request, session, redirect
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from kyzylborda_lib.secrets import get_flag, validate_token

def make_app():

    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for = 1, x_host = 1)
    app.secret_key = 'YTE1NTJkODMtNWUwMy00NDk5LTlmMDUt'
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://websvc:MzMwZjgzYjktMjU4NS00YzJhLWI5ODct@database:3306/appdb?charset=utf8mb4'
    db = SQLAlchemy(app)
    
    class User(db.Model):
        __tablename__ = 'users'
        id = db.Column('id', db.Integer, primary_key=True)
        username = db.Column('username', db.String(64), nullable=False)
        password = db.Column('password', db.String(64), nullable=False)
        token = db.Column("token", db.String(64), nullable=False)

        def __repr__(self):
            return '<User %r>' % self.username
        
    @app.route("/favicon.ico/")
    def favicon():
        return "404", 404
    
    @app.route("/<token>/")
    def index(token):
        if not validate_token(token):
            return "ZHETON BEDA", 401
        else:
            return render_template("welcome.html", token=token)
        
    @app.route("/<token>/demo")
    def demo(token):
        if not validate_token(token):
            return "ZHETON BEDA", 401
        username = request.args.get('username')
        if username not in ['admin', 'test']:
            check_username = User.query.filter(User.username == username,
                                               User.token == token).first()
            if check_username is None:
                return render_template("demo-dashboard.html", token=token, error_message="Пользователь не найден"), 404
        flag = ''
        if username == 'admin':
            flag = get_flag(token)
        return render_template("demo-dashboard.html", user=username, token=token, flag=flag), 200

    @app.route("/<token>/dashboard")
    def dashboard(token):
        if not validate_token(token):
            return "ZHETON BEDA", 401
              
        if 'sessid' in session:
            return render_template("dashboard.html", user=session['sessid'], token=token)
        else:
            return redirect(f'/{token}/login')
        
    @app.route("/<token>/login", methods=['GET', 'POST'])
    def login(token):
        if not validate_token(token):
            return "ZHETON BEDA", 401
        
        if request.method == 'GET':
            return render_template("login.html", token=token)
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']

            user = User.query.filter(User.username == username,
                                    User.password == password,
                                    User.token == token).first()
            if user:
                session['sessid'] = user.username
                return redirect(f'/{token}/dashboard')
            else:
                error_message = 'Неправильное имя пользователя или пароль!.'
                return render_template('login.html', token=token, error_message=error_message)
            
    @app.route("/<token>/register", methods=['GET', 'POST'])
    def register(token):
        if not validate_token(token):
            return "ZHETON BEDA", 401
        
        if request.method == 'GET':
            return render_template("register.html", token=token)
        elif request.method == 'POST':
            username = request.form['username']
            password = request.form['password']
            confirm_password = request.form['confirm_password']

            if password != confirm_password:
                return render_template('register.html',token=token, error_message="Пароль не совпадает с повтором!")

            check_username = User.query.filter(User.username == username,
                                               User.token == token).first()
            if check_username is not None or username in ['admin', 'test']:
                return render_template("register.html", token=token, error_message="Такой пользователь уже зарегистрирован")       

            new_user = User()
            new_user.username = username
            new_user.password = password
            new_user.token = token
            db.session.add(new_user)
            db.session.commit()

            return redirect(f'/{token}/login')
        
    @app.route("/<token>/logout")
    def logout(token):
        if not validate_token(token):
            return "ZHETON BEDA", 401
        session.pop('sessid', None)
        return redirect(f'/{token}/')
    
    return app
