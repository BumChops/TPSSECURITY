import hashlib, math, pickle, PIL
import tkinter as tk
from tkinter import font

def createCAPTCHA(text:str) -> None:
    from captcha.image import ImageCaptcha #type: ignore (the module is installed)
    image = ImageCaptcha(width=360, height=120)
    image.write(text, "./images/CAPTCHA.png")

def getData() -> dict:
    # Decrypt binary here
    with open("data.pickle", "rb") as f:
        return pickle.load(f)

def setData(overwrite) -> None:
    with open("data.pickle", "wb") as f:
        pickle.dump(overwrite, f)
    #Encrypt binary here

userCipherKey = ""
def hashCipherKey(data:str) -> str:
    string = data.encode("utf-8")
    hashBin = bin(int(hashlib.sha3_512(string).hexdigest(), 16))
    hashBin += bin(int(hashlib.sha3_512(string[::-1]).hexdigest(), 16))[2:]
    hashBin += bin(int(hashlib.sha3_512(string[:math.floor(len(string)/2)]).hexdigest(), 16))[2:]
    hashBin += bin(int(hashlib.sha3_512(string[math.floor(len(string)/2):]).hexdigest(), 16))[2:]
    while len(hashBin) < 2050:
        hashBin = "0b0" + hashBin[2:]
    return hashBin

def hashPassword(data:str) -> str:
    string = data.encode("utf-8")
    hashBin = hashlib.sha3_384(string).hexdigest()
    return hashBin

def sendMail(receiver:str, subject:str, html:str, text:str) -> None:
    import smtplib, ssl
    from email.message import EmailMessage
    from email.mime.multipart import MIMEMultipart
    from email.mime.text import MIMEText
    sender = "tpsemailbot@gmail.com"
    password = "qidx fkwg tuor cyqu"
    msg = MIMEMultipart("alternative")
    msg["From"] = sender
    msg["To"] = receiver
    msg["Subject"] = subject
    msg.attach(MIMEText(text, "plain"))
    msg.attach(MIMEText(html, "html"))
    context = ssl.create_default_context()
    with smtplib.SMTP_SSL("smtp.gmail.com", 465, context=context) as s:
        s.logIn(sender, password)
        s.sendmail(sender, receiver, msg.as_string())

#Style vars
BORDER = 2
COLOURS = {"fg": "#ff0a5c", "b-bg": "#676767", "bd": "#680a8e", "bg": "#232323", "txt": "#ffffff"}
FONTS = {"button": ("OCR A Extended", 12), "label": ("OCR A Extended", 12), "title": ("OCR A Extended", 48)}
PADDING = 10

#Tkinter setup
root = tk.Tk()
root.state("zoomed")
root.title("TPSSECURITY")
root.iconbitmap("./images/icon.ico")
root.config(bg=COLOURS["bg"])
root.config(cursor="@./cursors/default.cur")
title = tk.StringVar(root, value="TPSSECURITY")

