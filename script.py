

import base64
from PIL import Image
from io import BytesIO
import requests
import config
from ast import literal_eval

# result from the image API
def procees_frame(data):
    url = "http://localhost:5000/process/image/"
    payload = data
    headers = {
        'cache-control': "no-cache",
        'Postman-Token': "493db090-1235-4ee3-8b41-03014818e5c4"
        }
    response = requests.request("GET", url, data=payload, headers=headers)
    return literal_eval(response.text).get('result')


img_path = r'/Users/uditgera-air/Desktop/object_detection_test.jpg'

image = Image.open(img_path).convert('RGB')

image_base64 = config.image_to_base64(image)

output_image_base64 = procees_frame(image_base64)

output_image = config.base64_to_image(output_image_base64)

output_image.show()
