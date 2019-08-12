


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