### Rent file
import os
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
# from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
# from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
# import requests
import time
from selenium.webdriver.support.ui import Select
import urllib.request
# import pytesseract
from PIL import Image, ImageFilter ,ImageDraw
from pytesseract import pytesseract
# import PIL
import urllib.request
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
import re

image_count=1
image_counts=1
count=[1]
urls_list=[]
url_list=[]   #create lists to store data
photos_list=[]
photo_list=[]
name_list=[]
price_list=[]
property_detail= []
feature_list=[]
desc_list=[]
rent_urls_list=[]
rent_url_list=[]



try:
    driver.close()
except:
    pass
df=pd.read_csv('/home/yuchen/workspace/Accounts.csv')

urls=df['Agent url'].dropna().tolist()
emails=df['Email login'].dropna().tolist()
passwords=df['Password'].dropna().tolist()
rent_url_list.clear()
rent_urls_list.clear()

def rent_fun():
    res = driver.page_source
    soup = BeautifulSoup(res, 'html.parser')
    col=soup.find('div',{'class':'listing-widget-new small-listing-card','id':'listings-container'})
    images=col.find_all('a',{'class':'nav-link'})

    # rent_url_list.clear()
    # rent_urls_list.clear()
    for img in images:
        h=img.get('href')

        if  "https://www.commercialguru.com.sg/" not in h:
                rent_urls_list.append("https://www.commercialguru.com.sg/"+h)
        else:
            rent_urls_list.append(h)
        for x in rent_urls_list:
            if x not in rent_url_list:
                if "#contact-agent" not in x:
                    rent_url_list.append(x)
def after_pagination():
    try:    
            for i in range(0,len(urls)):    
                element =WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div[6]/div[6]/div/div/div[1]/div/button[2]'))).click()
                driver.delete_all_cookies()
                time.sleep(8)  
                rent_fun()
    except:
        pass

for i in range(0,len(urls)):
        agent_url=(urls[i])
        email=emails[i]
        password=passwords[i]
        driver = webdriver.Chrome('/home/yuchen/workspace/code/chromedriver')

        driver.get(agent_url)
        driver.maximize_window()
        driver.delete_all_cookies()    
        # time.sleep(10)          
        element =WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div[6]/div[6]/div/div/div[1]/div/button[2]'))).click()
        driver.delete_all_cookies()  
        rent_fun()
        after_pagination()
             
        print(rent_url_list)    
        print(len(rent_url_list))      
