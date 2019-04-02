from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.webdriver.common.by import By
from selenium import webdriver
from selenium.common.exceptions import WebDriverException
import time
import pandas as pd
URL="https://fynd.lk/explore?subcategory=Appliances%20Services"
# Start the WebDriver and load the page
wd = webdriver.Firefox()
wd.get(URL)

# Wait for the dynamically loaded elements to show up
WebDriverWait(wd, 10).until(
    EC.visibility_of_element_located((By.CLASS_NAME, "nav-menu-items")))

# And grab the page HTML source
html_page = wd.page_source
wd.quit()
npo_jobs = {}
# Now you can use html_page as you like
from bs4 import BeautifulSoup
soup = BeautifulSoup(html_page,'html.parser')
get_li_list= soup.findAll('li', {'class':'nav-menu-heading'} )

for lilist in get_li_list:
    list_sub_item = lilist.label.text
    if list_sub_item:
        wd1 = webdriver.Firefox()
        next_url= "https://fynd.lk/explore?subcategory="+list_sub_item
        wd1.get(next_url)
        WebDriverWait(wd1, 10).until(
        EC.visibility_of_element_located((By.CLASS_NAME, "nav-menu-items")))
        next_html_page = wd1.page_source
        nextsoup = BeautifulSoup(next_html_page,'html.parser')
        category_lists= soup.findAll('div', {'class':'category-item'} )
        #print(category_lists)
        i=0
	j=0
        for category_list in category_lists:
            if category_list:
                category_name=category_list.find('div',{'class':'category-name'})
                category_name_text=category_name.find('a').text
                #wd1.execute_script(return document.getElementsByClassName('category-item')["+str(i)+"].click()")
                clickafter = wd1.execute_script("return document.getElementsByClassName('category-item')["+str(i)+"].click()")
                i= i+1
                time.sleep(5)
                ext_click_page = wd1.page_source                
                soupclick = BeautifulSoup(ext_click_page,'html.parser')
                soupclick_list= soupclick.find('div', {'class':'company-list-container'} )
                company_item = soupclick_list.findAll('div',{'class':'company-item'})
                if company_item:
                        for data in company_item:
                                j=j+1
                                detail=data.find('div',{'class':'detail-sec'})
                                name=detail.find('a').text
                                btnsec= detail.find('div',{'class':'btn-sec'})
                                mobile_no=btnsec.find('span',{'class':'mat-button-wrapper'}).text
                                npo_jobs[j] = [list_sub_item, category_name_text, name,mobile_no]
                                #print("category="+list_sub_item+",category_name_text="+category_name_text+",mobile no="+mobile_no+",name="+name)
                                next_url= "https://fynd.lk/explore?subcategory="+list_sub_item        
                                wd1.get(next_url)
                                WebDriverWait(wd1, 10).until(
                                EC.visibility_of_element_located((By.CLASS_NAME, "nav-menu-items")))   
                else:
                        next_url= "https://fynd.lk/explore?subcategory="+list_sub_item        
                        wd1.get(next_url)
                        WebDriverWait(wd1, 10).until(EC.visibility_of_element_located((By.CLASS_NAME, "nav-menu-items"))) 
        break

npo_jobs_df = pd.DataFrame.from_dict(npo_jobs, orient = 'index', columns = ['Category','SubCategory','Name', 'Mobile'])
npo_jobs_df.head()
npo_jobs_df.to_csv('npo_jobs.csv')

        # category_items=category_list.findAll('div',{'class':'category-item-figure'})
        # for category_item in category_items:
        #     if category_item:
        #         wd1.execute_script('arguments[0].click()',JSON.encode(category_item))
        #         #wd1.find_element_by_link_text('img-responsive').click()
        #         # img=category_item.find('img',{'class':'img-responsive'})
        #         # time.sleep(1)
        #         # if img:
        #         #     print(img)
        #         #     img.click()
        # break
    
