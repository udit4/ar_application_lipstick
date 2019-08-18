





import cv2
import config 
from dlib import get_frontal_face_detector, shape_predictor

class VideoCamera(object):
    def __init__(self, detector, predictor):
        # Using OpenCV to capture from device 0. If you have trouble capturing
        # from a webcam, comment the line below out and use a video file
        # instead.
        self.video = cv2.VideoCapture(0)

        # If you decide to use video.mp4, you must have this file in the folder
        # as the main.py.
        # self.video = cv2.VideoCapture('video.mp4')

        # initializing the model
        self.detector = detector
        self.predictor = predictor

    def __del__(self):
        self.video.release()

    def get_frame(self):
        success, image = self.video.read()
        
        image = config.opencv_to_pil(image)
        image = config.pil_to_opencv(image)
        resized_image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)   
        
        #image_base64 = config.tag_lips(self.detector, self.predictor, image_base64, (34, 34, 178), 0.5)
        #image = config.base64_to_image(image_base64)
        #image = config.pil_to_opencv(image)
        #resized_image = cv2.resize(image, None, fx=0.5, fy=0.5, interpolation = cv2.INTER_LINEAR)
        # We are using Motion JPEG, but OpenCV defaults to capture raw images,
        # so we must encode it into JPEG in order to correctly display the
        # video stream.
        ret, jpeg = cv2.imencode('.jpg', resized_image)
        return jpeg.tobytes()