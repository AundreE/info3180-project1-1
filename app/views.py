import os, random, datetime
from app import app, db
from flask import render_template, request, redirect, url_for, flash
from forms import SignUpForm
from models import UserProfile
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    print "Welcome..."
    
@app.route('/profile')
def profile():
    form = SignUpForm()
    
    if request.method == "POST":
        file_folder = app.config['UPLOAD_FOLDER']
        
        if form.validate_on_submit():
            
            # get form data
            fname = form.first_name.data
            lname = form.last_name.data
            age = form.age.data
            gender = form.gender.data
            biography = form.biography.data
            
            # get the image
            pic = request.files['file']
            image = secure_filename(pic.filename)
            pic.save(os.path.join(file_folder, image))
            
            # generate user_id, username and date
            userid = genId(fname, lname, age)
            username = genUsername(fname)
            date_created = datetime.date.today()
            
            new_user = UserProfile(userid=userid, username=username, first_name=fname, last_name=lname, biography=biography, image=image,
                gender=gender,  profile_created_on=date_created, age=age)
                
            db.session.add(new_user)
            db.session.commit()
            
            flash("Created Successfully", "success")
            return redirect(url_for("profile"))
            
    return render_template("signup.html", form=form)

@app.route('/profiles', methods=["GET", "POST"])
def profiles():
    if request.method == "GET":
        pass
    
    
    elif request.method == "POST":
        return

@app.route('/profile/<userid>', methods=["GET", "POST"])
def get_profile(userid):
    if request.method == "GET":
        return
    
    elif request.method == "POST":
        user = UserProfile.query.filter_by(userid=userid).first()
        if user is not None:
            print user
        else:
            flash('No User Found', 'danger')

def genId(fname, lname, age):
    nid = ""
    for x in fname:
        nid += str(ord(x))
    for x in lname:
        nid += str(ord(x))
    nid += str(age)
    return nid
    
def genUsername(fname):
    return fname + str(random.randint(10,100))
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")