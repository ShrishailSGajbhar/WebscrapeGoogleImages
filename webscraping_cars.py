import bs4
import requests
import pathlib
import os 
import time 
from selenium import webdriver

def download_image(url, folder_name, num):

    # write image to file
    reponse = requests.get(url)
    if reponse.status_code==200:
        with open(os.path.join(folder_name, str(num)+".jpg"), 'wb') as file:
            file.write(reponse.content)

image_search_query = "Indian cars"
url_query = "+".join(image_search_query.split())

# get the folder name for saving the search query results
folder_name = "_".join([x.lower() for x in image_search_query.split()])
# print(folder_name)

#creating a directory to save images
pathlib.Path(folder_name).mkdir(parents=True, exist_ok=True)

chrome_driver_path = r"/home/shrishail/ext_bins/chromedriver_linux64/chromedriver"
options = webdriver.ChromeOptions()
options.add_experimental_option("detach", True)
driver = webdriver.Chrome(options=options, executable_path=chrome_driver_path)
driver.maximize_window()

search_URL = f"https://www.google.com/search?q={url_query}&source=lnms&tbm=isch"
driver.get(search_URL)

a = input("Waiting...")
#Scrolling all the way up
driver.execute_script("window.scrollTo(0, 0);")

page_html = driver.page_source
pageSoup = bs4.BeautifulSoup(page_html, 'html.parser')
containers = pageSoup.findAll('div', {'class':"isv-r PNCib MSM1fd BUooTd"} )

print(len(containers))

len_containers = len(containers)

for i in range(1, len_containers+1):
    if i % 25 == 0:
        continue
    xPath = f"""//*[@id="islrg"]/div[1]/div[{i}]"""
    if i>=51:
        xPath = f"""//*[@id="islrg"]/div[1]/div[51]/div[{i-51+1}]"""
    if i>=101:
        xPath = f"""//*[@id="islrg"]/div[1]/div[52]/div[{i-101+1}]"""
    if i>=201:
        xPath = f"""//*[@id="islrg"]/div[1]/div[53]/div[{i-201+1}]"""
    if i>=301:
        xPath = f"""//*[@id="islrg"]/div[1]/div[54]/div[{i-301+1}]"""
    if i>=401:
        xPath = f"""//*[@id="islrg"]/div[1]/div[55]/div[{i-401+1}]"""
    if i>=501:
        xPath = f"""//*[@id="islrg"]/div[1]/div[56]/div[{i-501+1}]"""
    previewImageXPath = xPath+"""/a[1]/div[1]/img"""
    previewImageElement = driver.find_element("xpath",previewImageXPath)
    previewImageURL = previewImageElement.get_attribute("src")
    #print("preview URL", previewImageURL)

    # //*[@id="islrg"]/div[1]/div[51]/div[4]
    # //*[@id="islrg"]/div[1]/div[52]/div[3]
    # //*[@id="islrg"]/div[1]/div[52]/div[1]

    #print(xPath)


    driver.find_element("xpath",xPath).click()
    #time.sleep(3)

    #//*[@id="islrg"]/div[1]/div[16]/a[1]/div[1]/img

    #input('waawgawg another wait')

    # page = driver.page_source
    # soup = bs4.BeautifulSoup(page, 'html.parser')
    # ImgTags = soup.findAll('img', {'class': 'n3VNCb', 'jsname': 'HiaYvf', 'data-noaft': '1'})
    # print("number of the ROI tags", len(ImgTags))
    # link = ImgTags[1].get('src')
    # #print(len(ImgTags))
    # #print(link)
    #
    # n=0
    # for tag in ImgTags:
    #     print(n, tag)
    #     n+=1
    # print(len(ImgTags))

    #/html/body/div[2]/c-wiz/div[3]/div[2]/div[3]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img

    #It's all about the wait

    timeStarted = time.time()
    while True:

        imageElement = driver.find_element("xpath","""//*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]""")
        # //*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]
        # //*[@id="Sva75c"]/div[2]/div/div[2]/div[2]/div[2]/c-wiz/div/div/div/div[3]/div[1]/a/img[1]
        imageURL= imageElement.get_attribute('src')

        if imageURL != previewImageURL:
            #print("actual URL", imageURL)
            break

        else:
            #making a timeout if the full res image can't be loaded
            currentTime = time.time()

            if currentTime - timeStarted > 10:
                print("Timeout! Will download a lower resolution image and move onto the next one")
                break


    #Downloading image
    try:
        download_image(imageURL, folder_name, i)
        print("Downloaded element %s out of %s total. URL: %s" % (i, len_containers + 1, imageURL))
    except:
        print("Couldn't download an image %s, continuing downloading the next one"%(i))

    #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img
    #//*[@id="Sva75c"]/div/div/div[3]/div[2]/c-wiz/div/div[1]/div[1]/div[2]/div[1]/a/img
