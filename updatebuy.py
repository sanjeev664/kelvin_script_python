from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait, Select
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
from bs4 import BeautifulSoup
from selenium.webdriver.common.proxy import Proxy, ProxyType
from selenium import webdriver
from selenium.webdriver.support.wait import WebDriverWait
from selenium.webdriver.support import expected_conditions as ec
from selenium.common.exceptions import TimeoutException
# import requests
import time
from selenium.webdriver.support.ui import Select
import urllib.request
# import pytesseract
from PIL import Image, ImageFilter ,ImageDraw
# from pytesseract import pytesseract
import PIL
import urllib.request
import os
from selenium.webdriver.support.ui import Select
from selenium.webdriver.common.keys import Keys
import pandas as pd
from urllib3 import add_stderr_logger
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

############################################ code for buy ##############################################
driver = webdriver.Chrome('/home/hp/workspace/shubham/chromedriver')

try:
    driver.close()
except:
    pass

try:    
    df=pd.read_csv('/home/hp/workspace/shubham/kenlvin/Accounts1.csv')
    urls=df['Agent url'].dropna().tolist()
    emails=df['Email login'].dropna().tolist()
    passwords=df['Password'].dropna().tolist()
    url_list.clear()
    urls_list.clear()

    def buy_property():
        res = driver.page_source
        soup = BeautifulSoup(res, 'html.parser')
        try:
            data = soup.find('div', {'class': 'carousel-container'})
            cards = data.find_all('a', {'class': 'listing-card-link listing-img-a'})
            for card in cards:
                link = card.get('href')
                print(link)
                url_list.append(link)
            # print("Property List :", url_list)
        except:
            pass
    
    def sale_property_with_listing(links):
        # print("url", url)
        driver.get(links)
        time.sleep(5)
        driver.delete_all_cookies()
        res = driver.page_source
        soup = BeautifulSoup(res, "html.parser")
        time.sleep(5)
        try:
            data = soup.find("div", {"class": "listing-widget-new small-listing-card"})
            links = data.find_all("a", {"class": "nav-link"})
            for i in links:
                link = i.get("href")
                if "#contact-agent" not in link:
                    if link not in url_list:
                        url_list.append(link)
            print(len(url_list))
            print(url_list)

            # try:
                # time.sleep(5)
            
            # except:
            #     pass

        except:
            pass
        # try: 
        button = WebDriverWait(driver, 15).until(EC.element_to_be_clickable((By.XPATH('//*[@id="search-results-container"]/div[2]/div[1]/div[2]/div[2]/section/div[5]/ul/li[4]/a'))))
        if button.click():

            print("cliked")
        time.sleep(10)
        driver.delete_all_cookies()
        res = driver.page_source
        soup = BeautifulSoup(res, "html.parser")
        data = soup.find("div", {"class": "listing-widget-new small-listing-card"})
        links = data.find_all("a", {"class": "nav-link"})
        for i in links:
            link = i.get("href")
            if "#contact-agent" not in link:
                if link not in url_list:
                    url_list.append(link)

    for i in range(0, len(urls)):
        agent_url = (urls[i])
        email = emails[i]
        password = passwords[i]
        driver = webdriver.Chrome('/home/hp/workspace/shubham/chromedriver')

        driver.get(agent_url)
        driver.delete_all_cookies()              
        driver.maximize_window()

        try:
            WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div[2]/div/div/div[2]/div/button'))).click()
        except:
            pass

        res = driver.page_source

        soup = BeautifulSoup(res, 'html.parser')
   
        try:
            WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div[6]/div[6]/div/div/div[1]/div/button[1]'))).click()
            driver.delete_all_cookies() 
            time.sleep(10)   
            buy_property()
        except:
            pass
        
        sale_count = soup.find("span", {"data-automation-id": "stat-listings-for-sale"})

        print("Count sale :", sale_count.text)
        # data-automation-id="stat-listings-for-sale"

        if int(sale_count.text) > 0:
            elems = driver.find_elements_by_css_selector(".more-link-wrapper [href]")
            links = [elem.get_attribute('href') for elem in elems]
            print("Link for the more poperr ur rir ", links)
            time.sleep(5)
            sale_property_with_listing(links[0])

        # try:
        #     WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/div[5]/div/div/section/div[8]/div[3]/ul/li[4]/a'))).click()
        #     buy_property()
        # except:
        #     pass

        ################################################################################################################          
        driver.delete_all_cookies()              


        for i in range(0,len(url_list)):        
        # for i in range(0,1):        
            driver.delete_all_cookies()
            u = (url_list[i])
            if "commercialguru.com.sg" in u:

                s = u.replace('https://www.propertyguru.com.sg/','')
                driver.get("https://www.propertyguru.com.sg/listing/23603697/for-sale-brand-new-3-5sty-9bdrms-lift-pool-walk-to-mrt-designer-decor")
                # print(s)
                driver.delete_all_cookies()  
               
               
            else:  
                driver.get(u)
                driver.delete_all_cookies() 
            res = driver.page_source
            soup = BeautifulSoup(res, 'html.parser')
           
       
            address = soup.find('div', {'class': 'listing-address'})
            postalCode = address.find('span',{'itemprop': 'postalCode'}).text

            name = soup.find('div', {'class': 'listing-title text-transform-none'})
            print(name.text)
            name_list.append(name)
       
            price = soup.find('span', {'class': 'element-label price'})

            price_list.append(price)

            no_of_bedroom = soup.find('div',{'class':'property-info-element beds'})
            try:
                no_of_bedrooms = no_of_bedroom.find('span',{'class':'element-label'})
            except:
                no_of_bedrooms = "no"

            no_of_bathroom = soup.find('div',{'class':'property-info-element baths'})
            try:
                no_of_bathrooms = no_of_bathroom.find('span',{'class':'element-label'})
            except:
                no_of_bathrooms="no"

            # details = soup.find_all('div', {'class':'value-block'})
            detail = soup.find("div", {"class": "listing-details-primary"})
            details = detail.find_all('td', {'class': 'value-block'})

            # print("Details :", details)
            # try:
            # nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Read More')]"))).click()
            # nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[2]/div/div/section[1]/div/div[4]/div/div/div/section/div[2]/div/div[2]/a[1]/span[1]'))).click()


            desc = soup.find('div', {'class':'listing-details-text compacted'})
            print(desc.text)

            # feture=soup.find_all('span',{'itemprop':'name'})
            # for feture in feture:
            #     (feature_list.append(feture.text))
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

            for imge in imge:

                photo=imge.find_all('img')

                for i in photo:

                    src = i.get('data-original')
                    if "https" in src:

                        x = src.replace("C80X60", "V800")

                        req = urllib.request.Request(x, headers={'User-Agent': '*'})
                        response = urllib.request.urlopen(req)
                        html = urllib.request.urlopen(req).read()
                        with open('/home/hp/workspace/shubham/images/img'+str(image_count)+'.jpeg', 'wb') as f:
                            f.write(html)
                            image_count = image_count+1
                            count.append(image_count)
            for counts in count:
                   
            #   imge = Image.open('/home/sunil/workspace/scraping/kelvin/images'+str(counts)+'.jpeg')
                try:
                    imge = Image.open('/home/hp/workspace/shubham/images/img'+str(counts)+'.jpeg')
               
                    hight=imge.size
                    a=imge.size
                    newsize = (800, 600)
                    im1 = imge.resize(newsize)
                    mask = Image.new('L', im1.size, 0)
                    draw = ImageDraw.Draw(mask)
                    draw.rectangle([ (610,425), (900,360)], fill=260)
                    draw.rectangle([ (425,445), (900,400)], fill=260)
                    img3=im1.filter(ImageFilter.GaussianBlur(48))
                    im1.paste(img3,mask=mask)              
                    im1.save('/home/hp/workspace/shubham/images/img'+str(counts)+'.jpeg')

                except:
                    pass


            try:
                driver.get("https://myestate.sg/agent/login")
            except:    
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

            time.sleep(5)
            nexts=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Next')]")))
            driver.execute_script("arguments[0].click();", nexts)

            try:
                for counts in count:

                    image_path=os.path.abspath('/home/hp/workspace/shubham/images/img'+str(counts)+'.jpeg')
                    lis= driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[4]/div[3]/div/input')
                    lis.send_keys(image_path)
                    os.remove('/home/hp/workspace/shubham/images/img'+str(counts)+'.jpeg')

            except:
                pass

            (count.clear())
            time.sleep(5)
            driver.find_element_by_xpath('/html/body/div[1]/div[2]/div[3]/div[2]/div[4]/div[5]/button[2]').click()
            nexts=WebDriverWait(driver, 20).until(EC.presence_of_element_located((By.XPATH,"//*[contains(text(),'Next')]")))
            # try:
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
            print(building_output)
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

            Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[1]/div/select')).select_by_visible_text('For Sale')
            # print("Number Of Bathrooms : ", str(no_of_bathroom.text))
            if no_of_bedrooms != "no":
                if str(no_of_bedrooms.text) > "5":
               
                    Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[3]/div/select')).select_by_value('5')
                else:
                    Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[3]/div/select')).select_by_value(no_of_bedrooms.text)
            else:
                Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[3]/div/select')).select_by_value('-2')

            if no_of_bathrooms != "no":

                    if str(no_of_bathrooms.text)> "5":
                        Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[4]/div/select')).select_by_value('5')
                    else:

           
                        Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[4]/div/select')).select_by_value(no_of_bathrooms.text)
            else:
                Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[4]/div/select')).select_by_value('0')


            # else:
            #     try:

            #         Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[4]/div/select')).select_by_value(no_of_bathrooms.text)
            #     except:
            #         Select(driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[4]/div[4]/div/select')).select_by_value('0')

            for i in range(0, len(details)):
                print('No.', i)
                print(details[i])

            s = (details[0].text).replace('For Sale','')

            # s = (details[0].text).replace('For Sale','')
            print(s,"ssss")
            if "Fa" in s:
                driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys("Fa")
                driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(Keys.ENTER)
                df=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[2]/div[1]/div[1]/div/div[1]/div[1]').click()
            else:
                driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(s)
                driver.find_element_by_xpath('//*[@id="react-select-2-input"]').send_keys(Keys.ENTER)
                df=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[2]/div[1]/div[1]/div/div[1]/div[1]').click()  

            s=(details[1].text)
            if s != "N/A":
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), '{}')]".format(s))))

                nexts.click()
            else:
                driver.find_element_by_xpath('//*[@id="react-select-5-input"]').send_keys('un')
                driver.find_element_by_xpath('//*[@id="react-select-5-input"]').send_keys(Keys.ENTER)


               
            nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[8]/div[1]/div/label'))).click()

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
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'High')]")))

                nexts.click()
            if "Low" in floor_level:
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Low')]")))

                nexts.click()
            if "Middle" in floor_level:
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Medium')]")))

                nexts.click()


            if "Ground Floor" in floor_level:
               
                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Ground')]")))

                nexts.click()    
            if "Penthouse" in floor_level:
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Penthouse')]")))

                nexts.click()  


           
            df=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[6]/div[1]/div[5]/div[1]/div/div[1]/div[1]').click()
            furnishing=((details[6].text))
            if "Partially" in furnishing:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Partial Furnished')]")))
                nexts.click()

            if "Fully" in furnishing:
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Fully Furnished')]")))

                nexts.click()

            if "N/A" in furnishing:
                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(), 'Unfurnished')]")))

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

                if "@" in descripton or "Call" in descripton:
                   

                    lis=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[7]/div/div/textarea')
                    lis.send_keys(descripton+phone)
                else:
                    lis=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[7]/div/div/textarea')
                    lis.send_keys(descripton)
               
                # lis=driver.find_element_by_xpath('//*[@id="app"]/div[2]/div[3]/div[2]/div[5]/form/div[7]/div/div/textarea')
                # lis.send_keys(descripton)

            if "Air-Conditioning" in feature_list:

                nexts= WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Air conditioning')]")))
                nexts.click()    
            if "AV Equipment" in feature_list:
                nexts= WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'AV Equipment')]")))
                nexts.click()        

            if "Bathtub" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Bathtub')]")))
                nexts.click()        

            if "Cooker Hob/Hood" in feature_list:

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
            if "Reception Services" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Reception Services')]")))
                nexts.click()        

            if "Restrooms" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Restrooms')]")))
                nexts.click()
            if "Secretarial Services" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Secretarial Services')]")))
                nexts.click()
            if "Swimming Pool View" in feature_list:

                nexts=WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Swimming Pool View')]")))
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

                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Pavilion')]")))
                nexts.click()
            if "Playground" in feature_list:

                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Playground')]")))
                nexts.click()
            if "Pool Deck" in feature_list:

                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Pool Deck')]")))
                nexts.click()
            if "Swimming Pool" in feature_list:

                nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,"//*[contains(text(),'Swimming Pool')]")))
                nexts.click()
            feature_list.clear()    
            nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[1]/div[2]/div[3]/div[2]/div[5]/form/div[10]/div/button')))

            nexts.click()
            nexts = WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH,'/html/body/div[3]/div[2]/div/div/div[3]/div/button[2]'))).click()

        # except:
        #     pass
        url_list.clear()
        urls_list.clear()
        driver.close()
except:
    pass        