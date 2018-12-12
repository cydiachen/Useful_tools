import os
import shutil
import schedule
import time
import requests
# We are now using the Baidu AI faces API to detect faces in our dataset

#client_id： 必须参数，应用的API Key；
#client_secret： 必须参数，应用的Secret Key；
# You need to get your own key from baidu, The access is free of charge.

client_id = ''
client_secret = ''
#Take host token 
host = 'https://aip.baidubce.com/oauth/2.0/token?grant_type=client_credentials&client_id={}&client_secret={}'.format(client_id, client_secret)
#get API token 
token_r = requests.post(host, headers={'Content-Type':'application/json'})

#face API adress
face_base_url = 'https://aip.baidubce.com/rest/2.0/face/v3/detect'
url = face_base_url + '?access_token=' + token_r.json()['access_token']

# Using a picture in order to find our requested Faces
# As is described in the Baidu Face API, we need to use base64 in order to meet the API's request


import os
import shutil
import base64

print("输入格式：E:\myprojectnew\jupyter\整理文件夹\示例")

path = input('请键入需要进行人脸检测的文件夹地址：')
face_path = input('请键入检测到人脸的文件夹地址：')
no_face_path = input('请键入没有检测到人脸的的文件夹地址：')
busy_path = input('请输入当服务忙时候存储没有检测到的人脸的文件夹的地址：')

def job():
    print("We are now using Job arrangement")
    for root, dirs, files in os.walk(path):
        for i in range(len(files)):
            #print(files[i])
            if (files[i][-3:] == 'jpg') or (files[i][-3:] == 'png') or (files[i][-3:] == 'JPG') or (files[i][-3:] == 'bmp' or (files[i][-3:] == 'PNG') or (files[i][-3:] == 'JPG') or (files[i][-3:] == 'bmp') or (files[i][-3:] == 'BMP')):
                file_path = root+'/'+files[i]
                print(file_path)
                with open(str(file_path), 'rb') as f:
                    wait_img = base64.b64encode(f.read())
                face_r = requests.post(url, headers={'Content-Type':'application/json'}, 
                       data={'image':wait_img,
                             'image_type':'BASE64'})
                print(face_r.json())
                result = face_r.json()
                is_face_in = result.get("error_code")
                if is_face_in == 0:
                    print("There is a face in the pic. Saving the pic to Faces dir")
                    new_file_path = face_path+ '/'+ files[i]
                    shutil.copy(file_path,face_path)  
                elif is_face_in != 18:
                    print("No face detected. Saving the pic to No_face dir")
                    new_file_path = no_face_path+ '/'+ files[i]
                    shutil.copy(file_path,no_face_path)
                else:
                    print("Service Busy. Try again")
                    new_file_path = no_face_path+ '/'+ files[i]
                    shutil.copy(file_path,busy_path)
    print("finished!")
    exit()


schedule.every(2).seconds.do(job)

while True:
    schedule.run_pending()
    time.sleep(1)
