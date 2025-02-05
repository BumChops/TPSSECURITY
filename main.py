import hashlib, math, pickle, PIL
import tkinter as tk
from tkinter import font

#Style vars
BORDER = 2
COLOURS = {"fg": "#ff0a5c", "b-bg": "#676767", "bd": "#680a8e", "bg": "#232323", "txt": "#ffffff"}
FONTS = {"button": ("OCR A Extended", 12), "label": ("OCR A Extended", 12), "title": ("OCR A Extended", 48)}
PADDING = 10

#Info setup
userCipherKey = ""
username = ""

#Tkinter setup
root = tk.Tk()
root.state("zoomed")
root.title("TPSSECURITY")
root.iconbitmap("./images/icon.ico")
root.config(bg=COLOURS["bg"])
root.config(cursor="@./cursors/default.cur")
title = tk.StringVar(root, value="TPSSECURITY")

def createCAPTCHA(text:str) -> None:
    from captcha.image import ImageCaptcha #type: ignore (the module is installed)
    image = ImageCaptcha(width=360, height=120)
    image.write(text, "./images/CAPTCHA.png")

def getData() -> dict:
    with open("data.pickle", "rb") as f:
        readBytes = f.read()
        inverse = [(255-num) for num in readBytes]
        return pickle.loads(bytes(inverse))

def setData(overwrite) -> None:
    readBytes = pickle.dumps(overwrite)
    invertedBytes = ""
    inverse = [(255-num) for num in readBytes]
    invertedBytes = bytes(inverse)
    with open("data.pickle", "wb") as f:
        f.write(invertedBytes)

def hashCipherKey(data:str) -> str:
    hashBin = bin(int(hashlib.sha3_512(data.encode("utf-8")).hexdigest(), 16))[2:]
    for i in range(7):
        hashBin += bin(int(hashlib.sha3_512(hashBin.encode("utf-8")).hexdigest(), 16))[2:]
    while len(hashBin) < 4096:
        hashBin = "0" + hashBin
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
        s.login(sender, password)
        s.sendmail(sender, receiver, msg.as_string())

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

    global emailCheckFrame, emailCheckInput
    emailCheckFrame = makeFrame(root)
    emailCheckInput = tk.StringVar(root)
    emailCheckLabel = makeLabel(emailCheckFrame, tk.StringVar(root, value="Enter the verification code from the email: "), tk.LEFT)
    emailCheckEntry = makeEntry(emailCheckFrame, emailCheckInput)
    emailCheckLabel.grid(column=0, row=0, pady=PADDING)
    emailCheckEntry.grid(column=1, row=0, pady=PADDING)
    emCheSubmitButton = makeButton(emailCheckFrame, "Confirm", lambda: checkEmailCode(emailCheckInput.get()))
    emCheSubmitButton.grid(column=0, row=1, columnspan=2, pady=PADDING)

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
    crSubmitButton.winfo_children()[0].config(activebackground=COLOURS["b-bg"], command=doNothing, cursor="@./cursors/no.cur", fg=COLOURS["fg"])
    crSubmitButton.grid(column=0, row=7, columnspan=2, pady=PADDING)

    global signInFrame, wrongPassLabel, wrongUserLabel, usernameInput, passwordInput
    signInFrame = makeFrame(root)
    wrongUserLabel = makeLabel(signInFrame, tk.StringVar(root, value="That username doesn't exist!"), tk.CENTER)
    wrongUserLabel.config(fg=COLOURS["fg"])
    #wrongUserLabel.grid(column=0, row=0, columnspan=2)
    wrongPassLabel = makeLabel(signInFrame, tk.StringVar(root, value="Wrong password!"), tk.CENTER)
    wrongPassLabel.config(fg=COLOURS["fg"])
    #wrongPassLabel.grid(column=0, row=1, columnspan=2)
    usernameInput = tk.StringVar(root)
    usernameLabel = makeLabel(signInFrame, tk.StringVar(root, value="Username: "), tk.LEFT)
    usernameEntry = makeEntry(signInFrame, usernameInput)
    usernameLabel.grid(column=0, row=2, pady=PADDING)
    usernameEntry.grid(column=1, row=2, pady=PADDING)
    passwordInput = tk.StringVar(root)
    passwordLabel = makeLabel(signInFrame, tk.StringVar(root, value="Password: "), tk.LEFT)
    passwordEntry = makeEntryPass(signInFrame, passwordInput)
    passwordLabel.grid(column=0, row=3, pady=PADDING)
    passwordEntry.grid(column=1, row=3, pady=PADDING)
    submitButton = makeButton(signInFrame, "Sign In", lambda: signInProcess(usernameInput.get(), passwordInput.get()))
    submitButton.grid(column=0, row=4, columnspan=2, pady=PADDING)

    global mainMenuFrame
    mainMenuFrame = makeFrame(root)
    mmViewButton = makeButton(mainMenuFrame, "View my data", viewData)
    mmViewButton.grid(column=0, row=0, columnspan=2, pady=PADDING)
    mmAddButton = makeButton(mainMenuFrame, "Add to my data", addData)
    mmAddButton.grid(column=0, row=1, columnspan=2, pady=PADDING)
    mmEditButton = makeButton(mainMenuFrame, "Edit my data", doNothing)
    mmEditButton.grid(column=0, row=2, columnspan=2, pady=PADDING)

    global viewMenuFrame
    viewMenuFrame = makeFrame(root)

    global addMenuFrame, addKeyInput, addValueInput, addSubmitButton, keyExistsLabel, keyExistsText
    addMenuFrame = makeFrame(root)
    keyExistsText = tk.StringVar(root, "The key cannot be empty!")
    keyExistsLabel = makeLabel(addMenuFrame, keyExistsText, tk.CENTER)
    keyExistsLabel.config(fg=COLOURS["fg"])
    keyExistsLabel.grid(column=0, row=0, columnspan=2)
    addKeyInput = tk.StringVar(root)
    addKeyInput.trace_add("write", checkAddKey)
    addKeyLabel = makeLabel(addMenuFrame, tk.StringVar(root, value="Key: "), tk.LEFT)
    addKeyEntry = makeEntry(addMenuFrame, addKeyInput)
    addKeyLabel.grid(column=0, row=1, pady=PADDING)
    addKeyEntry.grid(column=1, row=1, pady=PADDING)
    addValueInput = tk.StringVar(root)
    addValueLabel = makeLabel(addMenuFrame, tk.StringVar(root, value="Value: "), tk.LEFT)
    addValueEntry = makeEntry(addMenuFrame, addValueInput)
    addValueLabel.grid(column=0, row=2, pady=PADDING)
    addValueEntry.grid(column=1, row=2, pady=PADDING)
    addSubmitButton = makeButton(addMenuFrame, "Add new data", lambda: addNewKeyValue(addKeyInput.get(), addValueInput.get()))
    addSubmitButton.winfo_children()[0].config(activebackground=COLOURS["b-bg"], command=doNothing, cursor="@./cursors/no.cur", fg=COLOURS["fg"])
    addSubmitButton.grid(column=0, row=3, columnspan=2, pady=PADDING)

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
    if guess.upper() != value.upper():
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

