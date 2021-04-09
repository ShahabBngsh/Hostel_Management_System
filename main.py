from flask import Flask, render_template

app = Flask(__name__)

#route to login.html page
#NOTE: if you want to change function name, then also change in template.html file

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/searchroom")
def searchroom():
    return render_template("searchroom.html")

    
if __name__ == "__main__":
    app.run(debug=True)