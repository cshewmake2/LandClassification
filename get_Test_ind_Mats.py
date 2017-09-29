import sys
sys.path.append("/Applications/QGIS.app/Contents/Resources/python")
from subprocess import call
import gdal
from gdalconst import *
import numpy as np
from calc_Inds_anth import *
from qgis.core import *
import libtiff
import cv2



def get_test_mats(rgb_FILE,nir_FILE):
    
    ds = gdal.Open(rgb_FILE,GA_ReadOnly)
    NIR_ds = gdal.Open(nir_FILE,GA_ReadOnly)

    cols = 7000#ds.RasterXSize
    rows = 3000#ds.RasterYSize
    bands = ds.RasterCount

    geotransform = ds.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]



    NIR_geotransform = NIR_ds.GetGeoTransform()
    nband=NIR_ds.GetRasterBand(1)
    


    ndata = nband.ReadAsArray(1000, 2000,cols, rows).astype(np.float32)
    

    ndata=ndata/(ndata.max())
    xOffset =10# int((cols) / pixelWidth)
    yOffset = 10#int((rows) / pixelHeight)

    rband=ds.GetRasterBand(1)
    gband=ds.GetRasterBand(2)
    bband=ds.GetRasterBand(3)




    rdata = rband.ReadAsArray(500, 2000,cols, rows).astype(np.float32)
    gdata=gband.ReadAsArray(500, 2000,cols, rows).astype(np.float32)
    bdata=bband.ReadAsArray(500, 2000,cols, rows).astype(np.float32)

    rdata=rdata/(rdata.max())
    gdata=gdata/(gdata.max())
    bdata=bdata/(bdata.max())
    
    mask = np.equal(rdata+gdata+bdata, 0)
    X_train=[]
    Y_train=[]
    begin=1
    for i in range (0,9):#####for over indices
        write_raster_inds(ndata,rdata,gdata,bdata,ds,i,cols,rows)#8,

        tif = libtiff.TIFF.open('ind.tif')
        im = tif.read_image()
        cv2.imwrite('ind.jpg',im)
        temp_i=np.ravel(im)
        temp_i=temp_i[~numpy.isinf(temp_i)]
        inds=np.where(temp_i!=np.nan)
        

        if begin==1:
            X_test=temp_i.T
            begin=0
        else:
            X_test=np.vstack((X_test,temp_i.T))


    return X_test.T
