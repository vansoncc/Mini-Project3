# Import part
import json
import tweepy
import pymysql
import pymongo
import datetime
import os
import wget 
import subprocess
import ffmpeg
import io
import PIL
from os import listdir
from google.cloud import vision
from  PIL import ImageDraw, Image, ImageFont

#Provide the Twitter key and token
consumer_key = ''
consumer_secret = ''
access_token = ''
access_token_secret = ''

#The Image save path
image_path=os.chdir('/Users/vanson/downloads/boston university/EC601/API')

#Set the Json File
os.environ['GOOGLE_APPLICATION_CREDENTIALS']= "My_First.json"

#Set the label text size and font
FONT_PATH = os.environ.get("FONT_PATH", "/Library/Fonts/Times New Roman.ttf")

#Tweepy Authority process
auth = tweepy.OAuthHandler(consumer_key, consumer_secret)
auth.set_access_token(access_token, access_token_secret)
api = tweepy.API(auth)
# for tweet in public_tweets:
#     print(tweet.text)



#Using the Tweepy to download image
def download_tweets(source):
    Twitter_Page = api.user_timeline(screen_name =source, count=50)
    Twitter_with_image=set()
    print('Downloading the Image from '+ source)
    print('Processing.....')
    for status in Twitter_Page:
        media = status.entities.get('media', [])
        if (len(media) > 0):
            Twitter_with_image.add(media[0]['media_url'])
    i=0
    for url in Twitter_with_image:
        image=wget.download(url)
        os.rename(image, 'image'+str(i) + '.jpg')
        i += 1
    Img_url=''
    Img_url = Img_url+url
    return  Img_url

#Use ffmpeg to convert the images to video
def conv_image():
     print('Converting the images to video....Processing')
     subprocess.call(['ffmpeg', '-framerate', '1', '-i', 'image%d.jpg', '-vcodec', 'mpeg4','Tweets.mp4'])


client = vision.ImageAnnotatorClient()

#Use the google vision to label to images and then add the label text to the images
def get_describe(h):
    print('Label the Images...Processing')
    for i in range(h):
        file_name = os.path.join(os.path.dirname(__file__), 'image%s.jpg'%(i))

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

            image = vision.types.Image(content=content)


# Performs label detection on the image file
            response = client.label_detection(image=image)
            labels = response.label_annotations


        j = 0
        # str = ''
        description = ''
        for label in labels:
            # str = str + label.description + '\n'  # tag
            description = description + label.description + ','
            # print(label.description)
            raw_image = Image.open(file_name)
            draw = ImageDraw.Draw(raw_image)  # 修改图片
            font = ImageFont.truetype('/Library/Fonts/Times New Roman.ttf', 36)
            draw.text((50, 40 + j), label.description, fill=(0,0,0), font=font)
            j += 30
            raw_image.save(file_name)

        return description


def count_file_number():
    filename_list = listdir(image_path)
    h = 0
    for filename in filename_list:
        if filename.endswith('jpg'):
            h += 1
    print('Total image file :', + h-2)
    return h-2

##---------------------------------------For Mini Project3------------------------------------------##

##---------------Create Database---------------##
def Create_base():
    db = pymysql.connect(host='localhost',user='root', password='sbzaijian', port=3306)
    cursor = db.cursor()
    cursor.execute('SELECT VERSION()')
    data = cursor.fetchone()
    print('Database version:', data)
    cursor.execute('CREATE DATABASE Mini_Project3')
    db.close()


##---------------Create Table---------------##
def Create_table():
    db = pymysql.connect(host='localhost', user='root', password='sbzaijian', port=3306, db='Mini_Project3')
    cursor = db.cursor()
    cursor.execute('use Mini_Project3')
    # cursor.execute("DROP TABLE IF EXISTS Tweepy_Data")
    sql = 'CREATE TABLE IF NOT EXISTS Tweepy_Data (ID MEDIUMINT NOT NULL AUTO_INCREMENT, Twitter_ID VARCHAR(255) NOT NULL,Img_url VARCHAR(255) NOT NULL, Img_number INT NOT NULL, label VARCHAR(255) NOT NULL, Op_time CHAR(50) NOT NULL, PRIMARY KEY (ID))'
    cursor.execute(sql)
    # print('Table Create Successful')

    db.close()


