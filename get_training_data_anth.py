from subprocess import call
import gdal
from gdalconst import *
from get_Training_ind_Mats import *
import libtiff
from scipy import ndimage
import matplotlib.pyplot as plt



def get_training_data():
    begin=1
    app = QgsApplication([],True)
    QgsApplication.setPrefixPath("/Applications/QGIS.app/Contents/MacOS", True)
    QgsApplication.initQgis()
    providers = QgsProviderRegistry.instance().providerList()
    begin=1
    for block_num in range(0,3):#types of training
        label=block_num
        (X_temp,Y_temp)=get_ind_image(block_num,'training.shp','RGB_im.tif','NIR_im.tif',label)
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
    return (X_train,Y_train)

