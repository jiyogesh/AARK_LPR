import cv2
from . import ARK_LPR, ARK_Utils, ARK_Constants

class ARK_LicensePlateRecoginize(ARK_LPR.ARK_LPRBase):
    def __init__(self):
        pass
    
    def ReadLicensePlateNumber(self, _CV2Image, _Name, _Pass = 0):
        _bPlateTextFound = False
        _PlateNumber = ''
        #_CV2Image, _ = ARK_Utils.SliceImageHoriz(_CV2Image)

        if 0 == _Pass:
            _Image_Contours, _ = self.PreProcess(_CV2Image, 0, cv2.RETR_EXTERNAL, True)

            _txt, _rc = self.ExtractText (_CV2Image, _Image_Contours, 102)
            if len(_txt) > 0:
                for i in _txt:
                    _PlateNumber = _PlateNumber + ' ' + i

            return _PlateNumber

        if 1 == _Pass:
            _Image_Contours, _ = self.PreProcess(_CV2Image, 181, cv2.RETR_TREE, False)
            _txt, _rc = self.ExtractText (_CV2Image, _Image_Contours, 150)
                
            if len(_txt) > 0:
                for i in _txt:
                    _PlateNumber = _PlateNumber + ' ' + i

            return _PlateNumber

        if 2 == _Pass:
            _Threshold_Index = 0
            while True:
                if '' != _PlateNumber:
                    break
                if _Threshold_Index >= len(ARK_Constants.ARK_THRESHOLD_DELTA):
                    break
                
                _Image_Contours, _ = self.PreProcess(_CV2Image, ARK_Constants.ARK_THRESHOLD_DELTA[ _Threshold_Index ], cv2.RETR_TREE, True)

                _Threshold_Index2 = 0
                while True:
                    if '' != _PlateNumber:
                        break
                    if _Threshold_Index2 >= len(ARK_Constants.ARK_THRESHOLD_DELTA2):
                        break

                    _txt, _rc = self.ExtractText (_CV2Image, _Image_Contours, ARK_Constants.ARK_THRESHOLD_DELTA2[_Threshold_Index2])
                    for i in _txt:
                        _PlateNumber = _PlateNumber + ' ' + i
                    _Threshold_Index2 = _Threshold_Index2 + 1
                _Threshold_Index = _Threshold_Index + 1

            return _PlateNumber