
from flask import Flask
from flask import render_template
from flask import request
from flask import send_file
import main
app=Flask (__name__)
@app.route ("/")
def upload ():

    return render_template ("file_upload.html")


@app.route("/success" ,methods=["POST"])
def success ():

    global link
    global channel
    link=str(request.form['lin'])
    return render_template('result.html',lin=link)


@app.route("/convert")
def flask():
    main.flask(link)
    return render_template("download.html")

@app.route("/download")
def download():
    filename='most_engaged_videos.csv'
    return send_file(filename,as_attachment=True)


#python -m flask --app .\app.py run
if __name__== "__main__":

    app.run (debug=True)