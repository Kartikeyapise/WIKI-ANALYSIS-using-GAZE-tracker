import pytesseract
from PIL import Image
image=Image.open("img1.png")
text = pytesseract.image_to_string(image, lang='eng')
print(text)