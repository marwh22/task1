import os
from flask import Flask, render_template, request, url_for
from flask_wtf import FlaskForm 
from werkzeug.utils import secure_filename
from wtforms import FileField
from PIL import Image

app = Flask(__name__)

app.config['UPLOAD_FOLDER'] = 'uploads'
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024
app.config['SECRET_KEY'] = 'secret key'

class UploadForm(FlaskForm):
    image_file = FileField('Image File')

@app.route('/', methods=['GET', 'POST'])  
def upload():
    form = UploadForm()
    if form.validate_on_submit():
       f = form.image_file.data
       filename = secure_filename(f.filename)
       f.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
      
       img = convert_to_grayscale(filename)
      
       return render_template('index.html',  
                               img_filename = filename,     
                               gray_img_filename = img) 
    return render_template('index.html', form=form)

def convert_to_grayscale(filename):
    img = Image.open(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    img = img.convert("L")
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], "gray_" + filename))
    return "gray_" + filename

if __name__ == '__main__':
   app.run(debug = True)