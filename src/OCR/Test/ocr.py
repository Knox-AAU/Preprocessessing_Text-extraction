import cv2
import pytesseract

def ocr_core(img):
        text = pytesseract.image_to_string(img)
        return text

"""ocr compute of an image"""
def ocr_comp(image):

    img = cv2.imread(image)

    with open('extracted.txt', 'w') as f:
        f.write(ocr_core(img))
