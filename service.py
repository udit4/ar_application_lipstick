


from flask import Flask, render_template
from flask_socketio import SocketIO
from flask_socketio import send, emit 
from dlib import get_frontal_face_detector, shape_predictor
import time 
from PIL import Image
from io import BytesIO
import base64

app = Flask(__name__)
socketio = SocketIO(app)

global detector 
global predictor 


# converting base64 string to image (decoding)
def base64_to_image(data):
    data += "=" * ((4 - len(data) % 4) % 4)
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)

@socketio.on('connection_successful')
def method(data):
    print(str(data))
    tic = time.time()
    detector = get_frontal_face_detector()
    predictor = shape_predictor('shape_predictor_68_face_landmarks.dat')
    toc = time.time()
    emit('model_loaded', 'Model Loaded :: ' + str(float(toc-tic)) + ' seconds')


@socketio.on('video_streaming')
def process(data):
    emit('frame_from_server', data)



# function for rendering the html response page
@app.route('/')
def index():
    return render_template('service.html')



if __name__ == '__main__':
    app.run(host='192.168.0.103', debug=True)
