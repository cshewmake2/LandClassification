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



def get_ind_image(sel_num,mask_path,rgb_FILE,nir_FILE,label):
    mask=QgsVectorLayer(mask_path,'mask','ogr')
    expr = QgsExpression( 'id='+str(sel_num) )
    it = mask.getFeatures( QgsFeatureRequest( expr ) )
    ids = [i.id() for i in it]
    print ids
                 
                 
                 
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
    out=os.system('gdalwarp -cutline mask_sel.shp  -crop_to_cutline ' +rgb_FILE+' rgb_cut.tif')
####read cut tiff file 
##RGB_cut= QgsRasterLayer(Proj_Path+'cut.tif','RGB_cut')
##QgsMapLayerRegistry.instance().addMapLayer(RGB_cut)

    out=os.system('gdalwarp -cutline mask_sel.shp  -crop_to_cutline ' +nir_FILE+' NIR_cut.tif')
    NIR_cut= QgsRasterLayer('NIR_cut.tif','NIR_cut')
    QgsMapLayerRegistry.instance().addMapLayer(NIR_cut)
    

    ds = gdal.Open('rgb_cut.tif',GA_ReadOnly)
    NIR_ds = gdal.Open('NIR_cut.tif',GA_ReadOnly)

    cols = ds.RasterXSize
    rows = ds.RasterYSize
    bands = ds.RasterCount

    geotransform = ds.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3]
    pixelWidth = geotransform[1]
    pixelHeight = geotransform[5]



    NIR_geotransform = NIR_ds.GetGeoTransform()
    nband=NIR_ds.GetRasterBand(1)
    

    
    ndata = nband.ReadAsArray(0, 0,cols, rows).astype(np.float32)
    

    ndata=ndata/(ndata.max())
    xOffset =10# int((cols) / pixelWidth)
    yOffset = 10#int((rows) / pixelHeight)

    rband=ds.GetRasterBand(1)
    gband=ds.GetRasterBand(2)
    bband=ds.GetRasterBand(3)




    rdata = rband.ReadAsArray(0, 0,cols, rows).astype(np.float32)
    gdata=gband.ReadAsArray(0, 0,cols, rows).astype(np.float32)
    bdata=bband.ReadAsArray(0, 0,cols, rows).astype(np.float32)

    rdata=rdata/(rdata.max())
    gdata=gdata/(gdata.max())
    bdata=bdata/(bdata.max())
    
    mask = np.equal(rdata+gdata+bdata, 0)
    X_train=[]
    Y_train=[]
    begin=1
    for i in range (0,9):#####for over indices
        write_raster_inds(ndata,rdata,gdata,bdata,ds,i,cols,rows)#8,
        # ind_image= QgsRasterLayer('ind.tif', 'ind_image')
    
    

# IOError: cannot identify image file

        tif = libtiff.TIFF.open('ind.tif')
        im = tif.read_image()
        temp_i=np.ravel(im)
        temp_i=temp_i[~numpy.isinf(temp_i)]
        inds=np.where(temp_i!=np.nan)
        
        



        
#  im=im*255.0
# cv2.imwrite('ind_'+str(i)+'_'+str(sel_num)+'.jpg',im)
        if begin==1:
            X_train=temp_i.T
            begin=0
        else:
            X_train=np.vstack((X_train,temp_i.T))

    Y_train=label*np.ones(np.size(temp_i))
    out=os.system('rm '+'NIR_cut.tif')
    out=os.system('rm '+'rgb_cut.tif')
    return (X_train.T,Y_train)
