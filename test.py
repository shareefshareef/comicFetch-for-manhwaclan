import requests
import os 
import bs4
import time

#this is the first code of main.py with errors 

class Comic():

    def __init__(self,**kwargs):
        try:
            self.website_url_with_name = kwargs['website_url_with_name']
            self.foldername = kwargs['foldername'] #directory name
        except:
            print("keyword Missing...")

    def download_chapter(self,url):
        page_res = requests.get(url)
        page_res.raise_for_status()
        soup = bs4.BeautifulSoup(page_res.text,"html.parser")
        elements = soup.select('.page-break img')
        img_src = []
        for i in elements:
            img_src.append(i.get('src').strip())
        print("downloading started.")
        for link in range(len(img_src)):
            res = requests.get(img_src[link])
            res.raise_for_status()
            fi = open(str(link)+".webp",'wb')
            for chunk in res.iter_content(100000):
                fi.write(chunk)
            fi.close()

        print("download end...")



    def download_all_chapters(self):
        print("script started...")
        try:

            page_response = requests.get(self.website_url_with_name) #manhwa page req
            page_response.raise_for_status()

            soup = bs4.BeautifulSoup(page_response.text,"html.parser")
            elements = soup.select(".wp-manga-chapter a")
            extracted_chapter_links = []
            for links in elements:
                extracted_chapter_links.append(links.get('href').strip())
            

            folder = os.makedirs(self.foldername,exist_ok=True)
            os.chdir(self.foldername)

            for link in range(len(extracted_chapter_links)-1,-1,-1):
                sub_folder = os.makedirs(str(link))
                os.chdir(str(link))
                

                self.download_chapter(url=extracted_chapter_links[link])
                os.chdir(self.foldername)
                time.sleep(0.99)

            print(f"manhwa {self.foldername} downloaded...")
 
        except Exception as e:
            print(f"Errors: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

        
        
url = "https://manhwaclan.com/manga/the-beginning-after-the-end-side-story-jasmine-wind-borne/"
foldername = "Begningaftertheend"

manhwa = Comic(website_url_with_name=url,foldername=foldername)

manhwa.download_all_chapters()
