from flask import Flask, render_template
from flask import url_for
from markupsafe import escape
from flask_sqlalchemy import SQLAlchemy
import click
import os
import sys

# 判断操作的类型
WIN = sys.platform.startswith('win')
if WIN:     #如果是 Windows 系统，使用三个斜线
    prefix = 'sqlite:///'
else:   # 否则使用四个斜线
    prefix = 'sqlite:////'

# 创建app对象
app = Flask(__name__)

# 设置数据库URI
app.config['SQLALCHEMY_DATABASE_URI'] = prefix + os.path.join(app.root_path, 'data.db')
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False    # 关闭对模型修改的监控
# 在扩展类实例化前加载配置
db = SQLAlchemy(app)

# 创建数据库模型
class User(db.Model):   # 表名将会是 user（自动生成，小写处理）
    id = db.Column(db.Integer, primary_key=True)    # 主键
    name = db.Column(db.String(20))     # 名字

class Movie(db.Model):  # 表名将会是 movie
    id = db.Column(db.Integer, primary_key=True)    # 主键
    title = db.Column(db.String(60))    # 电影标题
    year = db.Column(db.String(4))  # 电影年份

# 自动执行创建数据库表操作
@app.cli.command()  # 注册为命令，可以传入 name 参数来自定义命令
@click.option('--drop', is_flag=True, help='Create after drop.')    # 设置选项
def initdb(drop):
    """Initialize the database."""
    if drop:    # 判断是否输入了选项
        db.drop_all()
    db.create_all()
    click.echo('Initialized database.') # 输出提示信息

# 创造假数据
@app.cli.command()
def forge():
    """Generate fake data."""
    db.create_all()

    # 全局的两个变量移动到这个函数内
    name = 'Yuan Chaofeng'
    movies = [
            {'title': 'My Neighbor Totoro', 'year': '1988'},
            {'title': 'Dead Poets Society', 'year': '1989'},
            {'title': 'A Perfect World', 'year': '1993'},
            {'title': 'Leon', 'year': '1994'},
            {'title': 'Mahjong', 'year': '1996'},
            {'title': 'Swallowtail Butterfly', 'year': '1996'},
            {'title': 'King of Comedy', 'year': '1999'},
            {'title': 'Devils on the Doorstep', 'year': '1999'},
            {'title': 'WALL-E', 'year': '2008'},
            {'title': 'The Pork of Music', 'year': '2012'},
            ]

    user = User(name=name)
    db.session.add(user)
    for m in movies:
        movie = Movie(title=m['title'], year=m['year'])
        db.session.add(movie)

    db.session.commit()
    click.echo('Done.')


# @app.route('/')
# def hello():
#     return 'Hello'

# 模板上下文处理函数
@app.context_processor
def inject_user():  # 函数名可以随意修改
    user = User.query.first()
    return dict(user=user)  # 需要返回字典，等同于 return {'user': user}

# 主页面
@app.route('/')
def index():
    # user = User.query.first()   # 读取用户记录
    movies = Movie.query.all()   # 读取所有电影记录
    return render_template('index.html', movies=movies)

# 404页面
@app.errorhandler(404)  # 传入要处理的错误代码
def page_not_found(e):  # 接受异常对象作为参数
    # user = User.query.first()
    return render_template('404.html'), 404  # 返回模板和状态码
@app.route('/user/<name>')
def user_page(name):
    return f'User: {escape(name)}'

@app.route('/test')
def test_url_for():
    #下面是一些调用示例（请访问http://localhost:5000/test 后在命令行窗口查看输出的URL：）
    print(url_for('hello'))     #生成hello视图函数对应的 URL，将输出：/
    print(url_for('user_page', name='yuancf'))      #输出：/user/yuancf
    print(url_for('user_page', name='tgjy'))        #输出：/user/tgjy
    print(url_for('test_url_for'))      #输出：/test
    print(url_for('test_url_for', num=2))       #输出：/test?num=2
    return 'Test page'
