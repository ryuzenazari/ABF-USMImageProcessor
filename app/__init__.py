import os
from flask import Flask

app = Flask(__name__)
app.config['SECRET_KEY'] = 'rahasia-aplikasi-peningkatan-gambar'
app.config['UPLOAD_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/uploads')
app.config['RESULT_FOLDER'] = os.path.join(os.path.dirname(os.path.abspath(__file__)), 'static/results')

def create_storage_directories():
    for folder in [app.config['UPLOAD_FOLDER'], app.config['RESULT_FOLDER']]:
        if not os.path.exists(folder):
            os.makedirs(folder)

create_storage_directories()

from app import routes