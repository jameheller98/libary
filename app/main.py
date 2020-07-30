from flask import Flask, render_template

app = Flask(__name__)


@app.route('/')
def index():
    return render_template("index.html")


@app.route('/books')
def books():
    return render_template("books.html")


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


if __name__ == '__main__':
    app.run()
