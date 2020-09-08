from flask import render_template, request, redirect
from app import app, loginMngr, dao
from flask_login import login_user
from app.admin import *


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/books')
def books():
    return render_template("books.html", books = dao.read_book_infos())


@app.route('/cart')
def cart():
    return render_template("cart.html")


@app.route('/checkout')
def checkout():
    return render_template("checkout.html")


@app.route('/contact')
def contact():
    return render_template("contact.html")


@app.route('/services')
def services():
    return render_template("services.html")


@app.route('/login')
def login():
    return render_template("login.html")


@app.route("/login-admin", methods=['GET', 'POST'])
def login_admin():
    if request.method == 'POST':
        username = request.form.get("username")
        password = request.form.get("password", "")
        password = str(hashlib.md5(password.strip().encode("utf-8")).hexdigest())
        user = NhanVien.query.filter(NhanVien.taiKhoan == username.strip(),
                                     NhanVien.matKhau == password.strip()).first()
        if user:
            login_user(user=user)

    return redirect("/admin")


@loginMngr.user_loader
def user_load(username):
    return NhanVien.query.filter_by(taiKhoan=username).first()


if __name__ == '__main__':
    app.run(debug=True)
