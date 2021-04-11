from flask import Flask, render_template

app = Flask(__name__)

availRooms = [
    {
        "roomNo": 101,
        "capacity": 4,
        "rate": 15000,
        "floorNo": 1
    },

    {
        "roomNo": 102,
        "capacity": 3,
        "rate": 16000,
        "floorNo": 1
    },

    {
        "roomNo": 103,
        "capacity": 3,
        "rate": 16000,
        "floorNo": 1
    },

    {
        "roomNo": 201,
        "capacity": 4,
        "rate": 15000,
        "floorNo": 2
    },

    {
        "roomNo": 202,
        "capacity": 3,
        "rate": 16000,
        "floorNo": 2
    },

    {
        "roomNo": 203,
        "capacity": 3,
        "rate": 16000,
        "floorNo": 2
    },

    {
        "roomNo": 301,
        "capacity": 2,
        "rate": 17000,
        "floorNo": 2
    }
]


#route to login.html page
#NOTE: if you want to change function name, then also change in template.html file

@app.route("/")
def login():
    return render_template("login.html")

@app.route("/signup")
def signup():
    return render_template("signup.html")

@app.route("/searchroom")
def searchroom():
    return render_template("searchroom.html", availRooms=availRooms)


if __name__ == "__main__":
    app.run(debug=True)