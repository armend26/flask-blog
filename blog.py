from datetime import timedelta
from operator import index
from flask import Flask,render_template
from flask import request,session
from flask.helpers import url_for 
from flask_sqlalchemy import SQLAlchemy
from werkzeug.utils import redirect

app = Flask(__name__) 
app.config['SQLALCHEMY_DATABASE_URI'] = 'sqlite:///db.sqlite'
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
app.permanent_session_lifetime = timedelta(seconds = 10)
app.secret_key = "blog"

db = SQLAlchemy(app)


class BlogDatas(db.Model):
    __tablename__ = 'BlogDatas'
    id = db.Column(db.Integer,primary_key=True)
    postTitle = db.Column(db.String(30),index=True) 
    postContent = db.Column(db.String(600),index=True)
    postImage = db.Column(db.String(600),index=True) 

@app.route('/')
def home():
    posts = BlogDatas.query.all()
    return render_template("home.html",posts=posts)

@app.route('/controlpanel',methods=["POST","GET"])
def cms():
    if "usr_name" in session:
        if request.method == "POST": 
            post_title = request.form["post-title"]
            post_content = request.form["post-content"]
            post_image = request.form["post-url"]
            new_post = BlogDatas(postTitle=post_title,postContent=post_content,postImage=post_image)
            db.session.add(new_post)
            db.session.commit()
            return redirect(url_for('home'))
        else:
            posts = BlogDatas.query.all()
            return render_template('controlpanel.html',posts=posts)
    return render_template('controlpanel.html')

@app.route('/admin',methods=["POST","GET"])
def admin_login():
    if request.method == "POST":
        session.permanent = True
        user_name = request.form["usrname"]
        user_pass = request.form["pass"]
        session["user_name"] = user_name
        if user_name=="admin" and user_pass=="admin":
            return redirect(url_for('cms'))
        else:
            return render_template('loginpage.html')
    return render_template('loginpage.html')

@app.route("/control_delete",methods=["POST","GET"])
def deletePost():
    posts = BlogDatas.query.all()
    if request.method == "POST":
        post_to_delete = request.form["value"]
        tdata = BlogDatas.query.filter_by(id=post_to_delete).first()
        db.session.delete(tdata)
        db.session.commit()
        return redirect(url_for('cms'))
    else:
        return render_template("deletecontrol.html",posts=posts)



if __name__=='__main__':
    db.create_all()
    app.run()
