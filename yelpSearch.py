#   Eli Gatchalian
#   May 2, 2019

import tkinter as tk
from requests import get
from urllib import request
from geocoder import ip
from webbrowser import open_new_tab
from PIL import ImageTk, Image
from io import BytesIO
from random import shuffle

#api set-up
YELP_API_KEY = '' #You can get a unique api key from yelp.com/developers
ENDPOINT = 'https://api.yelp.com/v3/businesses/search'
HEADERS = {'Authorization':'bearer %s' % YELP_API_KEY}

#creating window
window = tk.Tk()

#lists to track a restaurant's image url and yelp url
images_url = []
yelp_url = []

#locating user's city
city = ip('me').city
if(city == ''):
    city = 'Seattle'

def getBusinessInformation():
    parameters = {'location': city, 
                  'limit': 50, #get 50 places, output max 8
                  'radius': 1000,
                  'categories': 'Restaurants',
                  'open_now': True,
                  'price': (1,2,3),
                  'sort_by': 'rating'}
    response = get(url = ENDPOINT, params = parameters, headers = HEADERS)
    business_dict = response.json()
    return business_dict
        
def onClick(pic):
    open_new_tab(yelp_url[pic])

def createImage(url,i,j):
    raw_data = request.urlopen(url).read()
    img = Image.open(BytesIO(raw_data))
    img = img.resize((250,250), Image.ANTIALIAS)
    image = ImageTk.PhotoImage(img)
    label1 = tk.Label(window,image=image)
    label1.grid(row=i,column=j)
    images_url.append(image)

def createButton(name, url, i, j, pic_num):
    button = tk.Button(window, text = name, command = lambda idx = pic_num: onClick(idx))
    button.grid(row=i,column=j,sticky='s')
    yelp_url.append(url)

def addInfoToWindow(business_data):
    row = 0
    column = 0
    pic_num = 0
    shuffle(business_data['businesses'])
    
    for biz in business_data['businesses']:
        #Should include 8 businesses only if they have valid image and yelp url
        if (pic_num > 7):
            break
        if(biz['image_url'] == '' or biz['url'] == ''):
            continue 
        
        createImage(biz['image_url'],row,column)
        createButton(biz['name'],biz['url'],row,column,pic_num)
        pic_num += 1
        
        if(column < 3):
            column += 1
        else:
            column = 0
            row += 1

def main():
    addInfoToWindow(getBusinessInformation())
    window.title(str(len(images_url)) + " food places in " + city)
    window.mainloop()

if __name__ == '__main__':
    main()
