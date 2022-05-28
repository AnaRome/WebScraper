#!/usr/bin/env python3

#Import libraries
from selenium import webdriver
from selenium.webdriver.common.by import By
from bs4 import BeautifulSoup
import pandas as pd
import time
from lxml import etree
from selenium.webdriver.common.by import By
from selenium.webdriver.common.action_chains import ActionChains
from selenium.webdriver.support.ui import WebDriverWait
from selenium.common.exceptions import TimeoutException
from selenium.webdriver.support import expected_conditions as EC
import random
from datetime import datetime 
from selenium.webdriver.firefox.options import Options
from selenium.common.exceptions import NoSuchElementException
from selenium.common.exceptions import MoveTargetOutOfBoundsException
from PIL import Image
import os



BASE_URL = "https://www.thredup.com" #helps with creating list of full links

item_links= []
page = 0
#save dataframes for each page
dfs =[]

#Track time
start_time= datetime.now()

# Configure options for webscraper
options = Options()
options.add_argument("--user-agent=Mozilla/5.0 (Windows NT 10.0; Win64; x64; rv:98.0) Gecko/20100101 Firefox/98.0")
options.add_argument("referer=https://www.google.com/")
options.add_argument('--headless')
#driver = webdriver.Firefox(options=options)
driver = webdriver.Firefox()

driver.get('https://www.thredup.com/women/dresses')
driver.maximize_window()

#Check if driver is working
print(driver.title)


