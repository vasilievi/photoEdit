import os, piexif
from datetime import datetime

# dir = 'C:\\Users\\vasil\\YandexDisk\\photo\\20220509_Google Фото\\Photos from 2018\\'
dir = '.\\photos\\'
now = datetime.now()
beginning2018 = datetime(2018, 1, 1, 0, 0, 0).strftime("%Y:%m:%d %H:%M:%S")
incorrectDates = 0

for filename in os.listdir(dir):
    if filename[-3:].upper() == 'JPG':
        picPath = dir + filename
        exif_dict = piexif.load(picPath)

        try:
            dateTimeOriginal = str(exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal])
            dateTimeOriginal = dateTimeOriginal[2:21]
            dateTimeOriginal = datetime.strptime(dateTimeOriginal, '%Y:%m:%d %H:%M:%S')
        except:
            continue

        if dateTimeOriginal > now:
            incorrectDates += 1
            print(filename + ' ' + str(dateTimeOriginal))

            exif_dict['Exif'][piexif.ExifIFD.DateTimeOriginal] = beginning2018
            exif_bytes = piexif.dump(exif_dict)
            piexif.insert(exif_bytes, picPath)

print('Incorrect dates: ' + str(incorrectDates))
