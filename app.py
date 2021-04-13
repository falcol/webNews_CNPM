from __init__ import db, app
import os
from sqllib.database import User, Corona, Corona_VN, News, Category
from flask import render_template, url_for, redirect, request, flash, session


@app.route("/")
@app.route("/home")
def home():
    news = db.session.query(News).all()
    news_dict = [new.__dict__ for new in news][::-1]
    cate = db.session.query(Category.id, Category.name).all()
    login = session.get("logged_in")

    result = []
    for ca in cate:
        data = []
        for ne in news_dict:
            if ca[0] == ne["category_id"]:
                data.append(ne)
        tup = (ca[1], data)
        result.append(tup)

    return render_template('index.html', data=result, login=login, username=session.get("username"))


@app.route("/register", methods=["GET", "POST"])
def register():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]

        new_User = User(username=username, password=password)
        db.session.add(new_User)
        db.session.commit()
        flash("New user has been update")
        return redirect(url_for("login"))

    return render_template("register.html")


@app.route("/login", methods=["GET", "POST"])
def login():
    if request.method == "POST":
        username = request.form["username"]
        password = request.form["password"]
        session["username"] = username

        log = db.session.query(User).filter(User.username==username, User.password==password).first()
        if log:
            flash("Login success")
            session["logged_in"] = True
            return redirect(url_for('home'))
        else:
            flash("Thông tin tài khoản hoặc mật khẩu không chính xác")

    return render_template('login.html')


@app.route("/logout", methods=["GET", "POST"])
def logout():
    session["logged_in"] = False
    return home()


@app.route("/corona")
def corona():
    covid = db.session.query(Corona).all()
    data = [c.__dict__ for c in covid]
    covid_VN = db.session.query(Corona_VN).all()
    data2 = [c.__dict__ for c in covid_VN]
    login = session.get("logged_in")

    return render_template('corona.html', data=data, data2=data2, login=login, username=session.get("username"))


@app.route("/category/<int:cate_id>", methods=["GET", "POST"])
def category(cate_id):
    catego = db.session.query(Category).filter(Category.id==cate_id).first()
    news = db.session.query(News).filter(News.category_id==catego.id).all()
    news_dict = [new.__dict__ for new in news][::-1]
    login = session.get("logged_in")

    result = (catego.name, news_dict)

    return render_template("category.html", data=result, login=login, username=session.get("username"))


@app.route("/postnews", methods=["GET", "POST"])
def postnews():
    if request.method == "POST":
        image = request.form["image"]
        title = request.form["tit"]
        link = request.form["link"]
        intro = request.form["intro"]
        cate = int(request.form["cate"])

        news = News(img=image, title=title, href=link,sapo=intro, category_id=cate)
        db.session.add(news)
        db.session.commit()
    login = session.get("logged_in")

    return render_template("post.html", login=login, username=session.get("username"))


if __name__ == "__main__":
    app.secret_key = os.urandom(12)
    app.run(debug=True)