def Write_MySQL(Twitter_ID,Img_number,label,url):

    db = pymysql.connect(host='localhost', user='root', password='sbzaijian', port=3306, db='Mini_Project3')
    cursor = db.cursor()
    time = datetime.datetime.now()
    Tweepy_Data = {'Twitter_ID': 'Twitter_ID'}

    # value= (Twitter_ID,Img_number,label)
    try:

        sql = 'INSERT INTO Tweepy_Data (Twitter_ID,Img_url, Img_number,label,Op_time) VALUES (%s, %s, %s, %s, %s)'
        # Tweepy_Data = {'Twitter_ID': 'Twitter_ID'}

        cursor.execute(sql, (Twitter_ID, url, Img_number, label,time))
        db.commit()
    except:
        db.rollback()
        print("Can't connect to MySQL service")

    # cursor.execute("""SELECT * FROM Tweepy_Data""")
    db.close()

def main(source,h,method):
    if (method == 1):
        db = pymysql.connect(host='localhost', user='root', password='sbzaijian', port=3306, db='Mini_Project3')
        cursor = db.cursor()
        # cursor.execute('CREATE DATABASE Mini_Project3')
        cursor.execute('use Mini_Project3')
        sql = 'INSERT INTO Tweepy_Data (Twitter_ID,Img_url, Img_number,label,Op_time) VALUES (%s, %s, %s, %s, %s)'

    elif (method == 2):
        myclient = pymongo.MongoClient("mongodb://localhost:27017/")
        mydb = myclient["Mini_Project3_Mongo"]
        mycol = mydb["users"]

    # i = 0
    client = vision.ImageAnnotatorClient()

    for i in range(h):
        # Twitter_Page = api.user_timeline(screen_name=source, count=50)
        # Twitter_with_image = set()
        # print('Downloading the Image from ' + source)
        # print('Processing.....')
        # for status in Twitter_Page:
        #     media = status.entities.get('media', [])
        #     if (len(media) > 0):
        #         Twitter_with_image.add(media[0]['media_url'])
        # for url in Twitter_with_image:
        #     image = wget.download(url)
        #     os.rename(image, 'image' + str(i) + '.jpg')
        # Img_url = ''
        # Img_url = Img_url + url

        # print('Label the Images...Processing')
        file_name = os.path.join(os.path.dirname(__file__), 'image%s.jpg' % (i))

        with io.open(file_name, 'rb') as image_file:
            content = image_file.read()

        image = vision.types.Image(content=content)


        # Performs label detection on the image file
        response = client.label_detection(image=image)
        labels = response.label_annotations

        j = 0
        k = 0
        # str = ''
        description = ''
        for label in labels:
            # str = str + label.description + '\n'  # tag
            description = description + label.description + ','
            k= k+1
            # print(label.description)
            raw_image = Image.open(file_name)
            draw = ImageDraw.Draw(raw_image)  # 修改图片
            font = ImageFont.truetype('/Library/Fonts/Times New Roman.ttf', 36)
            draw.text((50, 40 + j), label.description, fill=(0, 0, 0), font=font)
            j += 1
            raw_image.save(file_name)

        i = i+1

        if(method == 1):
            time = datetime.datetime.now()
            value =(source, file_name, h, description, time)
            cursor.execute(sql,value)
            db.commit()
        elif(method ==2):
            time = datetime.datetime.now()
            mydict={"username": source, "Img_url": file_name, "Img_number": h, "Label:": description, "Time":time}
            mycol.insert(mydict)


if __name__ == '__main__':


    #Step1. Download the images from twitter
    #Step2. Label the images
    #Step3. Add the text to the images
    #steo4. Convert the image to video


    str1 = input("Request Download Image from Twitter Acount:")
    username = ''
    username = username + str1

    url= download_tweets(str1)
    # Img_url=''
    # Img_url = Img_url+url
    h=count_file_number()
    get_describe(h)
    conv_image()
    # # Create_base()
    Create_table()
    Write_MySQL(username, h,get_describe(h),url)

