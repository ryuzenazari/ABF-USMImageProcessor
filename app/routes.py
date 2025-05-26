import os
import secrets
import numpy as np
import cv2
from flask import (
    render_template, 
    request, 
    redirect, 
    url_for, 
    flash, 
    send_from_directory
)
from werkzeug.utils import secure_filename
from app import app
from app.utils.image_processor import process_image, process_image_with_unsharp_mask

ALLOWED_EXTENSIONS = {'png', 'jpg', 'jpeg', 'gif', 'bmp', 'tiff'}

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS

def calculate_histogram(image_path):
    img = cv2.imread(image_path)
    
    if img is None:
        return [0] * 8, [0] * 8, [0] * 8
    
    hist_r = cv2.calcHist([img], [2], None, [8], [0, 256])
    hist_g = cv2.calcHist([img], [1], None, [8], [0, 256])
    hist_b = cv2.calcHist([img], [0], None, [8], [0, 256])
    
    cv2.normalize(hist_r, hist_r, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist_g, hist_g, 0, 1, cv2.NORM_MINMAX)
    cv2.normalize(hist_b, hist_b, 0, 1, cv2.NORM_MINMAX)
    
    hist_r_list = [round(float(val[0]), 2) for val in hist_r]
    hist_g_list = [round(float(val[0]), 2) for val in hist_g]
    hist_b_list = [round(float(val[0]), 2) for val in hist_b]
    
    return hist_r_list, hist_g_list, hist_b_list

def save_uploaded_file(file):
    filename = secure_filename(file.filename)
    random_hex = secrets.token_hex(8)
    _, file_ext = os.path.splitext(filename)
    unique_filename = random_hex + file_ext
    
    input_path = os.path.join(app.config['UPLOAD_FOLDER'], unique_filename)
    file.save(input_path)
    
    return unique_filename, input_path

@app.route('/', methods=['GET'])
def index():
    return render_template('index.html')

@app.route('/process', methods=['POST'])
def process():
    if 'image' not in request.files:
        flash('Tidak ada file yang dipilih')
        return redirect(request.url)
    
    file = request.files['image']
    
    if file.filename == '':
        flash('Tidak ada file yang dipilih')
        return redirect(request.url)
    
    if not allowed_file(file.filename):
        flash('Format file tidak didukung. Gunakan PNG, JPG, JPEG, GIF, BMP, atau TIFF.')
        return redirect(url_for('index'))
    
    unique_filename, input_path = save_uploaded_file(file)
    
    abf_output_filename = f"abf_{unique_filename}"
    abf_output_path = os.path.join(app.config['RESULT_FOLDER'], abf_output_filename)
    
    usm_output_filename = f"usm_{unique_filename}"
    usm_output_path = os.path.join(app.config['RESULT_FOLDER'], usm_output_filename)
    
    params = {}
    
    abf_success, abf_message = process_image(input_path, abf_output_path, params)
    usm_success, usm_message = process_image_with_unsharp_mask(input_path, usm_output_path, params)
    
    if not (abf_success and usm_success):
        error_message = abf_message if not abf_success else usm_message
        flash(f'Error: {error_message}')
        return redirect(url_for('index'))
    
    orig_hist_r, orig_hist_g, orig_hist_b = calculate_histogram(input_path)
    abf_hist_r, abf_hist_g, abf_hist_b = calculate_histogram(abf_output_path)
    usm_hist_r, usm_hist_g, usm_hist_b = calculate_histogram(usm_output_path)
    
    return render_template(
        'result.html', 
        input_image=unique_filename, 
        abf_output_image=abf_output_filename,
        usm_output_image=usm_output_filename,
        orig_hist_r=orig_hist_r,
        orig_hist_g=orig_hist_g,
        orig_hist_b=orig_hist_b,
        abf_hist_r=abf_hist_r,
        abf_hist_g=abf_hist_g,
        abf_hist_b=abf_hist_b,
        usm_hist_r=usm_hist_r,
        usm_hist_g=usm_hist_g,
        usm_hist_b=usm_hist_b,
        message="Gambar berhasil diproses dengan kedua filter"
    )

@app.route('/uploads/<filename>')
def uploaded_file(filename):
    return send_from_directory(app.config['UPLOAD_FOLDER'], filename)

@app.route('/results/<filename>')
def result_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename)

@app.route('/download/<filename>')
def download_file(filename):
    return send_from_directory(app.config['RESULT_FOLDER'], filename, as_attachment=True)