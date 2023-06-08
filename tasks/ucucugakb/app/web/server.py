from flask import Flask, send_from_directory, render_template, request
from flask_sqlalchemy import SQLAlchemy
from werkzeug.middleware.proxy_fix import ProxyFix
from kyzylborda_lib.secrets import get_flag, validate_token

all_authors = ['nsychev', 'ksixty', 'kalan', 'abbradar', 'javach', 'gudn', 'purplesyringa', 'rozetkin', 'baksist', 'astrra']
all_events = ['ugractf-2020-quals', 'ugractf-2020-school', 'ugractf-2021-quals', 'ugractf-2021-school', 'ugractf-2022-quals', 'ugractf-2022-school', 'ugractf-2023-quals', 'ugractf-2023-school']
all_categories = ['web', 'crypto', 'pwn', 'reverse', 'forensics', 'osint', 'recon', 'misc', 'joy', 'ctb', 'ppc', 'stegano']

def make_app():
    
    app = Flask(__name__)
    app.wsgi_app = ProxyFix(app.wsgi_app, x_for = 1, x_host = 1)
    app.config['SQLALCHEMY_DATABASE_URI'] = 'mysql+pymysql://websvc:NDM5ZGUxNmUtZGJiMi00MDI3LWFmN2It@database:3306/appdb?charset=utf8mb4'
    db = SQLAlchemy(app)
    
    class Task(db.Model):
        __tablename__ = 'tasks'

        id = db.Column('id', db.Integer, primary_key=True)
        task_name = db.Column('task_name', db.String(30), nullable=False)
        title = db.Column('title', db.String(30), nullable=False)
        points = db.Column('points', db.Integer, nullable=False)
        category = db.Column('category', db.String(10), nullable=False)
        author = db.Column('author', db.String(20), nullable=False)
        event = db.Column('ctf', db.String(50), nullable=False)
        flag = db.Column('flag', db.String(100), nullable=False)

        def as_dict(self, show_flag=False):
            dict = {"Название": self.task_name,
                    "Заголовок": self.title,
                    "Тип": self.category,
                    "Стоимость": self.points,
                    "Создатель": self.author,
                    "Место": self.event}
            if show_flag == True:
                dict.update({"УИУ": self.flag})
            return dict

        def __repr__(self):
            return f'Task {self.task_name}'
        
    @app.route("/favicon.ico/")
    def favicon():
        return "404", 404
      
    @app.route("/<token>/")
    def index(token):
        if not validate_token(token):
            return "ZHETON BEDA", 401
        else:
            return render_template("index.html", token=token)

    @app.route("/<token>/api/")
    def api(token):
        if not validate_token(token):
            return "ZHETON BEDA", 401

        return send_from_directory("static", path="schema.json")    
        
    @app.route("/<token>/api/get-ucucuga")
    def search(token):
        if not validate_token(token):
            return "ZHETON BEDA", 401
        query = request.args.get('query')
        if query is None:
            query = ''
        category = request.args.getlist('category')
        if not category:
            category = all_categories
        elif 'osint' in category:
            category.append('recon')
        authors = request.args.getlist('author')
        if not authors:
            authors = all_authors
        min_points = request.args.get('min-points')
        if min_points is None:
            min_points = 0
        max_points = request.args.get('max-points')
        if max_points is None:
            max_points = 500
        events = request.args.getlist('event')
        if not events:
            events = all_events
        show_flag = request.args.get('show-flag')
        if show_flag == 'true':
            show_flag = True
        else:
            show_flag = False
        tasks = Task.query.filter(Task.task_name.like(f'%{query}%'),
                                  Task.category.in_(category),
                                  Task.author.in_(authors),
                                  Task.points >= min_points,
                                  Task.points <= max_points,
                                  Task.event.in_(events)).order_by(Task.task_name).all()
        result = {
            "order": ["Название", "Заголовок", "Тип", "Стоимость", "Создатель", "Место"],
            "data": []
        }
        if (show_flag):
            result["order"].append("УИУ")
        for task in tasks:
            if task.task_name == 'ucucugakb':
                task.flag = get_flag(token)
            result["data"].append(task.as_dict(show_flag))
        return result, 200
    
    return app