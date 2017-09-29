import numpy
import math
import os, sys, ogr
from osgeo import gdal
from gdalconst import *



def write_raster_inds(n,r,g,b,ds,sel,cols,rows):
    print sel
    gam=1.7
    bsize=min(cols,rows)/10
    print bsize

    geotransform = ds.GetGeoTransform()
    originX = geotransform[0]
    originY = geotransform[3] 
    mask = numpy.greater(n+r+g+b, 0)
    if sel==0:#DVI
        # print 0
        inds = numpy.choose(mask, (0,n-r))
    elif sel==1:##NDVI
        inds=numpy.choose(mask, (0,(n-r)/(n+r)))
    elif sel==2:#GARI
        inds=numpy.choose(mask, (0,(n-(g-gam*(b-r)))/(n+(g-gam*(b-r)))))
    elif sel==3:#GNDVI
        inds=numpy.choose(mask, (0,(n-g)/(n+g)))
        
    elif sel==4:#OSAVI
        inds=numpy.choose(mask, (0,1.5*(n-r)/(n+r+0.16)))
    elif sel==5:#RDVI
        inds=numpy.choose(mask, (0,(n - r)/numpy.sqrt(n + r)))
    elif sel==6: #RVI
        inds= numpy.choose(mask, (0,n/r))
    elif sel==7:#SAVI
        inds=numpy.choose(mask,(0,1.5*(n-r)/(n+r+0.5)) )
    elif sel==8:#TDVI
        inds=numpy.choose(mask, (0,numpy.sqrt(0.5+(n-r)/(n+r))))
    elif sel==9:
        inds=numpy.choose(mask, (0, (n-g)/(n + g)))
    elif sel==10:
        inds=(r - g)/(r + g)
    # inds=numpy.choose(mask, (0,(r - g)/(r + g)))
    elif sel==11:
        inds=numpy.choose(mask, (0,(n -0.5*(r + g))/(n+ 0.5*(r+g))))
    elif sel==12:
        inds=numpy.choose(mask, (0, numpy.sqrt((n- r)/(n+ r) + 1)))
    elif sel==13:
        inds=numpy.choose(mask, (0,n/g))
    else:
        
        inds=numpy.choose(mask, (0,200*(g*100)/(g*100+r*100+b*100)))

#ave_i=(max_i-ave_i)/50+ave_i
    maxi=numpy.max(inds)
    mini=numpy.min(inds)
    inds=inds*2/(maxi-mini)
    inds=inds-1
    mask2=numpy.equal(r+g+b,0)
    # print numpy.size(mask2)
    
    inds[mask2]=numpy.inf
    driver = ds.GetDriver()
    outDataset = driver.Create('Ind.tif', cols, rows, 1, GDT_Float32)
    outBand = outDataset.GetRasterBand(1)
    outBand.WriteArray(inds,0,0)
     
#     
#    
#    
