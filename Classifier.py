from get_training_data_anth import *
from sklearn import svm
from get_Test_ind_Mats import *
import scipy.io as sio

ind_path="inds/"
(X_train,Y_train)=get_training_data()
clf = svm.SVC()
clf.fit(X_train,Y_train)
#print clf
X_test=get_test_mats('RGB_im.tif','NIR_im.tif',0,ind_path)
sio.savemat('test_data.mat',{'X_test':X_test})
print "test_data_avail"
y_res=clf.predict(X_test)
sio.savemat('test_res.mat',{'y_res':y_res})
print y_res.shape
