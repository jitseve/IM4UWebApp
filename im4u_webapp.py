from flask import Flask, render_template, request, session, send_file
import main_processor

app = Flask(__name__) #Initializing app from flask class
app.secret_key = 'dljsaklqk24e21cjn!Ew@@dsa5'

#Create set of routes (endpoints in website)
@app.route("/")
@app.route("/home")
def home():
    return render_template("home.html")

@app.route("/result", methods = ['POST', 'GET'])
def result():
    #Todo: run our python code here based on the name that we get in
    #Todo: maybe output the name of the picture locations in the return
    output = request.form.to_dict()
    expnumber = output["expnumber"]
    im1, im2, im3 = main_processor.run(experimentnumber=expnumber)

    session["expnumber"] = expnumber

    return render_template("home.html", expnumber=expnumber, IMAGE1=im1, IMAGE2=im2, IMAGE3=im3)


if __name__ == '__main__':
    app.run(debug=True, port=5001)