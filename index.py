from flask import Flask, render_template, request, redirect, flash, url_for
import main
import urllib.request
from app import app
from werkzeug.utils import secure_filename
from main import getPrediction
import os
import cv2
import tensorflow as tf

 # physical_devices = tf.config.list_physical_devices('GPU') 
 # tf.config.experimental.set_memory_growth(physical_devices[0], True)


@app.route('/')
def index():
    return render_template('index.html')


@app.route('/', methods=['GET','POST'])
def submit_file():
    if request.method == 'POST':
        if 'file' not in request.files:
            flash('No file part')
            return redirect(request.url)
        file = request.files['file']
        if file.filename == '':
            flash('No file selected for uploading')
            return redirect(request.url)
        if file:
            file.save(secure_filename(file.filename))
            vidcap = cv2.VideoCapture(file.filename)
            success, image = vidcap.read()
            num = 0
            
            while success:
                cv2.imwrite("uploads/image%d.jpg"%num, image)     # save frame as JPEG file      
                success,image = vidcap.read()
                num += 1
                break
                
            for i in range(num):
                image = "uploads/image{}.jpg".format(i)
                label, acc = getPrediction(image)
                flash(label)
                flash(acc)
            
                break
        return redirect('/')


if __name__ == "__main__":
    app.run()