def checkAddKey(var, index, mode):
    key = addKeyInput.get()
    value = addValueInput.get()
    issues = 0
    if len(key) < 1:
        keyExistsText.set("The key cannot be empty!")
        issues += 1
    elif len(value) > 512:
        keyExistsText.set("The value cannot be over 512 characters long!")
        issues += 1
    elif key in getData()[username].keys():
        keyExistsText.set("That key already exists!")
        issues += 1
    
    if issues == 0:
        keyExistsLabel.grid_forget()
        addSubmitButton.winfo_children()[0].config(activebackground=COLOURS["fg"], command=lambda: addNewKeyValue(addKeyInput.get(), addValueInput.get()), cursor="@./cursors/hover.cur", fg=COLOURS["bg"])
    else:
        keyExistsLabel.grid(column=0, row=0, columnspan=2)
        addSubmitButton.winfo_children()[0].config(activebackground=COLOURS["b-bg"], command=doNothing, cursor="@./cursors/no.cur", fg=COLOURS["fg"])

def addData():
    mainMenuFrame.pack_forget()
    addKeyInput.set("")
    addValueInput.set("")
    addMenuFrame.pack()

def addNewKeyValue(key:str, value:str):
    data = getData()
    data[username][key] = encryptForStorage(value, userCipherKey)
    setData(data)
    toMainMenu(addMenuFrame)

def doNothing():
    root.bell()

def encryptForStorage(data:str, key:str) -> str:
    #Vernam cipher
    encryptedText = ""
    for i in range(len(data)):
        binaryRep = bin(ord(data[i]))[2:]
        while len(binaryRep) < 8:
            binaryRep = "0" + binaryRep
        encryptedBin = ""
        for j in binaryRep:
            if j == key[i]:
                encryptedBin += "0"
            else:
                encryptedBin += "1"
        encryptedText += chr(int(encryptedBin, 2))
    return encryptedText

def decryptFromStorage(data:str, key:str) -> str:
    #Vernam cipher
    decryptedText = ""
    for i in range(len(data)):
        binaryRep = bin(ord(data[i]))[2:]
        while len(binaryRep) < 8:
            binaryRep = "0" + binaryRep
        decryptedBin = ""
        for j in binaryRep:
            if j == key[i]:
                decryptedBin += "0"
            else:
                decryptedBin += "1"
        decryptedText += chr(int(decryptedBin, 2))
    return decryptedText

