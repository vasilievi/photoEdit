import os, piexif
from datetime import datetime

### SETTINGS ###
ext = 'jpg'
dir = r"C:\Users\vasil\YandexDisk\photo\Олин компьютер\ВСЕ ФОТО\2012-02_Фотокнига - Оле 25 л"
logFile = r"C:\temp\pyLog.txt"
newDate = datetime(2012, 2, 17, 0, 0, 0).strftime("%Y:%m:%d %H:%M:%S")
################

def printToFile(text):
    print(text)
    now = datetime.now()
    file = open(logFile, "a")
    file.write(str(now) + ": " + text + "\n")
    file.close()

now = datetime.now()
changedFiles = 0

for root, dirs, files in os.walk(dir):
    for file in files:
        picPath = os.path.join(root,file)
        
        if picPath[-3:].upper() != ext.upper():
            printToFile(picPath + ': is not ' + ext)
            continue
        
        exif_dict = piexif.load(picPath)
        changeDate = False

        try:
            dateTimeOriginalString = str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
            dateTimeOriginalString = dateTimeOriginalString[2:21]
            dateTimeOriginal = datetime.strptime(dateTimeOriginalString, '%Y:%m:%d %H:%M:%S')
        except:
            dateTimeOriginal = datetime.strptime(newDate, '%Y:%m:%d %H:%M:%S')
            printToFile(picPath + ': error reading date')
            changeDate = True

        if dateTimeOriginal > now:
            printToFile(picPath + ': ' + str(dateTimeOriginal))
            changeDate = True

        if changeDate:
            changedFiles += 1
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = newDate
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, picPath) ### SAVING PHOTO ###
            printToFile(picPath + ': date changed to ' + str(newDate))

printToFile('Changed files: ' + str(changedFiles))

