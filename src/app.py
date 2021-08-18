import os
from flask import Flask, request, jsonify, render_template
from flask_sqlalchemy import SQLAlchemy
from flask import render_template, redirect, send_file
from datetime import datetime
from PIL import Image
import pytz
app = Flask(__name__)

app.config.from_object(os.environ['APP_SETTINGS'])
app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False
# UPLOAD_FOLDER = "./static/uploads"
UPLOAD_FOLDER = os.path.join("static","uploads")
ALLOWED_EXTENSIONS = {'txt', 'pdf', 'png', 'jpg', 'jpeg', 'gif'}
app.config["UPLOAD_FOLDER"] = UPLOAD_FOLDER
app.config['MAX_CONTENT_LENGTH'] = 1 * 1024 * 1024 
db = SQLAlchemy(app)

from models import Pics

def page_not_found(error):
    return redirect("/" , code=302)
def request_entity_too_large(error):
    return ('File Too Large')
app.register_error_handler(413, request_entity_too_large)
app.register_error_handler(404, page_not_found)

@app.route("/")
def home():
    # return "Hello World!"
    return render_template(
            "index.html",
            link=None,
            name = None
        )

@app.route("/upload", methods=["POST"])
def upload():
    if request.method == 'POST': 
        if request.files is None or "Select File" not in request.files:
            return ("Please upload a valid file.",422) 
        f = request.files['Select File']  
        if f is None:
            return "Error: Provide a valid file"
        name=f.filename
        if name.split(".")[1] not in ALLOWED_EXTENSIONS:
            return "Error: Invalid File Extention"
        name=name.replace(" ","_")
        file_name=os.path.join(app.config['UPLOAD_FOLDER'], name)
        f.save(file_name) 

        image_data = Image.open(file_name)
        print(image_data.size)
        resolution = "x".join([str(v) for v in image_data.size])
         
        details = {
            "type":f.filename.split(".")[-1],
            "resolution": resolution,
            "upload_time": datetime.now(pytz.timezone("Asia/Kolkata")).strftime("%Y-%m-%d %H:%M:%S")
        }
        # details["file_size"]=os.stat(file_name).st_size

        try:
            pic=Pics(
                name=name,
                details=details
            )
            db.session.add(pic)
            db.session.commit()
            # return redirect("/view/" + str(pic.id), code=302)
            # return render_template("index.html",link=pic.id,name = name)
            return request.url_root+"view/"+str(pic.id)
        except Exception as e:
    	    return(str(e))


@app.route('/download/<filename>')
def return_files_tut(filename):
    file_path = UPLOAD_FOLDER + filename
    return send_file(file_path, as_attachment=True, attachment_filename='')

@app.route("/list")
def get_all():
    try:
        pics=Pics.query.filter_by(status = True).all()
        if pics is not None:
            # pics = [dict(pic) for pic in pics]
            return render_template("list.html",pics=pics)
        else:
            return redirect("/" , code=302) 
    except Exception as e:
	    return(str(e))

@app.route("/view/<id_>")
def view(id_):
    try:
        pic=Pics.query.filter_by(id=id_,status=True).first()
        if pic is not None:
            return render_template("view.html",name=pic.name,details= pic.details)
        else:
            return redirect("/" , code=302)

    except Exception as e:
	    return(str(e))

if __name__ == '__main__':
    app.run()
