import os, random, datetime
from app import app, db
from flask import render_template, request, redirect, url_for, flash, jsonify, make_response
from forms import SignUpForm
from models import UserProfile
from werkzeug.utils import secure_filename

@app.route('/')
def index():
    return render_template("home.html")
    
@app.route('/profile', methods=["GET", "POST"])
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
            
            # get and save the image
            pic = request.files['image']
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
    
    users = UserProfile.query.all()
    user_list = [{"user": user.username, "userid": user.userid} for user in users]
    
    if request.method == "GET":
        return render_template("view_all.html", users=users)
    
    elif request.method == "POST":
        response = make_response(jsonify({"users": user_list}))                                           
        response.headers['Content-Type'] = 'application/json'            
        return response

@app.route('/profile/<userid>', methods=["GET", "POST"])
def get_profile(userid):
    
    user = UserProfile.query.filter_by(userid=userid).first()
    
    if request.method == "GET":
        return render_template("view_user.html", user=user)
    
    elif request.method == "POST":
        if user is not None:
            response = make_response(jsonify(userid=user.userid, username=user.username, image=user.image, gender=user.gender, age=user.age,
                    profile_created_on=user.profile_created_on))
            response.headers['Content-Type'] = 'application/json'            
            return response
        else:
            flash('No User Found', 'danger')
            return redirect(url_for("index"))
            
@app.after_request
def add_header(response):
    response.headers["Content-Type"] = "application/json"
    return response

def genId(fname, lname, age):
    nid = []
    for x in fname:
        nid.append(str(ord(x)))
    for x in lname:
        nid.append(str(ord(x)))
    nid.append(str(age))
    
    random.shuffle(nid)
    
    nid = "".join(nid)
    
    return nid[:7]
    
def genUsername(fname):
    return fname + str(random.randint(10,100))
    
if __name__ == '__main__':
    app.run(debug=True,host="0.0.0.0",port="8080")