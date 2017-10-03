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
import scipy.io as sio
import rasterio



def get_ind_image(sel_num,mask_path,rgb_FILE,nir_FILE,label):
    mask=QgsVectorLayer(mask_path,'mask','ogr')
    expr = QgsExpression( 'Classvalue='+str(sel_num) )
    it = mask.getFeatures( QgsFeatureRequest( expr ) )
    ids = [i.id() for i in it]
    print ids
    crs = mask.crs() 
#                 
#                 
    mask.setSelectedFeatures( ids )
    res = QgsVectorFileWriter.writeAsVectorFormat( mask,
        'mask_sel.shp',
        'System',
         None, #crs
         'ESRI Shapefile',
         True #onlySelected
         )




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
    for i in range (1,6):#####for over indices
        write_raster_inds(ndata,rdata,gdata,bdata,0,i,rgb_FILE)#8,
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
        hhh
    Y_train=label*np.ones(np.size(temp_i))
    
    return (X_train.T,Y_train)
