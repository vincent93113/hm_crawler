import requests
from bs4 import BeautifulSoup
import pandas
import urllib.request as req
import json 
import pandas as pd
data_list = []
contail_list = []
user_agent = 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/119.0.0.0 Safari/537.36'
api_1 = 'https://www2.hm.com/zh_asia3/men/new-arrivals/view-all/_jcr_content/main/productlisting.display.json'
api_2= 'https://www2.hm.com/zh_asia3/men/new-arrivals/view-all/_jcr_content/main/productlisting.display.json?sort=stock&image-size=small&image=model&offset=36&page-size=36'
api_3='https://www2.hm.com/zh_asia3/men/new-arrivals/view-all/_jcr_content/main/productlisting.display.json?sort=stock&image-size=small&image=model&offset=72&page-size=36'
headers = {'user-agent': user_agent}
api1_data = requests.get(api_1,headers=headers)
api2_data = requests.get(api_2,headers=headers)
api3_data = requests.get(api_3,headers=headers)

api1_data = api1_data.json()
api2_data = api2_data.json()
api3_data = api3_data.json()

def download(url):                     
                          
    jpg = requests.get(url,headers=headers)           
    f = open(route, 'wb')    
    f.write(jpg.content)                 
    f.close()


data_list =[]
contail_url = []
material_list =[]
name = 1
all_api = [api1_data['products'],api2_data['products'],api3_data['products']]
for each_api in all_api:

    for each_data in each_api:

        try:
            each_url = f'https://www2.hm.com'+each_data['swatches'][0]['articleLink']
        except:
            each_url = 'None'

        try:
            title = each_data['title']
        except:
            title = 'None'

        try:
            price = each_data['price']
        except:
            price = 'None'

        try:
            color = each_data['swatches'][0]['colorName']
        except:
            color = 'None'
        
        contail_url.append(each_url)
        
        try:
            photo = 'https:'+each_data['image'][0]['dataAltImage']
            download(photo)
        except:
            photo = 'None'
        
        route = f'image/hm/man/{name}.jpg'
        
        name = name +1
        data_list.append([title,price,color,route])


    for each_contail in contail_url:

        url = each_contail
        
        try:
            res = requests.get(url,headers=headers)
            soup = BeautifulSoup(res.text,'html.parser')
            contail = soup.find('div', {'id': 'section-descriptionAccordion'}).find('p').get_text()
        except:
            contail = 'None'

        print(contail)

        try:
            material = soup.find('div', {'id': 'section-materialsAndSuppliersAccordion'}).find('p').get_text()
        except:
            material = 'None'

        print(material)

        contail_list.append(contail)
        material_list.append(material)


df = pd.DataFrame(data_list, columns=['名稱', '價格', '顏色','路徑'])
df.insert(3, '成分', contail_list[:len(data_list)])
df.insert(4, '描述', material_list[:len(data_list)])
df.to_csv('output.csv', index=False, encoding='utf-8')