#Choose how many pages to visit with scraper
while page <= 2:    
   
    #Surpass popups by 'x'ing out of popup if there or keeping going through rest of code
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//button[@aria-label='close']"))).click() 
    except TimeoutException:
        pass
    #Size popup
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//form/div[2]/button[contains(text(),'Skip this')]"))).click() 
    except TimeoutException:
        pass
    #Feedback popup
    try:
        WebDriverWait(driver,10).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'CLOSE')]"))).click() 
    except TimeoutException:
        pass
    #wait for page to load
    time.sleep(random.randint(10,20))  
    
    #store html content not js code
    page_source = driver.page_source
    soup = BeautifulSoup(page_source, 'html.parser')
    soup_fixed = BeautifulSoup(soup.prettify(), 'html.parser') # workaround to help with find_all function

    #Retrieve html that holds the href links
    item_list = soup_fixed.find_all('a', attrs={"class":"u-inset-0 u-absolute wAhTkKjWOmWyIy2F13MZ"})
    #print(item_list)
    for item in item_list:
        link = item.get('href')
        item_links.append(BASE_URL+link)
        
    #print('Retrieved this many items: ',len(item_links))
    
    ###### Click on each link of current page ######
    
    num_prods = len(item_list)
    data=[]
    count=0
    
    for num in range(num_prods):
        
        time.sleep(random.randint(15,25))
        #num_prods = len(driver.find_elements(By.CLASS_NAME,"u-inset-0 u-absolute wAhTkKjWOmWyIy2F13MZ"))
        
        
        #Check for popups on product pages
        #Find each element by div, remember XPATH uses index starting from 1 instead of 0
         #Size popup
        try:
            WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "//form/div[2]/button[contains(text(),'Skip this')]"))).click() 
        except TimeoutException:
            pass
        #Feedback popup
        try:
            WebDriverWait(driver,5).until(EC.element_to_be_clickable((By.XPATH, "//button[contains(text(),'CLOSE')]"))).click() 
        except TimeoutException:
            pass
        #Click on product link
        try:
            driver.execute_script("javascript:window.scrollBy(0,70)")
            time.sleep(random.randint(10,20))
            #prod_elems=WebDriverWait(driver,30).until(EC.element_to_be_clickable((By.XPATH, "/html/body/div[1]/div/main/div/div[3]/div[3]/div[2]/div[2]/div[1]/div["+ str(num) +"]"))).click()
            prod_elems=WebDriverWait(driver,45).until(EC.element_to_be_clickable((By.XPATH, '//div[@class="grid u-justify-center u-border u-border-t u-border-solid u-border-gray-0 md:u-border-0"]/div['+ str(num) +']'))).click()
            
            #Save Screenshot Image (Sanity Check)
            if (num % 40 == 0):
                driver.save_screenshot("product.png")

                # Loading the image
                p_image = Image.open("product.png")

                # Showing the image
                p_image.show()
                
        except NoSuchElementException:
            
            print("No Such Element Exception")            
            driver.save_screenshot("no_elem.png")

            # Loading the image
            no_image = Image.open("no_elem.png")

            # Showing the image
            no_image.show()
            continue
            
        except TimeoutException:
            print("Timeout Exception")
            driver.save_screenshot("time_out_elem.png")

            # Loading the image
            time_out_image = Image.open("time_out_elem.png")

            # Showing the image
            time_out_image.show()
            continue
        
       
        
        time.sleep(random.randint(10,15))
        #WebDriverWait(driver,random.randint(5,15))
        driver.execute_script("window.scrollTo(0,document.body.scrollHeight)")        
        pg_source = driver.page_source
        i_parse = BeautifulSoup(pg_source, 'html.parser')
        et = etree.HTML(str(i_parse)) #Use xpath with BS4

        #URL
        try:
            
            link = driver.current_url
                                   
        except:
            link = None
        
        #Brand

        try:
            brand=i_parse.find("a",{"class":"ui-link u-text-20"}).text
        except:
            brand = None

        #Item type
        try:
            i_type=i_parse.find("span",{"class":"wc1Wg5BbXVFBe4MHxY3r"}).text
        except:
            i_type = None


        #Size
        try:
            size=i_parse.find("div",{"class":"P9j6cGJ6kvC9bBgLk4pE"}).text
        except:
            size = None 

        #Price
        try:
            price=i_parse.find("span",{"class":"price u-font-bold u-text-20 u-text-alert"}).text.replace('\n',"")
        except:
            price = None
        
        #Original Price
        try:
            orig_price = i_parse.find("div",{"class":"u-text-gray-5 savings"}).find("span", {"class": "u-line-through"}).text.replace('\n',"")
        except:
            orig_price = None

        #Material
        try:
            get_material = et.xpath('//*[@id="root"]/div/main/div/div/section/div[2]/div[2]/div[1]/ul/li[1]')
            material=get_material[0].text
        except:
            material = None
        #Condition
        try:
            get_condition =et.xpath('//*[@id="root"]/div/main/div/div/section/div[2]/div[2]/div[3]/ul/li') 
            condition= get_condition[0].text
        except:
            condition = None
            
         #Item ID
        try:
            get_id = et.xpath('//*[@id="root"]/div/main/div/div/section/div[2]/div[2]/div[1]/ul/li[last()]')
            p_id = get_id[0].text
        except:
            p_id = None

        #create dictionary
        clothing = {'URL': link,
                    'Brand': brand,
                   'Item Type': i_type,
                   'Size': size,
                   'Price': price,
                    'Original Price': orig_price,
                   'Material': material,
                   'Condition': condition,
                   'Item ID': p_id}

        data.append(clothing)
        
        #Count successes
        count=count+1
        
        #driver.back()
        time.sleep(10)
        try:
            driver.execute_script("window.history.go(-1)")
        except:
            time.sleep(10)
            driver.execute_script("window.history.go(-1)")
            
        time.sleep(5) 
    
    
    #####PAGE COMPLETE####
    
    #How many product links were found on page
    print("Found ", num_prods," items on page ", page+1)
    
    #Number of products added to datafame
    print("Number of items added to dataframe:",len(data))
    
    
    #Save Data
    df = pd.DataFrame(data)
    dfs.append(df)
    next_page = driver.find_element(By.XPATH,'//button[text()="Next"]')
    next_page.click()
    page += 1
    #print(item_links)
    
#print(page_source)


driver.quit()

#Final data output
df_final = pd.concat(dfs)
print("Total number of entries added: ", len(df_final))
tu_output = 'tu_ouput.csv'
df_final.to_csv(tu_output,mode='a', index= False, header= not os.path.exists(tu_output))
elasped_time = datetime.now()- start_time
print(elasped_time)





