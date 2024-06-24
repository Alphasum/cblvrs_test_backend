from flask import Flask, render_template, request, redirect, url_for, flash, session
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from werkzeug.utils import secure_filename
import os
from datetime import datetime

app = Flask(__name__)
app.config['SECRET_KEY'] = 'your_secret_key'
app.config['SQLALCHEMY_DATABASE_URI'] = 'postgresql://postgres:FvIMXvBgBmAVXPEEcNTwuVFNBjJbJzqf@monorail.proxy.rlwy.net:19636/railway'
app.config['UPLOAD_FOLDER'] = 'static/uploads/'
app.config['MAX_CONTENT_PATH'] = 100 * 1024 * 1024  # Maximum file size of 100MB

db = SQLAlchemy(app)
migrate = Migrate(app, db)

# Ensure the upload folder exists
if not os.path.exists(app.config['UPLOAD_FOLDER']):
    os.makedirs(app.config['UPLOAD_FOLDER'])

class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(150), unique=True, nullable=False)
    password = db.Column(db.String(150), nullable=False)
    first_name = db.Column(db.String(150))
    last_name = db.Column(db.String(150))
    profile_picture = db.Column(db.String(150), nullable=True)

class ProfilePicture(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    filename = db.Column(db.String(150), nullable=False)
    user_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    user = db.relationship('User', backref=db.backref('profile_pictures', lazy=True))

class Post(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    text = db.Column(db.String(500), nullable=True)
    image = db.Column(db.String(150), nullable=True)
    video = db.Column(db.String(150), nullable=True)
    poster_id = db.Column(db.Integer, db.ForeignKey('user.id'), nullable=False)
    poster = db.relationship('User', backref=db.backref('posts', lazy=True))
    timestamp = db.Column(db.DateTime, default=datetime.utcnow)

@app.route('/')
def landing():
    return render_template('landing.html')

@app.route('/about')
def about():
    return render_template('about.html')

@app.route('/contactus')
def contactus():
    return render_template('contactus.html')

@app.route('/faq')
def faq():
    return render_template('faq.html')

@app.route('/privacypolicy')
def privacypolicy():
    return render_template('privacypolicy.html')

@app.route('/termsandconditions')
def termsandconditions():
    return render_template('termsandconditions.html')

@app.route('/cookiepolicy')
def cookiepolicy():
    return render_template('cookiepolicy.html')

@app.route('/communityguidelines')
def communityguidelines():
    return render_template('communityguidelines.html')

@app.route('/feedack')
def feedack():
    return render_template('feedack.html')

@app.route('/home')
def home():
    return render_template('index.html')

@app.route('/signup', methods=['POST'])
def signup():
    email = request.form.get('email')
    first_name = request.form.get('first_name')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    if user:
        flash('Email address already exists')
        return redirect(url_for('home'))
    
    new_user = User(email=email, first_name=first_name, password=generate_password_hash(password, method='pbkdf2:sha256'))
    db.session.add(new_user)
    db.session.commit()
    
    flash('Account created successfully')
    return redirect(url_for('home'))

@app.route('/login', methods=['POST'])
def login():
    email = request.form.get('email')
    password = request.form.get('password')
    
    user = User.query.filter_by(email=email).first()
    if not user or not check_password_hash(user.password, password):
        flash('Login failed. Check your email and password')
        return redirect(url_for('home'))
    
    session['user_id'] = user.id
    session['user_first_name'] = user.first_name
    session['user_email'] = user.email
    flash('Logged in successfully')
    return redirect(url_for('bible'))

@app.route('/bible')
def bible():
    if 'user_id' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('home'))
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('home'))

    user_first_name = user.first_name
    profile_picture = user.profile_picture  # Assuming the profile picture filename is stored in this column
    
    return render_template('bible.html', first_name=user_first_name, profile_picture=profile_picture)


@app.route('/logout')
def logout():
    session.pop('user_id', None)
    session.pop('user_first_name', None)
    flash('You have been logged out')
    return redirect(url_for('/'))