#     #############################################################################################
        driver.delete_all_cookies()
       

        for i in range (0,len(rent_url_list)):
            time.sleep(5)
            rent=(rent_url_list[i])
            driver.delete_all_cookies()
            driver.get(rent)
            driver.delete_all_cookies()
            res = driver.page_source
            soup = BeautifulSoup(res, 'html.parser')
       
            address=soup.find('div',{'class':'listing-address'})

            name=soup.find('div',{"class":"listing-title text-transform-none"})
            name_list.append(name)

            price=soup.find('span',{'class':"element-label price"})
            price_list.append(price)
            try:
                postalCode=address.find('span',{'itemprop':'postalCode'}).text
                no_of_bedroom=soup.find('div',{'class':'property-info-element beds'})
                no_of_bedrooms=no_of_bedroom.find('span',{'class':'element-label'})
            except:
                pass
            try:
                no_of_bathroom=soup.find('div',{'class':'property-info-element baths'})
                no_of_bathrooms=no_of_bathroom.find('span',{'class':'element-label'})
            except:
                pass
            details=soup.find_all('div', {'class':'value-block'})
            desc=soup.find('div',{'class':'listing-details-text'})
           
            fetures = soup.find('div', {'id': 'facilities'})
            try:
                x = re.split("\n", fetures.text)
                for i in x:
                    if i != '':
                        feature_list.append(i)
                    else:
                        pass
            except:
                pass    

            imge=soup.find_all('li',{'data-target':'#carousel-photos'})

            time.sleep(5)
            for imge in imge:

                photo=imge.find_all('img')

                for i in photo:

                    src = i.get('data-original')

                    if "https" in src:

                        x = src.replace("C80X60", "V800")
                        req = urllib.request.Request(x, headers={'User-Agent': '*'})
                        response = urllib.request.urlopen(req)
                        html = urllib.request.urlopen(req).read()
                        with open('/home/yuchen/workspace/code/img'+str(image_count)+'.jpeg', 'wb') as f:
                            f.write(html)
                            image_count = image_count+1
                            count.append(image_count)

            for counts in count:
                try:
                        imge = Image.open('/home/yuchen/workspace/code/img'+str(counts)+'.jpeg')

                        a=imge.size

                        hight=imge.size
                        a=imge.size
                        newsize = (800, 600)
                        im1 = imge.resize(newsize)
                        mask = Image.new('L', im1.size, 0)
                        draw = ImageDraw.Draw(mask)
                        draw.rectangle([ (605,425), (900,360)], fill=260)
                        draw.rectangle([ (425,445), (900,400)], fill=260)
                        img3=im1.filter(ImageFilter.GaussianBlur(48))
                        im1.paste(img3,mask=mask)              
                        im1.save('/home/yuchen/workspace/code/img'+str(counts)+'.jpeg')
                            # imge.save('/home/sunil/workspace/scraping/kelvin/images/img'+str(counts)+'.jpeg')
                except:
                    pass
           

            driver.delete_all_cookies()

            try:
                driver.get("https://myestate.sg/agent/login")
            except:
                driver.delete_all_cookies()              

                driver.get("https://myestate.sg/agent/listings/create")
            try:
                WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[3]/div/div/div[2]/form/div[1]/input'))).send_keys(email)
                WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[3]/div/div/div[2]/form/div[2]/input'))).send_keys(password)
                WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[3]/div/div/div[2]/form/button'))).click()
                driver.maximize_window()
            except:
                    driver.get("https://myestate.sg/agent/listings/create")


            try:
                el=WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[1]/div/div/div/div[1]/div/button[2]')))
                driver.execute_script("arguments[0].click();", el)
                li=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[1]/div/div/div/div[1]/div/div/div/ul/div/li[2]')))
                driver.execute_script("arguments[0].click();", li)
            except:

                driver.get("https://myestate.sg/agent/listings/create")



            driver.get("https://myestate.sg/agent/listings/create")


            time.sleep(10)
            nexts = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Next')]")))
            driver.execute_script("arguments[0].click();", nexts)


            for counts in count:
                try:
                    image_path=os.path.abspath('/home/yuchen/workspace/code/img'+str(counts)+'.jpeg')
                    lis= driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[4]/div[3]/div/input')
                    lis.send_keys(image_path)
                    os.remove('/home/yuchen/workspace/code/img'+str(counts)+'.jpeg')
                except:
                    pass

            count.clear()
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/div[4]/div[5]/button[2]').click()
           
            for i in range(0,5):
                try:    
                    nexts = WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Next')]")))
                except:
                    pass    
            try:
               
                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[1]/div[1]/div/input').send_keys(int(postalCode))
            except:
                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[1]/div[1]/div/input').send_keys('tam')
               
            time.sleep(10)
           
            try:
                    ela=WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[1]/div[1]/div/ul/li')))
                    driver.execute_script("arguments[0].click();", ela)
            except:  
                pass
            building_input = driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[1]/div[1]/div/input')
            building_output=(building_input.get_attribute('value'))
           
            if len(building_output)>6:
                pass

            else:

                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[1]/div[1]/div/input').send_keys(Keys.ENTER)
                for i in range(0,7):

                    driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[1]/div[1]/div/input').send_keys(Keys.BACKSPACE)

                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[1]/div[1]/div/input').send_keys('tam')
                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[1]/div[1]/div/input').send_keys(Keys.ENTER)
                time.sleep(10)
                ela=WebDriverWait(driver,2).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[1]/div[1]/div/ul/li')))
                driver.execute_script("arguments[0].click();", ela)
            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[2]/div[1]/div/input').clear()
            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[2]/div[1]/div/input').send_keys(name.text)

            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[2]/div/input').send_keys(price.text)
            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[3]/div[2]/div/select/option[2]').click()

            Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[1]/div/select')).select_by_visible_text('For Rental')
            try:
                Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[3]/div/select')).select_by_value(no_of_bedrooms.text)
            except:
                Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[3]/div/select')).select_by_value('-2')
            try:
                Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[4]/div/select')).select_by_value(no_of_bathrooms.text)
            except:
                Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[4]/div/select')).select_by_value('0')

            # s=(details[0].text).replace('For Rent','')

            s=(details[0].text).replace('For Rent','')  
           
            try:
               
                if "Fa" in s:
                    driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys("Fa")
                    driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(Keys.ENTER)
                    df=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[2]/div[1]/div[1]/div/div[1]/div[1]').click()
                elif "Bu" in s:
                    driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys("BUS")
                    driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(Keys.ENTER)
                    df=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[2]/div[1]/div[1]/div/div[1]/div[1]').click()    
                else:
                    driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(s)
                    driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(Keys.ENTER)
                    df=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[2]/div[1]/div[1]/div/div[1]/div[1]').click()
            except:
                pass        
           
            type_value=driver.find_element_by_xpath('//*[@id="react-select-2-input"]').get_attribute('value')
            print(type_value)
            if len(type_value)<0:    
           
                driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys("Bus")
                driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(Keys.ENTER)
                df=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[2]/div[1]/div[1]/div/div[1]/div[1]').click()          

            s=(details[1].text)
            try:
                if s != "Unknown Tenure":
                    nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), '{}')]".format(s))))

                    nexts.click()
                # else  "Un" in s:
                #     driver.find_element_by_xpath('//*[@id="react-select-5-input"]').send_keys('Flexible')
                #     driver.find_element_by_xpath('//*[@id="react-select-5-input"]').send_keys(Keys.ENTER)
                else:
                    driver.find_element_by_xpath('//*[@id="react-select-5-input"]').send_keys('Flexible')
                    driver.find_element_by_xpath('//*[@id="react-select-5-input"]').send_keys(Keys.ENTER)  
            except:

                driver.find_element_by_xpath('//*[@id="react-select-5-input"]').send_keys('Flexible')
                driver.find_element_by_xpath('//*[@id="react-select-5-input"]').send_keys(Keys.ENTER)  
            nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[8]/div[1]/div/label'))).click()

            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[1]/div[2]/input').send_keys(details[2].text)

            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[2]/div[5]/input').send_keys(details[3].text)
            land_size=((details[4].text))
            if "N/A" in land_size:
                pass
            else:

                driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[1]/div[3]/input').send_keys(details[4].text)

            driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[2]/div[3]/input').send_keys(details[7].text)
            df=driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[1]/div[4]/div/div/div[1]/div[1]').click()
            floor_level=((details[8].text))
            if "N/A" in floor_level:
                driver.find_element_by_xpath('//*[@id="react-select-3-input"]').send_keys("N/A")

            if "High" in floor_level:
                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'High')]")))

                nexts.click()
            if "Low" in floor_level:
                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Low')]")))

                nexts.click()
            if "Middle" in floor_level:
                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Medium')]")))

                nexts.click()

            if "Ground Floor" in floor_level:
                   
                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Ground')]")))

                nexts.click()        
            if "Penthouse" in floor_level:
                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Penthouse')]")))

                nexts.click()  


            df=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[1]/div[5]/div[1]/div/div[1]/div[1]').click()
            furnishing=((details[6].text))
            if "Partially" in furnishing:

                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Partial Furnished')]")))
                nexts.click()

            if "Fully" in furnishing:
                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Fully Furnished')]")))

                nexts.click()

            if "N/A" in furnishing:
                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Unfurnished')]")))

                nexts.click()

            if "Unfurnished" in furnishing:
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Unfurnished')]")))

                nexts.click()
                   
            if "Bare" in furnishing:
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Unfurnished')]")))

                nexts.click()
            lis=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[7]/div/div/textarea')
            lis.send_keys(desc.find('h5').text)

            phone=soup.find('span',{'class':'agent-phone-number agent-phone-number-original visible-print'}).text

            for strong_tag in desc.find_all('br'):
                descripton=(strong_tag.next_sibling)

                if "@" in descripton:
                    (descripton+phone)

                    lis=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[7]/div/div/textarea')
                    lis.send_keys(descripton+phone)
                else:
                    lis=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[7]/div/div/textarea')
                    lis.send_keys(descripton)
           
            if "Air-Conditioning" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Air conditioning')]")))
                nexts.click()  

            if "Intercom" in feature_list:
       
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Intercom')]")))
                nexts.click()

            if "Audio System" in feature_list:
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'AV Equipment')]")))
                nexts.click()

            if "Function room" in feature_list:

                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Meeting Rooms')]")))
                nexts.click()        

            if "Bathtub" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Bathtub')]")))
                nexts.click()        

            if "Cooker Hob / Hood" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Cooker Hob / Hood')]")))
                nexts.click()        
            if "Hairdryer" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Hairdryer')]")))
                nexts.click()  
            if "Handicap-friendly" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Handicap-friendly')]")))
                nexts.click()
            if "Intercom" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Intercom')]")))
                nexts.click()
            if "Jacuzzi" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Jacuzzi')]")))
                nexts.click()
            if "Meeting Rooms" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Meeting Rooms')]")))
                nexts.click()
            if "Private Pool" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Private Pool')]")))
                nexts.click()
            if "Internet Connection" in feature_list:

                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Broadband Internet')]")))
                nexts.click()
            if "Reception Services" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Reception Services')]")))
                nexts.click()        

            if "Restrooms" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Restrooms')]")))
                nexts.click()
            if "Audio System" in feature_list:

                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'AV Equipment')]")))
                nexts.click()

            if "Secretarial Services" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Secretarial Services')]")))
                nexts.click()
            if "Swimming Pool View" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Swimming Pool View')]")))
                nexts.click()

            if "Gymnasium room" in feature_list:
                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Gym')]")))
                nexts.click()

            if "Turnstile Control" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Turnstile Control')]")))
                nexts.click()
            if "Video Conferencing" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Video Conferencing')]")))
                nexts.click()

            if "Water Heater" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Water Heater')]")))
                nexts.click()

            if "Barbeque Area" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Barbeque Area')]")))
                nexts.click()

            if "Gym" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Gym')]")))
                nexts.click()

            if "Pavilion" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Pavilion')]")))
                nexts.click()

            if "Playground" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Playground')]")))
                nexts.click()

            if "Pool Deck" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Pool Deck')]")))
                nexts.click()

            if "Swimming Pool" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Swimming Pool')]")))
                nexts.click()

            if "Lap pool" in feature_list:

                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Swimming Pool')]")))
                nexts.click()
            feature_list.clear()

         
            nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[2]/div[3]/div[2]/div[5]/form/div[10]/div/button')))

            nexts.click()
            nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div/div/div[3]/div/button[2]'))).click()  
         
        # Remove the rent link.
        # rent_url_list.clear()
        # rent_urls_list.clear()
        driver.close()