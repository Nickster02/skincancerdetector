import tensorflow as tf
from tensorflow import keras
from keras.models import load_model
import numpy as np


class SkinCancerDetector:
    
    def __init__(self,path='model/model.h5'):

        self.classes = {0: ('akiec', 'actinic keratoses and intraepithelial carcinomae'),  
           1:('bcc' , ' basal cell carcinoma'), 
           2 :('bkl', 'benign keratosis-like lesions'), 
           3: ('df', 'dermatofibroma'),
           4: ('nv', ' melanocytic nevi'), 
           5: ('vasc', ' pyogenic granulomas and hemorrhage'), 
           6: ('mel', 'melanoma')}
        
        self.model=load_model(path)


    def predict(self,path):
        image_open = open(path, 'rb')
        read_image = image_open.read()
        decoded = tf.image.decode_jpeg(read_image)
        image = tf.image.resize(decoded, [28,28])
        final_image=image.numpy()
        final_image=np.reshape(final_image,(1,28,28,3))
        final_image/=255.0
        prediction=self.model(final_image,training=False)
        max_prob=max(prediction[0])
        predicted_class=list(prediction[0]).index(max_prob)
        return self.classes[predicted_class]