@app.route('/biblespaceenv')
def biblespaceenv():
    if 'user_id' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('home'))
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('home'))

    user_first_name = user.first_name
    profile_picture = user.profile_picture  # Assuming the profile picture filename is stored in this column
    
    return render_template('biblespaceenv.html', first_name=user_first_name, profile_picture=profile_picture)
@app.route('/blessedbazaar')
def blessedbazaar():
    if 'user_id' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('home'))
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('home'))

    user_first_name = user.first_name
    profile_picture = user.profile_picture  # Assuming the profile picture filename is stored in this column
    
    return render_template('blessedbazaar.html', first_name=user_first_name, profile_picture=profile_picture)

@app.route('/entertainment')
def entertainment():
    if 'user_id' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('home'))
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('home'))

    user_first_name = user.first_name
    profile_picture = user.profile_picture  # Assuming the profile picture filename is stored in this column
    
    return render_template('entertainment.html', first_name=user_first_name, profile_picture=profile_picture)

@app.route('/gracefulgiving')
def gracefulgiving():
    if 'user_id' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('home'))
    
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('home'))

    user_first_name = user.first_name
    profile_picture = user.profile_picture  # Assuming the profile picture filename is stored in this column
    
    return render_template('gracefulgiving.html', first_name=user_first_name, profile_picture=profile_picture)


@app.route('/profile', methods=['GET', 'POST'])
def profile():
    if 'user_id' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('home'))

    user = User.query.get(session['user_id'])
    
    if request.method == 'POST':
        # Handle profile picture upload
        profile_picture = request.files.get('profile_picture')
        if profile_picture:
            filename = secure_filename(profile_picture.filename)
            profile_picture.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            
            # Update user's profile picture in database
            user.profile_picture = filename
            db.session.commit()
            flash('Profile picture updated successfully!')
    
    return render_template('profile.html', user=user)

@app.route('/spherebids')
def spherebids():
    if 'user_id' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('home'))
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('home'))

    user_first_name = user.first_name
    profile_picture = user.profile_picture  # Assuming the profile picture filename is stored in this column
    
    return render_template('spherebids.html', first_name=user_first_name, profile_picture=profile_picture)

@app.route('/socialcircle', methods=['GET', 'POST'])
def socialcircle():
    if 'user_id' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('home'))
    
    user = User.query.get(session['user_id'])
    user_id = session.get('user_id')
    user = User.query.get(user_id)
    if not user:
        flash('User not found')
        return redirect(url_for('home'))

    user_first_name = user.first_name
    profile_picture = user.profile_picture
    
    if request.method == 'POST':
        text = request.form.get('text')
        image_file = request.files.get('image')
        video_file = request.files.get('video')
        
        image_filename = None
        video_filename = None
        
        if image_file and image_file.filename != '':
            image_filename = secure_filename(image_file.filename)
            image_filepath = os.path.join(app.config['UPLOAD_FOLDER'], image_filename)
            image_file.save(image_filepath)
        
        if video_file and video_file.filename != '':
            video_filename = secure_filename(video_file.filename)
            video_filepath = os.path.join(app.config['UPLOAD_FOLDER'], video_filename)
            video_file.save(video_filepath)

        new_post = Post(text=text, image=image_filename, video=video_filename, poster=user)
        db.session.add(new_post)
        db.session.commit()
        
        flash('Post created successfully!')
        return redirect(url_for('socialcircle'))
    
    posts = Post.query.order_by(Post.timestamp.desc()).all()
    return render_template('socialcircle.html', posts=posts, user=user,first_name=user_first_name, profile_picture=profile_picture)



@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return redirect(url_for('static', filename='uploads/' + filename), code=301)

@app.route('/payment')
def payment():
    if 'user_id' not in session:
        flash('Please log in to access this page')
        return redirect(url_for('home'))
    
    return render_template('payment.html')

if __name__ == '__main__':
    with app.app_context():
        db.create_all()
    app.run(debug=True,host='0.0.0.0', port=8080)
