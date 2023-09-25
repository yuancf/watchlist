from flask import Flask, render_template
from flask import url_for
from markupsafe import escape

app = Flask(__name__)

# 定义虚拟数据
name = 'yuancf'
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

# @app.route('/')
# def hello():
#     return 'Hello'

# 主页面
@app.route('/')
def index():
    return render_template('index.html', name=name, movies=movies)

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
