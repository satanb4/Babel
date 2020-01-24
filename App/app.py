from flask import Flask, render_template, url_for, request
from recognition import speechRec

app = Flask(__name__,static_folder='static',template_folder='templates')

@app.route('/home')
@app.route('/')
def home():
    menuButtons = [('Home','/'),('List','/list'),('Login','/login'),('Intercept','/intercept')]
    return render_template('index.html',title='Babel Home',menuButtons=menuButtons)

@app.route('/intercept',methods=['POST','GET'])
def intercept():
    data = request.data
    recognised = speechRec(audio_data=data)
    print(recognised)
    return 'Hey'

if __name__ == "__main__":
    app.run(debug=True,host='0.0.0.0',port=5000)