def onload():
    global titleLabel
    titleLabel = tk.Label(root, textvariable=title, font=FONTS["title"], bg=COLOURS["bg"], fg=COLOURS["fg"])
    titleLabel.pack()

    #Assemble (most) frames
    global logInFrame
    logInFrame = makeFrame(root)
    signInButton = makeButton(logInFrame, "Sign In", lambda: notARobot(logInFrame, signInFrame))
    createAccButton = makeButton(logInFrame, "Create Account", lambda: notARobot(logInFrame, createAccFrame))
    signInButton.pack(pady=PADDING)
    createAccButton.pack(pady=PADDING)

    global createAccFrame, crPassLenLabel, crPassMatchLabel, crUserExistsLabel, crSubmitButton, crEmailInput, crPasswordInput, crPassConfirmInput, crUsernameInput
    createAccFrame = makeFrame(root)
    crUserExistsLabel = makeLabel(createAccFrame, tk.StringVar(root, value="That username is already in use. Pick a different one!"), tk.CENTER)
    crUserExistsLabel.config(fg=COLOURS["fg"])
    #crUserExistsLabel.grid(column=0, row=0, columnspan=2)
    crUsernameInput = tk.StringVar(root)
    crUsernameInput.trace_add("write", checkCrData)
    crUsernameLabel = makeLabel(createAccFrame, tk.StringVar(root, value="Username: "), tk.LEFT)
    crUsernameEntry = makeEntry(createAccFrame, crUsernameInput)
    crUsernameLabel.grid(column=0, row=1, pady=PADDING)
    crUsernameEntry.grid(column=1, row=1, pady=PADDING)
    crEmailInput = tk.StringVar(root)
    crEmailInput.trace_add("write", checkCrData)
    crEmailLabel = makeLabel(createAccFrame, tk.StringVar(root, value="Email address: "), tk.LEFT)
    crEmailEntry = makeEntry(createAccFrame, crEmailInput)
    crEmailLabel.grid(column=0, row=2, pady=PADDING)
    crEmailEntry.grid(column=1, row=2, pady=PADDING)
    crPassLenLabel = makeLabel(createAccFrame, tk.StringVar(root, value="Your password should be at least 8 characters long!"), tk.CENTER)
    crPassLenLabel.config(fg=COLOURS["fg"])
    crPassLenLabel.grid(column=0, row=3, columnspan=2)
    crPassMatchLabel = makeLabel(createAccFrame, tk.StringVar(root, value="Those passwords don't match!"), tk.CENTER)
    crPassMatchLabel.config(fg=COLOURS["fg"])
    #crPassMatchLabel.grid(column=0, row=4, columnspan=2)
    crPasswordInput = tk.StringVar(root)
    crPasswordInput.trace_add("write", checkCrData)
    crPasswordLabel = makeLabel(createAccFrame, tk.StringVar(root, value="Password: "), tk.LEFT)
    crPasswordEntry = makeEntryPass(createAccFrame, crPasswordInput)
    crPasswordLabel.grid(column=0, row=5, pady=PADDING)
    crPasswordEntry.grid(column=1, row=5, pady=PADDING)
    crPassConfirmInput = tk.StringVar(root)
    crPassConfirmInput.trace_add("write", checkCrData)
    crPassConfirmLabel = makeLabel(createAccFrame, tk.StringVar(root, value="Confirm Password: "), tk.LEFT)
    crPassConfirmEntry = makeEntryPass(createAccFrame, crPassConfirmInput)
    crPassConfirmLabel.grid(column=0, row=6, pady=PADDING)
    crPassConfirmEntry.grid(column=1, row=6, pady=PADDING)
    crSubmitButton = makeButton(createAccFrame, "Create Account", lambda: createAccProcess(crUsernameInput.get(), crEmailInput.get(), crPasswordInput.get()))
    crSubmitButton.grid(column=0, row=7, columnspan=2, pady=PADDING)

    global signInFrame
    signInFrame = makeFrame(root)
    usernameInput = tk.StringVar(root)
    usernameLabel = makeLabel(signInFrame, tk.StringVar(root, value="Username: "), tk.LEFT)
    usernameEntry = makeEntry(signInFrame, usernameInput)
    usernameLabel.grid(column=0, row=0, pady=PADDING)
    usernameEntry.grid(column=1, row=0, pady=PADDING)
    passwordInput = tk.StringVar(root)
    passwordLabel = makeLabel(signInFrame, tk.StringVar(root, value="Password: "), tk.LEFT)
    passwordEntry = makeEntryPass(signInFrame, passwordInput)
    passwordLabel.grid(column=0, row=1, pady=PADDING)
    passwordEntry.grid(column=1, row=1, pady=PADDING)
    submitButton = makeButton(signInFrame, "Sign In", lambda: signInProcess(usernameInput.get(), passwordInput.get()))
    submitButton.grid(column=0, row=2, columnspan=2, pady=PADDING)

    logInFrame.pack()

def makeButton(parent, text, command):
    border = tk.Frame(parent, bg=COLOURS["bd"])
    button = tk.Button(border, activebackground=COLOURS["fg"], bg=COLOURS["b-bg"], borderwidth=0, command=command, cursor="@./cursors/hover.cur", fg=COLOURS["bg"], font=FONTS["button"], height=1, text=text)
    button.pack(padx=BORDER, pady=BORDER)
    return border

def makeEntry(parent, var):
    return tk.Entry(parent, bg=COLOURS["b-bg"], font=FONTS["button"], fg=COLOURS["fg"], justify="left", relief=tk.FLAT, textvariable=var)

def makeEntryPass(parent, var):
    return tk.Entry(parent, bg=COLOURS["b-bg"], font=FONTS["button"], fg=COLOURS["fg"], justify="left", relief=tk.FLAT, show="*", textvariable=var)

def makeFrame(parent):
    return tk.Frame(parent, bg=COLOURS["bg"])

