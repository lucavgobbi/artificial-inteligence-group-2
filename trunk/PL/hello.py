from bottle import route, run

@route('/hello/:name')
def hello(name):
    return "Hello %s!" % name

@route('/index/:contador')
def index(contador):
    a = "<table><tr><td>Index</td></tr>"
    a += "<tr><td>" + contador + "</td></tr>"
    return a

run(host='localhost', port=8080)