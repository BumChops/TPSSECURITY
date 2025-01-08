from captcha.image import ImageCaptcha # type: ignore (the module is installed)

image = ImageCaptcha(width=280, height=90)
data = image.generate("TPSSECURITY")
image.write("TPSSECURITY", "./images/CAPTCHA.png")