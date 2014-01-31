import flask, flask.views
from flask import request
import os
app = flask.Flask(__name__)

@app.route('/')
def index():
    return flask.render_template('index.html')

@app.route('/<category>')
def catpage(category):
    path = 'summary.txt'
    f= open(path)
    data = eval( f.read() )['summary']
    f.close()
    data = [i for i in data[1:] if i['category'] == category]
    return flask.render_template('index.html',data=data,cat=category)

@app.route('/v/<id>')
def newspage(id):
    path = 'summary.txt'
    f= open(path)
    data = eval( f.read() )['summary']
    f.close()
    data = [i for i in data[1:] if i['id'] == id][0]
    data['summary'] = data['summary'].split('\n\n')
    return flask.render_template('news.html',data=data)

'''
class Main(flask.views.MethodView):
    def get(self):
        path = 'summary.txt'
        cat = user = request.args.get('cat')
        f= open(path)
        data = eval( f.read() )['summary']
        f.close()
        data = [i for i in data[1:] if i['category'] == cat]
        return flask.render_template('index.html',data=data,cat=cat)
    
app.add_url_rule('/', view_func=Main.as_view('main'), methods=['GET', 'POST'])
'''
app.debug = True
app.run()
