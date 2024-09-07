from flask import Flask,render_template,request,redirect,session,jsonify,flash
from chatbot.chat import get_response
from flask_sqlalchemy import SQLAlchemy
import numpy as np
from keras.models import load_model
from keras.preprocessing.image import load_img
import bcrypt
import cv2


app = Flask(__name__)
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///database.db'
db = SQLAlchemy(app)
app.secret_key = 'ashdiuesnohsaohneo'

class User(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    firstname = db.Column(db.String(100), nullable=True)
    lastname = db.Column(db.String(100), nullable=True)
    email = db.Column(db.String(100), nullable=True)
    password = db.Column(db.String(100), nullable=True)

    def __init__(self,email,password,firstname,lastname):
        self.firstname = firstname
        self.lastname = lastname
        self.email = email
        self.password = bcrypt.hashpw(password.encode('utf-8'),bcrypt.gensalt()).decode('utf-8')

    def check_password(self,password):
        return bcrypt.checkpw(password.encode('utf-8'),self.password.encode('utf-8'))


with app.app_context():
    db.create_all()



model = load_model('C:\\Users\\DELL\\Desktop\\testing - Copy\\blu_vs_cln.h5')


@app.route('/',methods=['GET'])
def home():
    
    return render_template('index.html')

# app.route('/chat',methods=['GET'])
# def chat():    
#     return render_template('chat.html')
@app.route('/',methods=['POST'])
def chat_predict():
    text = request.get_json().get('message')
    response = get_response(text)
    message = {"answer": response}
    return jsonify(message)
    
    



@app.route('/upload',methods=['GET'])
def prediction():
    return render_template('indexes.html')
@app.route('/upload', methods=['POST'])
def predict():
    imagefile= request.files['imagefile']
    image_path = "static/images/" + imagefile.filename
    imagefile.save(image_path)
    image = image_path
    img = load_img(image, target_size=(224, 224))
    img_array = np.array(img)
    img_array = img_array.reshape(1,224,224,3)
    img_pred = model.predict(img_array)
    if img_pred == 0:
        result = 'This is a BLUR image! Please upload a clear image'
    else:
        result = 'This is a CLEAR image!'
    return render_template('indexes.html', result=result, image_path = image)


@app.route('/register', methods=['GET','POST'])
def register():
    if request.method == 'POST':
        firstname = request.form['firstname']
        lastname = request.form['lastname']
        email = request.form['email']
        password = request.form['password']
        
        new_user = User(firstname=firstname,lastname=lastname,email=email,password=password)
        db.session.add(new_user)
        db.session.commit()
        return redirect('login')
    return render_template('registration.html')


@app.route('/login',methods=['GET','POST'])
def login():
    if request.method == 'POST':
        email = request.form['email']
        password = request.form['password']
        
        user = User.query.filter_by(email=email).first()
        
        if user and user.check_password(password):
            session['firstname'] = user.firstname
            session['lastname'] = user.lastname
            session['email'] = user.email
            session['password'] = user.password
            return redirect('/')
        else:
            return render_template('login.html', error='Invalid user')
            
        
        
        
    return render_template('login.html')

@app.route('/contact',methods=['GET','POST'])
def contact():
    return render_template('contact.html')

@app.route('/demo',methods=['GET'])
def demoapp():
    return render_template('demo.html')
@app.route('/demo',methods=['POST'])
def demo():
    imagefile= request.files['imagefiledemo']
    image_path = "static/imagesdemo/" + imagefile.filename
    imagefile.save(image_path)
    image = image_path
    img = load_img(image, target_size=(224, 224))
    img_array = np.array(img)
    img_array = img_array.reshape(1,224,224,3)
    img_pred = model.predict(img_array)
    print(img_pred)
    if img_pred == 0:
        result = 'This is a BLUR image! Please upload a clear image'
    else:
        result = 'This is a CLEAR image!'
        flash('The form is submitted successfully')
        
    return render_template('demo.html', result=result)
    
@app.route('/about')
def about():
    return render_template('about.html') 

if __name__ =='__main__':
    app.run(debug=True)