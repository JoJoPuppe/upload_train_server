import os
from flask import Flask, flash, request, redirect, render_template
from werkzeug.utils import secure_filename
import pathlib
from PIL import Image

app=Flask(__name__)

app.secret_key = "secret key"
app.config['MAX_CONTENT_LENGTH'] = 16 * 1024 * 1024

# Get current path
path = os.getcwd()
# file Upload
TRAINING_BASE_PATH = pathlib.Path(path)

# Allowed extension you can set your own
ALLOWED_EXTENSIONS = set(['png', 'jpg', 'jpeg', 'JPG'])


def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


@app.route('/')
def upload_form():
    return render_template('upload.html')


@app.route('/', methods=['POST'])
def upload_file():
    if request.method == 'POST':

        if 'files[]' not in request.files:
            flash('No file part')
            return redirect(request.url)

        files = request.files.getlist('files[]')
        for f in files:
            img = Image.open(f)  # load with Pillow
            if img.size[0] != img.size[1]:
                flash('images are not square aspect ratio!')
                return redirect(request.url)

        training_name = request.form.get("fname").lower() + request.form.get("lname").lower()

        training_path = pathlib.Path.joinpath(TRAINING_BASE_PATH, training_name)
        training_path.mkdir(parents=True, exist_ok=True)

# Make directory if uploads is not exists

        app.config['UPLOAD_FOLDER'] = training_path.absolute().as_posix()

        for file in files:
            if file and allowed_file(file.filename):
                filename = secure_filename(file.filename)
                file.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))

        flash('File(s) successfully uploaded')
        return redirect('/')


if __name__ == "__main__":
    app.run(host='127.0.0.1',port=5000,debug=True,threaded=True)
