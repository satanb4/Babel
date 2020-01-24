from flask import Flask, render_template, url_for, request
from recognition import speechRec
from translation import translate
from backend import Database

app = Flask(__name__,static_folder='static',template_folder='templates')

@app.route('/home')
@app.route('/')
def home():
    menuButtons = [('Home','/'),('Ribbon','https://ribboncommunications.com/'),('Login','/login')]
    return render_template('index.html',title='Babel Home',menuButtons=menuButtons)

@app.route('/intercept',methods=['POST','GET'])
def intercept():
    data = request.data
    recognised = speechRec(audio_data=data)
    translated = translate(recognised)
    print(translated)
    return 'Okay'

@app.route('/login',methods=['POST','GET'])
def login():
    db = Database()
    formData = request.form.to_dict()
    if formData and db.verify_user(formData['uname'],formData['psw']):
        return render_template('dashboard.html',title='Dashboard')
    return render_template('login.html',title='Login')

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)