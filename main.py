import os, piexif
from datetime import datetime

### SETTINGS ###
ext = 'jpg'
dir = r"C:\Users\vasil\YandexDisk\photo\2010-07_Соловки"
newDate = datetime(2010, 7, 1, 0, 0, 0).strftime("%Y:%m:%d %H:%M:%S")
################


now = datetime.now()
changedFiles = 0

for filename in os.listdir(dir):
    if filename[-3:].upper() == ext.upper():
        picPath = dir + '\\' + filename
        exif_dict = piexif.load(picPath)

        changeDate = False
        try:
            dateTimeOriginal = str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
            dateTimeOriginal = dateTimeOriginal[2:21]
            dateTimeOriginal = datetime.strptime(dateTimeOriginal, '%Y:%m:%d %H:%M:%S')
        except:
            print(filename + ': error')
            changeDate = True

        if dateTimeOriginal > now:
            print(filename + ': ' + str(dateTimeOriginal))
            changeDate = True

        if changeDate:
            changedFiles += 1
            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = newDate
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, picPath) ### SAVING PHOTO ###
            print(filename + ': date changed to ' + str(newDate))
        
        # if filename == 'SNV30607(1).JPG':
        #     print('!!!!!!!!') 
        #     print(filename) 
        #     print(str(dateTimeOriginal))


print('Changed files: ' + str(changedFiles))
