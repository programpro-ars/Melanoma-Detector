###################################################
# Real-Time Melanoma Detector                     #
# by Arseniy Arsentyev (programpro.ars@gmail.com) #
###################################################
import cv2
import numpy as np
import keras.models
from skimage.transform import resize

# capture webcam video
vid = cv2.VideoCapture(0)

# load model's weights from file
weights_file = "path to the fast-model.h5 file"
model = keras.models.load_model(weights_file)

# processing every frame
while not(cv2.waitKey(1) & 0xFF == ord('q')):
    # get a frame
    ret, frame = vid.read()
    # resize the image
    img = frame
    img = resize(img, (512, 512))
    img = 255 * img
    img = img.astype(np.uint8)
    arr = [img]
    arr = np.array(arr)
    # show the prediction
    if model.predict(arr, verbose=0) < 0.7:
        cv2.rectangle(frame, (0, 0), (120, 120), (0, 0, 255), -1)
    else:
        cv2.rectangle(frame, (0, 0), (120, 120), (0, 255, 0), -1)
    cv2.imshow('frame', frame)

# close the program's window
vid.release()
cv2.destroyAllWindows()
