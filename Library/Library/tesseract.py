import numpy as np
import cv2
import pytesseract
import random

class Tesseract:

    def handle_ISBNs(self,img):

        for image in img.chunks():
            img = image
            break

        img = cv2.imdecode(np.fromstring(img, np.uint8), cv2.IMREAD_UNCHANGED)
        height = img.shape[0]
        width = img.shape[1]
        y = int(height / 2)

        gray = self.__get_grayscale(img)
        thresh = self.__thresholding(gray)

        processes = [thresh]

        results = []
        for process in processes:
            endY = 100
            text = ""
            while endY + y < height:  
                cropped = self.__getCroppedImage(process, y, endY)
                resized = self.__resizedImage(cropped, (int(cropped.shape[1]*1.2), int(cropped.shape[0] * 1.2)))
                text = self.__getISBNFromOCR(resized)
                if len(text) == 13:
                    results.append(text)
                    break
                y += (endY - 80)
            y = int(height / 2)

        if len(results) != 0:
            text = results[0]
        else:
            text = "Bulunamadı"

        return text

    def __getCroppedImage(self, img, startY, endY):
        return img[startY:startY + endY]  

    def __resizedImage(self, img, ds):
        return cv2.resize(img, ds) 

    def __getISBNFromOCR(self, img):
        custom_config = r'--oem 3 --psm 6 outputbase digits'
        text = pytesseract.image_to_string(img, config=custom_config)
        text = text.replace(".", "")
        text = text.replace("|", "")
        text = text.replace("\"", "")
        text = text.replace("\'", "")
        text = text.replace("'","")
        text = text.replace("%","")
        c = ""
        for i in text:
            if i.isdigit():
                c += i
        splitedText = c.split("\n")
        for i in range(0, len(splitedText)):
            splitedText[i] = splitedText[i].replace(" ", "")
            splitedText[i] = splitedText[i].replace("-", "")
        for split in splitedText:
            if len(split) != 13 and split != "":
                splitedText.remove(split)
        if len(splitedText) != 0:
            text = splitedText[0]
        else:
            text = "nil"
        
        return text
    # get grayscale image
    def __get_grayscale(self,image):
        return cv2.cvtColor(image, cv2.COLOR_BGR2GRAY)

    # noise removal
    def __remove_noise(self,image):
        return cv2.medianBlur(image, 5)

    # thresholding
    def __thresholding(self,image):
        return cv2.threshold(image, 0, 255, cv2.THRESH_BINARY + cv2.THRESH_OTSU)[1]

    # dilation
    def __dilate(self,image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.dilate(image, kernel, iterations=1)

    # erosion
    def __erode(self,image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.erode(image, kernel, iterations=1)

    # opening - erosion followed by dilation
    def __opening(self,image):
        kernel = np.ones((5, 5), np.uint8)
        return cv2.morphologyEx(image, cv2.MORPH_OPEN, kernel)
