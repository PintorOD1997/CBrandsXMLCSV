
from flask import Flask, render_template, request, Response, flash,send_from_directory
import os
import XMLtoCSV
from werkzeug.utils import secure_filename
app = Flask(__name__)
app.secret_key = "secret key"
path = os.getcwd()
UPLOAD_FOLDER = os.path.join(path, 'uploads')
if not os.path.isdir(UPLOAD_FOLDER):
    os.mkdir(UPLOAD_FOLDER)
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER

@app.route("/") #Decorador EndPoint a definir para las interacciones culeras
def home():
    uploadedFiles = os.listdir(app.config['UPLOAD_FOLDER'])
    for f in uploadedFiles:
        rem = os.path.join(UPLOAD_FOLDER, f)
        os.remove(rem)            
    return render_template("home.html")

@app.route("/convertir",methods=["POST"])
def upload():
    print(request.files)
    print(type(request.files))
    if 'files' not in request.files:
        flash('No file part')
    files = request.files.getlist("files")

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    XMLtoCSV.toCSV(app.config['UPLOAD_FOLDER'])
    uploadedFiles = os.listdir(app.config['UPLOAD_FOLDER'])
    out = os.path.join(app.config['UPLOAD_FOLDER'],"resultado.csv")
    send_from_directory(app.config['UPLOAD_FOLDER'], "resultado.csv",as_attachment = True)
    return send_from_directory(app.config['UPLOAD_FOLDER'], "resultado.csv",as_attachment = True)

@app.route("/convertInvoice",methods=["POST"])
def uploadInvoice():
    print(request.files)
    print(type(request.files))
    if 'files' not in request.files:
        flash('No file part')
    files = request.files.getlist("files")

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    XMLtoCSV.reduced_bill(app.config['UPLOAD_FOLDER'])
    uploadedFiles = os.listdir(app.config['UPLOAD_FOLDER'])
    out = os.path.join(app.config['UPLOAD_FOLDER'],"resultado.csv")
    send_from_directory(app.config['UPLOAD_FOLDER'], "resultado.csv",as_attachment = True)
    return send_from_directory(app.config['UPLOAD_FOLDER'], "resultado.csv",as_attachment = True)

@app.route("/convertPO",methods=["POST"])
def uploadPO():
    print(request.files)
    print(type(request.files))
    if 'files' not in request.files:
        flash('No file part')
    files = request.files.getlist("files")

    for file in files:
        filename = secure_filename(file.filename)
        file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    XMLtoCSV.purchase_order(app.config['UPLOAD_FOLDER'])
    uploadedFiles = os.listdir(app.config['UPLOAD_FOLDER'])
    out = os.path.join(app.config['UPLOAD_FOLDER'],"resultado.csv")
    send_from_directory(app.config['UPLOAD_FOLDER'], "resultado.csv",as_attachment = True)
    return send_from_directory(app.config['UPLOAD_FOLDER'], "resultado.csv",as_attachment = True)


if __name__ == '__main__':
   app.run()
