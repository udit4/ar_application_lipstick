

'''
from flask import Flask, jsonify, request
from PIL import Image 
from io import BytesIO
import base64
import config
import json


app = Flask(__name__)




#@app.route('/process/image/<string:color>/', methods=['GET'])
# def process_image(color)
@app.route(r'/process/image/', methods=['GET'])
def process_image():
    color_code = (34, 34, 178)
    alpha = 0.5
    output_image_base64 = config.tag_lips(request.get_data(), color_code, alpha)
    # return base64 bytes of image
    return output_image_base64



if __name__ == '__main__':
    app.run(debug=True)
'''

'''
from flask import Flask, render_template, Response
from camera import VideoCamera
from dlib import get_frontal_face_detector, shape_predictor



app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')

def gen(camera):
    
    while True:
        frame = camera.get_frame()
        yield (b'--frame\r\n'
               b'Content-Type: image/jpeg\r\n\r\n' + frame + b'\r\n\r\n')

@app.route('/video_feed')
def video_feed():
    detector = get_frontal_face_detector()
    predictor = shape_predictor('shape_predictor_68_face_landmarks.dat')
    return Response(gen(VideoCamera(detector, predictor)),
                    mimetype='multipart/x-mixed-replace; boundary=frame')

if __name__ == '__main__':
    app.run(host='192.168.24.82', debug=True)
'''



from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def index():
    return render_template('index.html')



if __name__ == '__main__':
    #app.run(host='192.168.24.82', debug=True)
    #app.run(host='127.0.0.1', debug=True)
    app.run(host='192.168.0.104', debug=True)