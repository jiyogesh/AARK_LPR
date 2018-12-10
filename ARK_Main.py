import cv2
from os import listdir
from os.path import isfile, join

from arklpr.ARK_PlateRecoginizer import ARK_LicensePlateRecoginize

if __name__ == "__main__":
    _alpr = ARK_LicensePlateRecoginize()
    _DataDir = 'DATA/'
    print('Recoginizing Number Plate')
    _files = [f for f in listdir(_DataDir) if isfile(join(_DataDir, f))]
    for f in _files:
        print ('Process File: ' + f)
        _Pass = 0
        while True:
            if _Pass > 2:
                break
            _txt = _alpr.ReadLicensePlateNumber(cv2.imread(join(_DataDir, f)), f, _Pass)
            if _txt:
                print ('\tRegistration : ' + _txt)
                break
            _Pass = _Pass + 1
    pass