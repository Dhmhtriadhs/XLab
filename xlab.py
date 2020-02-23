from flask import Flask, request, send_from_directory, render_template
from werkzeug.utils import secure_filename
from xdb import xdb
import os, json, socket
app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = "./img/"
db = xdb()

# TODO: fill excersices
# TODO: viewers mode

@app.route('/html/<path:path>')
def send_html(path):
   return send_from_directory('html',path)

@app.route('/img/<path:path>')
def send_xray(path):
   return send_from_directory('img',path)

@app.route('/upload', methods=['GET', 'POST'])
def upload():
    file = request.files['photo']
    filename = secure_filename(file.filename)
    file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    return {"result":"OK","filename":filename}

@app.route('/<int:exercise>')
def xmu(exercise):
    data = db.getPatient(exercise)
    js_value = str(json.dumps(data))#.replace(u'<', u'\\u003c').replace(u'>', u'\\u003e').replace(u'&', u'\\u0026').replace(u"'", u'\\u0027'))
    js_value  = str(data)
    print(data)
    print(js_value)
    return render_template('Xray.html', data=data, js_value=js_value)

@app.route('/admin/<data>')
def admin(data):
    jsn = eval(data)
    if "command" not in jsn:
        return str({"result":"fail"})
    if jsn["command"]=="addBodypart":
        db.addBodypart(jsn["en"],jsn["gr"])
    elif jsn["command"]=="getBodyparts":
        ret = str(db.getBodyparts()).replace("'",'"')
        return ret
    elif jsn["command"]=="removeBodypart":
        ret = str(db.removeBodypart(int(jsn["id"])))
    elif jsn["command"]=="getExams":
        ret = str(db.getExams(jsn["id"])).replace("'",'"')
        return ret
    elif jsn["command"]=="addExam":
        db.addExam(jsn["bodyID"], jsn["en"], jsn["gr"], jsn["from"], jsn["to"])
    elif jsn["command"]=="removeExam":
        db.removeExam(int(jsn["id"]))
    elif jsn["command"]=="getXrays":
        ret = str(db.getXrays(jsn["id"])).replace("'",'"')
        return ret
    elif jsn["command"]=="addXray":
        db.addXray(jsn)
    elif jsn["command"]=="removeXray":
        db.removeXray(int(jsn["id"]))
    elif jsn["command"]=="getQRs":
        ret = str(db.getQRs()).replace("'",'"')
        print(ret)
        return ret

    return str({"result":"OK"})

@app.route('/view')
def view():
   return 'view'

@app.route('/')
def base():
    sockets = (([ip for ip in socket.gethostbyname_ex(socket.gethostname())[2] if not ip.startswith("127.")] or [[(s.connect(("8.8.8.8", 53)), s.getsockname()[0], s.close()) for s in [socket.socket(socket.AF_INET, socket.SOCK_DGRAM)]][0][1]]) + ["no IP found"])[0]
    return render_template('qr.html', data=sockets)

if __name__ == '__main__':
   app.run(host='0.0.0.0')
