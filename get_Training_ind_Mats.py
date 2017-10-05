import sys
sys.path.append("/Users/Golnoosh/Desktop/Internship/Libraries_in_usage/pyshp-master")
from subprocess import call
import gdal
from gdalconst import *
import numpy as np
from calc_Inds_anth import *

import libtiff
import cv2
import scipy.io as sio
import rasterio
import shapefile



def get_ind_image(sel_num,mask_path,rgb_FILE,nir_FILE,label,ind_path,calc_ind):
    mask=shapefile.Reader(mask_path)
    records = mask.records()
    shp_writer= shapefile.Writer(shapefile.POLYGON)
    
    fields = mask.fields
    shp_fields = shp_writer.fields
    
    for name in fields:
        if type(name) == "tuple":
            continue
        else:
            args = name
            shp_writer.field(*args)
            
    for shaperec in mask.iterShapeRecords():
        
        if int(shaperec.record[1])==sel_num:
            print shaperec.record
            shp_writer.record(*shaperec.record)
            shp_writer.shape(shaperec.shape)
    shp_writer.save('mask_sel.shp')
  
#                 
#                 


#QgsMapLayerRegistry.instance().addMapLayer(mask_sel)
####burn mask_sel_to another raster
    
    ds = gdal.Open(rgb_FILE,GA_ReadOnly)
    cols = ds.RasterXSize
    rows = ds.RasterYSize
    rband=ds.GetRasterBand(1)
    gband=ds.GetRasterBand(2)
    bband=ds.GetRasterBand(3)
    nband=ds.GetRasterBand(4)
    
    
    rdata = rband.ReadAsArray(0, 0,cols, rows).astype(numpy.float32)
    gdata=gband.ReadAsArray(0, 0,cols, rows).astype(numpy.float32)
    bdata=bband.ReadAsArray(0, 0,cols, rows).astype(numpy.float32)
    ndata = nband.ReadAsArray(0, 0,cols, rows).astype(numpy.float32)
    

    rdata=rdata/(rdata.max())
    gdata=gdata/(gdata.max())
    bdata=bdata/(bdata.max())
    ndata=ndata/(ndata.max())
    
    X_train=[]
    Y_train=[]
    begin=1
    for i in range (1,14):#####for over indices
        if calc_ind==1:
            write_raster_inds(ndata,rdata,gdata,bdata,0,i,rgb_FILE)#8,
        else:
            tif = libtiff.TIFF.open(ind_path+'ind'+str(i)+'.tif')
            with rasterio.open(ind_path+'ind'+str(i)+'.tif') as src:
                im = src.read(1)
            print im.shape

            im+=0.00001
            src = rasterio.open(rgb_FILE)
            new_dataset =rasterio.open('Ind'+str(i)+'.tif','w',driver='Gtiff',height=im.shape[0], width=im.shape[1],count=1, dtype=str(im.dtype),crs=src.crs,transform=src.transform)
            new_dataset.write(im, 1)
            new_dataset .close()

        out=os.system('gdalwarp -cutline mask_sel.shp  -crop_to_cutline '+'ind'+str(i)+'.tif rgb_cut.tif')
        tif = libtiff.TIFF.open('rgb_cut.tif')
        im = tif.read_image()
        mask2=np.equal(im,0)
        im[mask2]=np.inf
        
        temp_i=np.ravel(im)
        temp_i=temp_i[~numpy.isinf(temp_i)]
        temp_i=temp_i[~numpy.isnan(temp_i)]
        inds=np.where(temp_i!=np.nan)

        if begin==1:
            X_train=temp_i.T
            begin=0
        else:
            X_train=np.vstack((X_train,temp_i.T))
            
        sio.savemat('train_data.mat',{'X_train':X_train})
 
        out=os.system('rm '+'rgb_cut.tif')
        
    Y_train=label*np.ones(np.size(temp_i))
    return (X_train.T,Y_train)
