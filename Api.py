import os
from flask import Flask, flash, request, redirect, url_for
from flask import send_from_directory
from werkzeug.utils import secure_filename
from detect_fake_videos import test_full_image_network 
from flask import jsonify
from convert import convert_avi_to_mp4
import random 
import warnings#
warnings.filterwarnings('ignore')

UPLOAD_FOLDER = 'path'
ALLOWED_EXTENSIONS = {'mp4'}

app = Flask(__name__)
app.secret_key = b'_5#y2L"F4Q8z\n\xec]/'
app.config['UPLOAD_FOLDER'] = UPLOAD_FOLDER


def allowed_file(filename):
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'],
                               filename)
@app.route('/result/<ress>/<vidn>')
def showres(ress,vidn):
    return jsonify(resault=ress,durl=vidn)


@app.route('/', methods=['GET', 'POST'])
def upload_file():
    if request.method == 'POST':
        # check if the post request has the file part
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        # if user does not select file, browser also
        # submit an empty part without filename
        if file.filename == '':
            flash('No selected file')
            return redirect(request.url)
        if file and allowed_file(file.filename):
            filename = secure_filename(file.filename)
            file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
            prediction = test_full_image_network(os.path.join(app.config['UPLOAD_FOLDER'], filename),'./models/final_model.p','./',False)
            print("The Fake Score is: " + str(prediction["score"]))
            print("Output video in: " + prediction["file"])
            rr=str(prediction["score"])
            Favi=filename.split('.')
            Favi=Favi[0]+".avi"
            #retval = os.getcwd()
            #print("Current working directory %s" % retval)
            vidname= filename.split('.')[0]+str(random.randint(1, 100))
            

            tt=convert_avi_to_mp4('./path/'+Favi, './path/'+vidname)
            mp4vid=vidname+".mp4"
            return redirect(url_for('showres',ress=rr,vidn=mp4vid))

           # return redirect(url_for('showres',ress='100',vidn='DF-2323.mp4'))

           # return jsonify(resault=str(prediction["score"]))
    return '''
    <!doctype html>
    <title>Upload new File</title>
    <h1>Upload new File</h1>
    <form method=post enctype=multipart/form-data>
      <input type=file name=file>
      <input type=submit value=Upload>
    </form> '''
if __name__ == '__main__':
    #app.run(debug=True)
    app.run(host='0.0.0.0', port=7070)
    #http://localhost:7070/home