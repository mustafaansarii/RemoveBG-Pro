import os
from flask import Flask, render_template, request, redirect, url_for, send_file
from rembg import remove
from PIL import Image
from io import BytesIO

app = Flask(__name__)
app.config['UPLOAD_FOLDER'] = './static/uploads'
app.secret_key = 'your_secret_key'

os.makedirs(app.config['UPLOAD_FOLDER'], exist_ok=True)


@app.route('/', methods=['GET', 'POST'])
def index():
    if request.method == 'POST':
        if 'image' not in request.files:
            return redirect(request.url)
        file = request.files['image']
        if file.filename == '':
            return redirect(request.url)

        input_path = os.path.join(app.config['UPLOAD_FOLDER'], file.filename)
        file.save(input_path)

        with open(input_path, 'rb') as img_file:
            img_data = img_file.read()
            output_data = remove(img_data)

        output_path = os.path.join(app.config['UPLOAD_FOLDER'], f'result-{file.filename}')
        with open(output_path, 'wb') as out_file:
            out_file.write(output_data)

        return render_template('index.html', original_image=file.filename, result_image=f'result-{file.filename}')

    return render_template('index.html', original_image=None, result_image=None)


@app.route('/download/<filename>')
def download_file(filename):
    file_path = os.path.join(app.config['UPLOAD_FOLDER'], filename)
    return send_file(file_path, as_attachment=True)


if __name__ == '__main__':
    app.run(debug=True)