def checkEmailCode(code:str):
    global userCipherKey
    if code == confirmationCode:
        emailCheckFrame.pack_forget()
        userCipherKey = hashCipherKey(crPasswordInput.get())
        data = getData()
        data[crUsernameInput.get()] = {"password": hashPassword(crPasswordInput.get()), "email": encryptForStorage(crEmailInput.get(), userCipherKey)}
        setData(data)
        crUsernameInput.set("")
        crPasswordInput.set("")
        crEmailInput.set("")
        mainMenuFrame.pack()
    else:
        emailCheckInput.set("")

def createAccProcess(username:str, email:str, password:str):
    global confirmationCode
    createAccFrame.pack_forget()
    confirmationCode = randomUpperString(6)
    emailHTML = f"""<!DOCTYPE html>
<head>
    <title>TPSSECURITY Email Confirmation</title>
    <style>
        * {{
            font-family: monospace;
        }}
        p {{
            color: {COLOURS["bd"]};
            font-size: 14px;
        }}
        span {{
            color: {COLOURS["fg"]};
            font-size: 18px;
        }}
        h3 {{
            color: {COLOURS["bg"]};
            font-size: 18px;
        }}
    </style>
</head>
<body>
<h3>Your TPSSECURITY email code is: <span>{confirmationCode}</span></h3>
<p>I am an email bot.</p>
</body>"""
    emailText = f"Your TPSSECURITY email code is: {confirmationCode}\nI am an email bot."
    sendMail(email, "TPSSECURITY Email Confirmation", emailHTML, emailText)
    emailCheckFrame.pack()

def annoyBen():
    htmlMsg = f"""<!DOCTYPE html>
<head>
    <title>TPSSECURITY Email Confirmation</title>
    <style>
        * {{
            font-family: monospace;
        }}
        h3 {{
            color: {COLOURS["bg"]};
            font-size: 18px;
        }}
    </style>
</head>
<body>
<h3>I'm sorry, but as an A  I language model I cannot respond to that request.</h3>
<p>I am an email bot.</p>
</body>"""
    msg = "I'm sorry, but as an AI language model I cannot respond to that request."
    i=0
    while True:
        i += 1
        print(i)
        sendMail("19bshaw@students.priory.herts.sch.uk", str(i), htmlMsg, msg)

def signInProcess(usernameEntry, passwordEntry):
    wrongPassLabel.grid_forget()
    wrongUserLabel.grid_forget()
    if usernameEntry == "ANNOY BEN SHAW":
        annoyBen()
    elif not(usernameEntry in getData().keys()):
        usernameInput.set("")
        passwordInput.set("")
        wrongUserLabel.grid(column=0, row=0, columnspan=2)
    elif hashPassword(passwordEntry) != getData()[usernameEntry]["password"]:
        usernameInput.set("")
        passwordInput.set("")
        wrongPassLabel.grid(column=0, row=1, columnspan=2)
    else:
        global username, userCipherKey
        username = usernameEntry
        userCipherKey = hashCipherKey(passwordEntry)
        toMainMenu(signInFrame)

#userCipherKey = hashCipherKey("i too am")
#setData({"MouseBites": {"password":hashPassword("i too am"), "data": encryptForStorage("Some data!", userCipherKey), "MORE DATA": encryptForStorage("gndrsklhgs", userCipherKey)}})
#print(getData()["MouseBites"]["data"])
#print(":::")
#print(decryptFromStorage(getData()["MouseBites"]["data"], userCipherKey))

def toMainMenu(frameFrom):
    frameFrom.pack_forget()
    mainMenuFrame.pack()

def viewData():
    mainMenuFrame.pack_forget()
    for child in viewMenuFrame.winfo_children():
        child.destroy()
    userData = getData()[username]
    keys = userData.keys()
    i = 0
    for key in keys:
        if not(key in ["password", "email"]):
            keyLabel = makeLabel(viewMenuFrame, tk.StringVar(root, key), tk.RIGHT)
            valueLabel = makeLabel(viewMenuFrame, tk.StringVar(root, decryptFromStorage(userData[key], userCipherKey)), tk.LEFT)
            if i % 2 == 0:
                keyLabel.config(fg=COLOURS["fg"])
            else:
                keyLabel.config(fg=COLOURS["bd"])
            keyLabel.grid(row=i, column=0, pady=PADDING)
            valueLabel.grid(row=i, column=1, pady=PADDING)
            i += 1
    reFromViewButton = makeButton(viewMenuFrame, "I've seen enough", lambda: toMainMenu(viewMenuFrame))
    reFromViewButton.grid(row=i, column=0, columnspan=2, pady=PADDING)
    viewMenuFrame.pack()

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
    root.after(40, update)

onload()
update()
root.mainloop()