def makeLabel(parent, textvar, justify):
    return tk.Label(parent, bg=COLOURS["bg"], font=FONTS["label"], fg=COLOURS["txt"], justify=justify, textvariable=textvar)

def processCAPTCHA(guess, value, after):
    if guess != value:
        notARobot(notARobotFrame, after)
    else:
        notARobotFrame.pack_forget()
        after.pack()

def randomUpperString(length:int) -> str:
    import random, string
    return "".join(random.choices(string.ascii_uppercase, k=length))

def notARobot(before, after):
    import PIL.ImageTk
    before.pack_forget()
    value = randomUpperString(8)
    createCAPTCHA(value)
    global notARobotFrame
    notARobotFrame = makeFrame(root)
    image = PIL.Image.open("./images/CAPTCHA.png")
    CAPTCHAPhotoImage = PIL.ImageTk.PhotoImage(image)
    CAPTCHAImage = tk.Label(notARobotFrame, image=CAPTCHAPhotoImage)
    CAPTCHAImage.image = CAPTCHAPhotoImage
    CAPTCHAInput = tk.StringVar(root)
    inputLabel = makeLabel(notARobotFrame, tk.StringVar(root, value="CAPTCHA Value: "), tk.LEFT)
    CAPTCHAEntry = makeEntry(notARobotFrame, CAPTCHAInput)
    CAPTCHAImage.grid(column=0, row=0, columnspan=2, pady=PADDING)
    inputLabel.grid(column=0, row=1, pady=PADDING)
    CAPTCHAEntry.grid(column=1, row=1, pady=PADDING)
    submitButton = makeButton(notARobotFrame, "Submit", lambda: processCAPTCHA(CAPTCHAInput.get(), value, after))
    submitButton.grid(column=0, row=2, columnspan=2, pady=PADDING)

    notARobotFrame.pack()

def checkCrData(var, index, mode):
    issues = 0
    if len(crPasswordInput.get()) < 8:
        crPassLenLabel.grid(column=0, row=3, columnspan=2)
        issues += 1
    else:
        crPassLenLabel.grid_forget()
    
    if crPasswordInput.get() != crPassConfirmInput.get():
        crPassMatchLabel.grid(column=0, row=4, columnspan=2)
        issues += 1
    else:
        crPassMatchLabel.grid_forget()
    
    if not(len(crEmailInput.get()) > 0 and len(crUsernameInput.get()) > 0):
        issues += 1

    if crUsernameInput.get() in getData().keys():
        crUserExistsLabel.grid(column=0, row=0, columnspan=2)
        issues += 1
    else:
        crUserExistsLabel.grid_forget()

    if issues == 0:
        crSubmitButton.winfo_children()[0].config(activebackground=COLOURS["fg"], command=lambda: createAccProcess(crUsernameInput.get(), crEmailInput.get(), crPasswordInput.get()), cursor="@./cursors/hover.cur", fg=COLOURS["bg"])
    else:
        crSubmitButton.winfo_children()[0].config(activebackground=COLOURS["b-bg"], command=doNothing, cursor="@./cursors/no.cur", fg=COLOURS["fg"])
    
def doNothing():
    root.bell()

def encryptForStorage(data:str) -> str:
    return data

def createAccProcess(username:str, email:str, password:str):
    ...
    #confirmationCode = randomUpperString(6)
    #emailHTML = """<>"""
    #emailText = ""
    #sendMail(email, "TPSSECURITY Email Confirmation", emailHTML, emailText)


    #data = getData()
    #userCipherKey = hashCipherKey(password)
    #data[username] = {"password": hashPassword(password), "email": encryptForStorage(email)}

def signInProcess(username, password):
    ...

pinkRGB = list(int(COLOURS["fg"][1:][i:i+2], 16) for i in (0, 2, 4))
purpleRGB = list(int(COLOURS["bd"][1:][i:i+2], 16) for i in (0, 2, 4))

titleColourPhase = -100
def update():
    #Update title colour
    import math
    global pinkRGB, purpleRGB, titleColourPhase
    colour = "#"
    for i in range(len(pinkRGB)):
        result = hex(math.floor((pinkRGB[i]*abs(titleColourPhase) + purpleRGB[i]*(100-abs(titleColourPhase)))/100))[2:]
        if len(result) < 2:
            result = "0" + result
        colour += result

    if titleColourPhase < 100:
        titleColourPhase += 1
    else:
        titleColourPhase = -100

    titleLabel.config(fg=colour)
    root.after(20, update)

onload()
update()
root.mainloop()