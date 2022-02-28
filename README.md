# iact_dnn
Reconstruction of IACT showers with DNNs.

Path at HPC:
/home/woody/caph/mpp228/ML/iact_dnn/

Data preparation:
Transformation of HESS MC .simhess files to ctapipe .h5 files readable by DL1DH:
general/notebooks/simhess2h5.ipynb

Transformation of ctapipe HESS MC .h5 files to (customly defined) .h5 files with square images for CNNs:
general/notebooks/hess_mc_to_square.ipynb


