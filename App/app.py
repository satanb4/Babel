from flask import Flask, render_template, url_for, request,redirect, session
from recognition import speechRec
from translation import translate
from backend import Database
import os,json
from werkzeug.utils import secure_filename

STORAGE_FOLDER = 'storage'
ALLOWED_EXTENSIONS = {'pcap','txt','wav'}
VOICE_DATA = STORAGE_FOLDER+'/'+'voice_data.json'

app = Flask(__name__,static_folder='static',template_folder='templates')
app.config['STORAGE_FOLDER'] = STORAGE_FOLDER
app.config['SECRET_KEY'] = os.urandom(12)

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def recogTranslate(data):
    recognised = speechRec(audio_data=data)
    translated = translate(recognised)
    dataDict = {'recognised':recognised,'translated':translated}
    with open(VOICE_DATA,'w+') as f:
        json.dump(dataDict,f)
    return True

@app.route('/home')
@app.route('/')
def home():
    menuButtons = [('Home','/'),('Ribbon','https://ribboncommunications.com/'),('Login','/login')]
    return render_template('index.html',title='Babel Home',menuButtons=menuButtons)

@app.route('/intercept',methods=['POST','GET'])
def intercept():
    data = request.data
    recogTranslateProcess = recogTranslate(data)
    return 'Okay'

@app.route('/login',methods=['POST','GET'])
def login():
    db = Database()
    if request.method == 'POST':
        formData = request.form.to_dict()
        session['name'] = formData['uname']
        session['password'] = formData['psw']
        user = db.verify_user(session['name'],session['password'])
        if user:
            return redirect(url_for('dashboard'))
        else:
            return render_template('login.html',title='Login',display='none')

    if request.method == 'GET':
        if 'name' in session.keys() and session['name']:
            return redirect(url_for('dashboard'))
        return render_template('login.html',title='Login',display='none')

@app.route('/sign-up',methods=['POST','GET'])
def signUp():
    db = Database()
    if request.method == 'POST':
        formData = request.form.to_dict()
        if db.verify_user(formData['uname'],formData['psw']):
            return redirect(url_for('login'))
        else:
            db.add_user(formData['uname'],formData['sname'],formData['mail'],formData['psw'])
            return redirect(url_for('login'))
    
    elif request.method == 'GET':
        return render_template('signup.html',title='Sign Up')
        

@app.route('/dashboard',methods=['POST','GET'])
def dashboard():
    menuButtons = [('Home','/'),('Logout','/logout')]
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            return redirect(url_for('dashboard'))
    
    elif request.method == 'GET':
        with open(VOICE_DATA,'r') as f:
            dataDict = json.load(f)
        return render_template('dashboard.html',title='Dashboard',menuButtons=menuButtons,data=dataDict)


@app.route('/uploader', methods = ['GET', 'POST'])
def upload_file():
   if request.method == 'POST':
      f = request.files['file']
      fileName = secure_filename(f.filename)
      f.save(fileName)
      os.rename(fileName,'static/sound/test.wav')
      return redirect(url_for('dashboard'))

@app.route('/logout')
def logout():
    session.clear()
    return redirect(url_for('login'))

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)