import numpy
import math
import os, sys, ogr
from osgeo import gdal
from gdalconst import *
import rasterio
from rasterio import crs


def write_raster_inds(n,r,g,b,ds,sel,rgb_File):
    print sel
    gam=1.7


    mask = numpy.greater(n+r+g+b, 0)
    if sel==0:#DVI
        # print 0
        inds = numpy.choose(mask, (0,n-r))
    elif sel==1:##NDVI
        inds=numpy.choose(mask, (0,(n-r)/(n+r)))
#    elif sel==2:#GARI
#        inds=numpy.choose(mask, (0,(n-(g-gam*(b-r)))/(n+(g-gam*(b-r)))))
    elif sel==2:#GNDVI
        inds=numpy.choose(mask, (0,(n-g)/(n+g)))
        
    elif sel==3:#OSAVI
        inds=numpy.choose(mask, (0,1.5*(n-r)/(n+r+0.16)))
    elif sel==4:#RDVI
        inds=numpy.choose(mask, (0,(n - r)/numpy.sqrt(n + r)))
#    elif sel==6: #RVI
#        inds= numpy.choose(mask, (0,n/r))
    elif sel==5:#SAVI
        inds=numpy.choose(mask,(0,1.5*(n-r)/(n+r+0.5)) )
    elif sel==6:#TDVI
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
#    print "bbeeeffoorreeee"
#    print numpy.min(inds)
#    print numpy.max(inds)
#    print numpy.mean(inds)
#    print numpy.var(inds)
#    print "nnnooorrrmmmaaallliizzeeee"
#
    inds=inds-numpy.mean(inds)
    inds=inds/numpy.std((inds))
    
#    inds=inds/numpy.max((inds))
#
#    print numpy.min(inds)
#    print numpy.max(inds)
#    print numpy.mean(inds)
#    jjjjj
####normalize al together afterwards


#    maxi=numpy.max(inds)
#    mini=numpy.min(inds)
#    inds=inds*2/(maxi-mini)
#    inds=inds-1
    mask2=numpy.equal(r+g+b,0)
    inds+=numpy.ones((inds.shape[0],inds.shape[1]))*0.0001
    # print numpy.size(mask2)
# ccrs=crs.from_string("EPSG:32647")
    inds[mask2]=numpy.inf
    src = rasterio.open(rgb_File)

  
    new_dataset =rasterio.open('Ind'+str(sel)+'.tif','w',driver='Gtiff',height=inds.shape[0], width=inds.shape[1],count=1, dtype=str(inds.dtype),crs=src.crs,transform=src.transform)
    
    new_dataset.write(inds, 1)
    new_dataset .close()


    
    
#     
#    
#    
