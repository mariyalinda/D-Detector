# import parselmouth
# import numpy as np
# import os
# from scipy.stats import kurtosis,skew
# from pathlib import Path
# import sklearn

# from sklearn import preprocessing
# import keras

# import sys
# import math
# from tqdm import tqdm
# import matplotlib.pyplot as plt
# import seaborn as sns

# # def get_mfcc_val(files,mfcc_val,audio_count,healthy):
# def get_mfcc_val(path,healthy):
#     sound = parselmouth.Sound(path)
#     mfcc_object = sound.to_mfcc(number_of_coefficients=13,window_length = 0.015, time_step= 0.010, firstFilterFreqency= 100.0, distance_between_filters= 100.0)
#     mfcc_values=mfcc_object.to_array()
#     print(mfcc_values)

#     #calculating 8 statistical features as input features for ffnn
#     for i in range(len(mfcc_values)):
#         mfcc_val[i][0]   =  min(mfcc_values[i])                    
#         mfcc_val[i][1]   =  max(mfcc_values[i])                    
#         mfcc_val[i][2]   =  np.mean(mfcc_values[i])                
#         mfcc_val[i][3]   =  np.median(mfcc_values[i])              
#         mfcc_val[i][4]   =  np.std(mfcc_values[i])                 
#         mfcc_val[i][5]   =  max(mfcc_values[i])-min(mfcc_values[i])
#         mfcc_val[i][6]   =  kurtosis(mfcc_values[i],bias=False)    
#         mfcc_val[i][7]   =  skew(mfcc_values[i],bias=False)
#         mfcc_val[i][8]   =  healthy
    
#     return mfcc_val

# from keras.models import load_model

# def get_model(x):
#     model = load_model('ffnn_model_v1.h5') 
#     y_pred=model.predict(x)
#     y_pred
#     count=0
#     for i in range(len(y_pred)):
#         val=y_pred[i]
#         if val >= 0.5:
#             count=count+1
#     if count > 0.5 * len(y_pred):
#         return 1
#     else:
#         return 0

# if __name__ == "__main__":
#     path=Path(str(sys.argv[1]))
#     get_mfcc_val(path)

import parselmouth
import numpy as np
import os
from scipy.stats import kurtosis,skew
from pathlib import Path
import sklearn

from sklearn import preprocessing
import keras

import sys
import math
from tqdm import tqdm
import matplotlib.pyplot as plt
import seaborn as sns

import tensorflow as tf

'''

Extracting the mfcc features given the wave file path 

eg: snd = parselmouth.Sound("docs/examples/audio/the_north_wind_and_the_sun.wav")


ip wave_file : file path
op mfcc features np 2D array 

'''

def get_mfcc_val(wave_file,healthy):

        
    sound = parselmouth.Sound(wave_file)
    mfcc_object = sound.to_mfcc(number_of_coefficients=13,window_length = 0.015, time_step= 0.010, firstFilterFreqency= 100.0, distance_between_filters= 100.0)
    mfcc_values=mfcc_object.to_array()
    #print(mfcc_values)

    mfcc_val=np.zeros([len(mfcc_values) , 9] )

    #calculating 8 statistical features as input features for ffnn
    for i in range(len(mfcc_values)):
        mfcc_val[i][0]   =  min(mfcc_values[i])                    
        mfcc_val[i][1]   =  max(mfcc_values[i])                    
        mfcc_val[i][2]   =  np.mean(mfcc_values[i])                
        mfcc_val[i][3]   =  np.median(mfcc_values[i])              
        mfcc_val[i][4]   =  np.std(mfcc_values[i])                 
        mfcc_val[i][5]   =  max(mfcc_values[i])-min(mfcc_values[i])
        mfcc_val[i][6]   =  kurtosis(mfcc_values[i],bias=False)    
        mfcc_val[i][7]   =  skew(mfcc_values[i],bias=False)
        mfcc_val[i][8]   =  1
    
    return mfcc_val

'''

Loading keras model from path

ip mfcc feature x
op SLI patient or not (1/0)

'''

from keras.models import load_model

def get_model(mfcc_val):
    model = load_model('ffnn_model_v1.h5') 
    x  = mfcc_val[:,:9]
    y  = mfcc_val[:,8]
    y_pred=model.predict(x)
    y_pred
    count=0
    for i in range(len(y_pred)):
        val=y_pred[i]
        if val >= 0.5:
            count=count+1
    if count > 0.5 * len(y_pred):
        return 1
    else:
        return 0

# mfcc_val = get_mfcc_val(wave_file='test.wav',healthy)
# get_model(mfcc_val)

healthy=0
if __name__ == "__main__":
    path=Path(str(sys.argv[1]))
   
    mfcc_val=get_mfcc_val(path,healthy)
    get_model(mfcc_val)