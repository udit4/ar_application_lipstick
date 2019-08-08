

from collections import OrderedDict
from dlib import get_frontal_face_detector, shape_predictor
import base64
from io import BytesIO
import cv2
from PIL import Image
import numpy as np
from imutils import face_utils


# detector and predictor 
detector = get_frontal_face_detector()
predictor = shape_predictor('shape_predictor_68_face_landmarks.dat')

# converting image to base64 string (encoding)
def image_to_base64(image):
    buff = BytesIO()
    image.save(buff, format='JPEG')
    image_string = base64.b64encode(buff.getvalue())
    return image_string

# converting base64 string to image (decoding)
def base64_to_image(data):
    buff = BytesIO(base64.b64decode(data))
    return Image.open(buff)

# convert PIL image to opencv image
def pil_to_opencv(image):
    return cv2.cvtColor(np.array(image), cv2.COLOR_RGB2BGR)

# convert opnecv image to pil
def opencv_to_pil(image):
    return Image.fromarray(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))


# method for coloring the lips 
def color_lips(frame, shape, color_code, alpha):
    overlay = frame.copy()
    output = frame.copy()
    
    pairs_indexes = [[50, 62, 61, 49], [51, 63, 62, 50], [52, 64, 63, 51], [52, 53, 54, 64],
                    [64, 54, 55, 65], [65, 55, 56, 66], [67, 66, 56, 57], [67, 66, 57, 58],
                    [68, 67, 58, 59], [61, 68, 59, 60], [49, 61, 68, 60]]
    
    for pair in pairs_indexes:
        coords = np.array( [[[shape[pair[0]-1][0], shape[pair[0]-1][1]], [shape[pair[1]-1][0], shape[pair[1]-1][1]], 
                [shape[pair[2]-1][0], shape[pair[2]-1][1]], [shape[pair[3]-1][0], shape[pair[3]-1][1]] ]])
        cv2.fillPoly(overlay, coords, color_code)
    
    #coords = np.array( [[[x_49, y_49], [x_50, y_50], [x_62, y_62], [x_61, y_61]]], dtype=np.int32)
    cv2.fillPoly(overlay, coords, color_code)
    cv2.addWeighted(overlay, alpha, output, 1-alpha, 0, output)
    return output



# tagging lips on the frame
def tag_lips(frame_base64, color_code, alpha):
    frame = base64_to_image(frame_base64)
    frame = pil_to_opencv(frame)
    #frame = cv2.resize(frame, None, fx=0.5, fy=0.5, interpolation=cv2.INTER_AREA)
    gray = cv2.cvtColor(frame, cv2.COLOR_BGR2GRAY)
    rects = detector(gray, 1)
    if len(rects) == 0:
        frame = opencv_to_pil(frame)
        return image_to_base64(frame)
    else:
        rects = rects[0]
        shape = predictor(gray, rects)
        shape = face_utils.shape_to_np(shape)
        for index, value in enumerate(shape):
            if index in range(48, 68):
                continue
            else:
                shape[index] = [0, 0]
        output = color_lips(frame, shape, color_code, alpha)
        output = opencv_to_pil(output)
        return image_to_base64(output)


# bgr color codes for different colors  
color_code = {
    'black':(0, 0, 0),
    'white':(255, 255, 255),
    'red':(0, 0, 255),
    'lime':(0, 255, 0),
    'blue':(255, 0, 0),
    'yellow':(0, 255, 255),
    'aqua':(255, 255, 0),
    'maroon':(0, 0, 128),
    'navy':(128, 0, 0),
    'dark-red':(0, 0, 139),
    'tomato':(71, 99, 255),
    'crimson':(60, 20, 200),
    'salmon':(114, 128, 250),
    'light-salmon':(122, 160, 255),
    'orange':(0, 165, 255),
    'gold':(0, 215, 255),
    'yellow-green':(50, 2015, 154),
    'lawn-green':(0, 252, 124),
    'turquoise':(208, 224, 64),
    'sky-blue':(235, 206, 135),
    'light-blue':(230, 216, 173),
    'indigo':(130, 0, 75),
    'pink':(180, 105, 255),
    'deep-pink':(147, 20, 255),
    'chocolate':(30, 105, 210)

}

