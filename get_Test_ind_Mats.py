import sys
from subprocess import call

import numpy as np
from calc_Inds_anth import *
import gdal
from gdalconst import *
import libtiff
import cv2



def get_test_mats(rgb_FILE,nir_FILE,calc_ind,ind_path):
    
    ds = gdal.Open(rgb_FILE,GA_ReadOnly)
    NIR_ds = gdal.Open(nir_FILE,GA_ReadOnly)

    cols = ds.RasterXSize
    rows = ds.RasterYSize
    offsetX=0
    offsetY=0
    bands = ds.RasterCount

    geotransform = ds.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]

    

   
    xOffset =10# int((cols) / pixelWidth)
    yOffset = 10#int((rows) / pixelHeight)

    rband=ds.GetRasterBand(1)
    gband=ds.GetRasterBand(2)
    bband=ds.GetRasterBand(3)
    nband=ds.GetRasterBand(4)




    rdata = rband.ReadAsArray(offsetX, offsetY,cols, rows).astype(np.float32)
    gdata=gband.ReadAsArray(offsetX, offsetY,cols, rows).astype(np.float32)
    bdata=bband.ReadAsArray(offsetX, offsetY,cols, rows).astype(np.float32)
    ndata=nband.ReadAsArray(offsetX, offsetY,cols, rows).astype(np.float32)

    rdata=rdata/(rdata.max())
    gdata=gdata/(gdata.max())
    bdata=bdata/(bdata.max())
    ndata=ndata/(ndata.max())
    
    
    mask = np.equal(rdata+gdata+bdata, 0)
    X_train=[]
    Y_train=[]
    begin=1
    for i in range (1,14):#####for over indices
        if calc_ind==1:
            write_raster_inds(ndata,rdata,gdata,bdata,0,i,rgb_FILE)#8,
        else:
            with rasterio.open(ind_path+'ind'+str(i)+'.tif') as src:
                im = src.read(1)
            im+=0.00001


        temp_i=np.ravel(im)
        temp_i=temp_i[~numpy.isinf(temp_i)]
        temp_i=temp_i[~numpy.isnan(temp_i)]
        # inds=np.where(temp_i!=np.nan)
        

        if begin==1:
            X_test=temp_i.T
            begin=0
        else:
            X_test=np.vstack((X_test,temp_i.T))


    return X_test.T
