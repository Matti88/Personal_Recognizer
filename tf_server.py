
"""


This is a project initiated and developed by Matteo Montanari
Copyright (C) 2016 Matteo Montanari <matteo.montanari25@gmail.com>
-------------------------------------------------------------
"""

from flask import Flask, current_app, render_template, jsonify, request, make_response
from os import listdir
from os.path import isfile, join
import tensorflow as tf
import sys
import numpy
import os

current_path = os.path.dirname(os.path.abspath(__file__))

class Neural_Network_Usage:

    def __init__(self):

        self.control = 0
        self._ = None
        self.label_lines = []
        self.graph_def = None

    def model_parameters_loader(self):

        # Loads label file, strips off carriage return
        self.label_lines = [line.rstrip() for line in tf.gfile.GFile(current_path + "/output_labels.txt")]
        # Insert your model into the above function
        with tf.gfile.FastGFile(current_path + "/output_graph.pb", 'rb') as f:
            self.graph_def = tf.GraphDef()
            self.graph_def.ParseFromString(f.read())
            self._ = tf.import_graph_def(self.graph_def, name='')
        #print(self._)



    def model_interogator(self, image_path= current_path +  "/img.jpg"):
        # Read in the image_data
        image_data = tf.gfile.FastGFile(image_path, 'rb').read()
        with tf.Session() as sess:
            # KeyError: "The name 'final_result:0' refers to a Tensor which does not exist. The operation, 'final_result', does not exist in the graph."
            # Feed the image_data as input to the graph and get first prediction
            softmax_tensor = sess.graph.get_tensor_by_name('final_result:0')
    
            predictions = sess.run(softmax_tensor,  {'DecodeJpeg/contents:0': image_data})
    
            # Sort to show labels of first prediction in order of confidence
            top_k = predictions[0].argsort()[-len(predictions[0]):][::-1]
            #print(type(top_k))
            node_id = top_k[0]
            human_string = self.label_lines[node_id]
            score = predictions[0][node_id]
            print('%s (score = %.5f)' % (human_string, score))
            return human_string

print("Loading the Model...")        
example = Neural_Network_Usage()
example.model_parameters_loader()
print("Model LOADED!!!")

human_string = "None"

app = Flask(__name__)

app.config['ALLOWED_EXTENSIONS'] = set(['jpeg', 'jpg'])

@app.route('/')
def homepage():
    return  render_template('prompt_pict.html' )


@app.route('/getdata', methods=['GET'])
def get_data():
    global human_string
    if human_string == "None":
        return "Null"
    else:
        return_string = human_string
        human_string = "None"
        print(return_string)
        return return_string

def allowed_file(filename):
    return '.' in filename and filename.rsplit('.')[1] in app.config['ALLOWED_EXTENSIONS']


@app.route('/upload', methods=['POST'])
def upload_files():
    global human_string
    print("by the request")
    file = request.files['image']
    print(type(file))

    if file and allowed_file(file.filename):
        file.save(os.path.join(current_path, 'image_test.jpg'))
        type_of_trash = current_path +  "/" + 'image_test.jpg'
        human_string = example.model_interogator(image_path= type_of_trash)
        print(human_string)
        return  human_string
    else:
        return "Error"

@app.route('/getid', methods=['GET'])
def getid():
    return  "image_server"    

if __name__ == "__main__":
    app.run(host= '0.0.0.0')























