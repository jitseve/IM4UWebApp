from flask import Flask, render_template, request, redirect, session, url_for
from werkzeug.utils import secure_filename
import main_processor
import os


app = Flask(__name__)  # Initializing app from flask class
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

# Create set of routes (endpoints in website)


@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")


# Todo: this might become different if on a server
app.config["CSV_UPLOADS"] = "/home/jitseve/Documents/q1-project_course/im4u_web/uploads"
app.config["ALLOWED_EXTENSIONS"] = ["CSV", "JSON"]


@app.route("/upload_csv", methods=['GET', 'POST'])
def upload_csv():

    if request.method == "POST":

        if request.files:
            csv = request.files["csv"]

            if csv.filename == "":
                print("CSV must have a filename")
                return redirect(request.url)

            if not allowed_file(csv.filename):
                print("That filename extension is not allowed")
                return redirect(request.url)

            else:
                filename = secure_filename(csv.filename)
                csv.save(os.path.join(app.config["CSV_UPLOADS"], filename))
                print("CSV saved")
                return redirect("/result")

    return render_template("upload_csv.html")


@app.route("/result", methods=['POST', 'GET'])
def result():
    # Todo: run our python code here based on the name that we get in
    # Todo: maybe output the name of the picture locations in the return
    im1, im2, im3 = main_processor.run()

    return render_template("result.html", IMAGE1=im1, IMAGE2=im2, IMAGE3=im3)


def allowed_file(filename):
    if not "." in filename:
        return False

    ext = filename.rsplit(".", 1)[1]

    if ext.upper() in app.config["ALLOWED_EXTENSIONS"]:
        return True
    else:
        return False


@app.route('/recorddata')
def recorddata():
    return render_template("recorddata.html")


if __name__ == '__main__':
    app.run(debug=True, port=5001)
