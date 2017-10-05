from subprocess import call

from get_Training_ind_Mats import *
import libtiff
from scipy import ndimage
import matplotlib.pyplot as plt
import scipy.io as sio



def get_training_data():
    begin=1
    ind_path="inds/"
    for block_num in range(1,6):#types of training
        label=block_num
        (X_temp,Y_temp)=get_ind_image(block_num,'training1.shp','RGB_im.tif','NIR_im.tif',label,ind_path,0)
        if begin==1:
            X_train=X_temp
            Y_train=Y_temp
            begin=0
        else:
            print "tteeemmpppp_ssiizzeee"
            print block_num
            print X_train.shape
            print (X_temp.shape)
            X_train=np.vstack((X_train,X_temp))
        # X_train=np.append(X_train,X_temp,0)
            Y_train=np.hstack((Y_train,Y_temp))
            print "ttrraaaiiinnn_ssiizzeee"
        print (Y_train.shape)
    sio.savemat('train_data.mat',{'X_train':X_train,'Y_train':Y_train})

    return (X_train,Y_train)

