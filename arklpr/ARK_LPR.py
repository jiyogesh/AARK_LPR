from . import ARK_Utils, ARK_Constants
import numpy as np
import cv2
from PIL import Image
import pytesseract as tess

class ARK_LPRBase:
    def __init__(self):
        pass

    def PreProcess(self, _CV2Image, _Threshold_Delta, _ContourMode, _bRefine):
        _Threshold_Image = None
        if _bRefine:
            _Blur = cv2.GaussianBlur( _CV2Image, (5, 5), 0 )
            _Gray_Image = cv2.cvtColor( _Blur, cv2.COLOR_BGR2GRAY )
            _Sobel = cv2.Sobel( _Gray_Image, cv2.CV_8U, 1, 0, ksize = 3 )
            _, _Threshold_Image = cv2.threshold( _Sobel, _Threshold_Delta, 255, cv2.THRESH_BINARY)
        else:
            _Gray_Image = cv2.cvtColor( _CV2Image, cv2.COLOR_BGR2GRAY )
            _, _Threshold_Image = cv2.threshold( _Gray_Image, _Threshold_Delta, 255, cv2.THRESH_BINARY)

        _Element = cv2.getStructuringElement(shape = cv2.MORPH_RECT, ksize = (17, 3))
        _Image_Tmp = _Threshold_Image.copy()
        cv2.morphologyEx(src = _Threshold_Image, op = cv2.MORPH_CLOSE, kernel = _Element, dst =  _Image_Tmp)
        _, _Image_Contours, _ = cv2.findContours( _Image_Tmp, _ContourMode, cv2.CHAIN_APPROX_SIMPLE)

        return _Image_Contours, _Threshold_Image
    
    def CheckRatio(self, _Area, _Width, _Height):
        if (_Area < ARK_Constants.ARK_PLATE_MIN_AREA or _Area > ARK_Constants.ARK_PLATE_MAX_AREA):
                return False

        _Ratio = float(_Width)/float(_Height)
        if _Ratio < 1:
            _Ratio = 1 / _Ratio

        if (_Ratio < ARK_Constants.ARK_RATIO_MIN or _Ratio > ARK_Constants.ARK_RATIO_MAX):
            return False
        return True
    
    def ValidateRotationAndRatio(self, _Rect):
        (_x, _y), (_Width, _Height), rAngle = _Rect
        if (0 == _Width) or (0 == _Height):
            return False
        
        _Angle = -rAngle        
        if (_Width <= _Height):
            _Angle = 90 + rAngle
        
        if _Angle > 15:
            return False
        
        if not self.CheckRatio(_Width * _Height, _Width, _Height):
            return False
        return True
    
    def IsWhitePlate(self, _Plate):
        if np.mean(_Plate) < ARK_Constants.ARK_PLATE_WHITE_MEAN:
            return False
        return True
    
    def CleanPlate(self, _Plate, _Threshold_Delta, _ContourMode, _bRefine = False):
        _Image_Contours, _Threshold_Image = self.PreProcess(_Plate, _Threshold_Delta, _ContourMode, _bRefine)
       # ARK_Utils.ShowImage('CP', _Threshold_Image)
        if not _Image_Contours:
            return _Plate, None

        _Area = [ cv2.contourArea( _Contour ) for _Contour in _Image_Contours ]
        _Max_Index = np.argmax( _Area )
        _Max_Contour = _Image_Contours [ _Max_Index ]
        _Max_Contour_Area = _Area [ _Max_Index ]
        _Left, _Top, _Width, _Height = cv2.boundingRect( _Max_Contour )

        if not self.CheckRatio( _Max_Contour_Area, _Width, _Height ):
            return _Plate, None
        _Cleaned_Image = _Threshold_Image [ _Top : _Top + _Height, _Left : _Left + _Width ]

        return _Cleaned_Image, [ _Left, _Top, _Width, _Height ]

    def ExtractText(self, _CV2Image, _Image_Contours, _Threshold_Delta2):
        if not _Image_Contours:
            return '', None
        
        _PlateNumber = []
        _Rect = []
        for _, _nContour in enumerate ( _Image_Contours ):
            if not self.ValidateRotationAndRatio( cv2.minAreaRect( _nContour ) ):
                continue

            _Left, _Top, _Width, _Height = cv2.boundingRect( _nContour )

            _Plate_Image = _CV2Image [ _Top : _Top + _Height, _Left : _Left + _Width ]

            if not self.IsWhitePlate( _Plate_Image ):
                continue

            _Clean_Plate, _Clean_Rect = self.CleanPlate( _Plate_Image, _Threshold_Delta2, cv2.RETR_EXTERNAL)
            if not _Clean_Rect:
                continue
            _Clean_Plate_Image = Image.fromarray(_Clean_Plate)
            
            _txt = ARK_Utils.CleanText(tess.image_to_string( _Clean_Plate_Image, lang= 'eng' ))

            if not _txt.isalpha() and '' != _txt:
                _PlateNumber.append(_txt)
                _Rect.append(_Clean_Rect)
        return _PlateNumber, _Rect