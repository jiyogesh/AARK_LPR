import cv2
import re

def SliceImageHoriz(_CV2Image):
    _Height, _Width = _CV2Image.shape[:2]
    _Start_Row, _Start_Col = int (0.5 * _Height), 0
    _End_Row, _End_Col = _Height, _Width

    _Lower_Half_Image = _CV2Image [ _Start_Row: _End_Row, _Start_Col: _End_Col ]
    _Upper_Half_Image = _CV2Image [ 0: _Start_Row, 0: _End_Col ]

    return _Lower_Half_Image, _Upper_Half_Image

def ShowImage(_WndCaption, _CV2Image):
    #_CV2Image = cv2.resize(_CV2Image, (320, 240))
    cv2.imshow(_WndCaption, _CV2Image)
    cv2.waitKey(0)

def CleanText(_InputText):
    return re.sub('[^A-Za-z0-9]+', '', _InputText.strip())