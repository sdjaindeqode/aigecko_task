import io
import os
import time
import hashlib
import re
import requests
from base64 import encodebytes
from PIL import Image, UnidentifiedImageError
from flask import render_template, flash, redirect, request, jsonify, send_from_directory
from ai_app import app, ALLOWED_EXTENSIONS


def allowed_file(filename):
    '''
    Used to check if file is valid or not.
    '''
    return '.' in filename and \
           filename.rsplit('.', 1)[1].lower() in ALLOWED_EXTENSIONS


def secure_filename(filename):
    '''
    Used to generate unique id for every file.
    '''
    curr_time = time.time()
    extension = filename.rsplit('.', 1)[1].lower()
    if not extension in ALLOWED_EXTENSIONS:
        extension = 'jpg' # only done when image is uploaded through url and do not have proper extension
    name = str(curr_time) + filename
    filename = hashlib.md5(name.encode('utf-8')).hexdigest() + '.' + extension
    return filename


@app.route('/')
def index():
    """
    This view renders the template for the ease of the user.
    Methods: GET
    url: '/'
    """
    return render_template('upload.html')


@app.route('/list_images', methods=['GET'])
def list_images():
    """
    This view returns the list of images already uploaded to server.
    Methods: GET
    url: '/list_images'
    """
    folder = app.config['UPLOAD_FOLDER']
    files = os.listdir(folder)
    encoded_response = []
    for file in files:
        temp = f'/uploads/{file}'
        encoded_response.append({'id': file.rsplit('.', 1)[0], 'image': temp})
    return jsonify({'file_list': encoded_response})


@app.route('/upload_image', methods=['POST'])
def upload_image():
    """
    This view is used when user uploads a file to server directly.
    Methods: POST
    url: '/upload_image'
    data: 'file1'
    """
    if 'file1' not in request.files:
        flash('No file part')
        return jsonify({'error': 'Please upload a file.'}), 400
    file1 = request.files['file1']
    if file1.filename == '':
        return jsonify({'error': 'Please upload a valid file.'}), 400
    if file1 and allowed_file(file1.filename):
        filename = secure_filename(file1.filename)
        file1.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
        file_id = filename.rsplit('.', 1)[0]
        return jsonify({'message': f'This is your uploaded image id: {file_id}'}), 201


@app.route('/upload_image/<path:url>', methods=['GET'])
def upload_by_link(url):
    """
    This view is used when user uploads a file to server using a url.
    Methods: GET
    url: '/upload_image/<path:url>'
    """
    try:
        response = requests.get(url)
    except Exception as e:
        return jsonify({'error': 'Please enter a valid url.'}), 400
    try:
        img = Image.open(io.BytesIO(response.content)).convert("RGB")
    except UnidentifiedImageError as e:
        return jsonify({'error': 'Please upload link of valid file.'}), 400
    filename = secure_filename(url)
    img.save(os.path.join(app.config['UPLOAD_FOLDER'], filename))
    file_id = filename.rsplit('.', 1)[0]
    return jsonify({'message': f'This is your uploaded image id: {file_id}'}), 201


@app.route('/analyse_image/<string:hash_id>', methods=['GET'])
def analyse_image(hash_id):
    """
    This view is used to analyse image of given id by user.
    Methods: GET
    url: '/analyse_image/<string:hash_id>'
    """
    if not re.findall(r"([a-fA-F\d]{32})", hash_id):
        return jsonify({'error': 'Please provide valid id.'}), 400
    folder = app.config['UPLOAD_FOLDER']
    filepath = f'{folder}/{hash_id}'
    for ext in ALLOWED_EXTENSIONS:
        if os.path.exists(filepath + '.'+ ext):
            filepath = filepath+ '.'+ ext
            break
    try:
        img = Image.open(filepath)
    except FileNotFoundError:
        return jsonify({'error': 'File not found with given id.'}), 400
    width, height = img.size
    return jsonify({'message': f'Width: {width} and Heigth: {height}'}), 200