#python3
#main.py
#request,os,beautifulsoup(bs4),pyperclip,sys,webbrowser -imports
#use request,os,bs4 



#This is a web scraping project to download manhwa(comic)korean based
#website used to scrape website: https://manhwaclan.com/


#link should look like this
# protocol  domain        manga    manhwa name
# https://manhwaclan.com/manga/overlord-of-insects/

import requests
import os 
import bs4
import time


class Comic():

    def __init__(self, **kwargs):
        try:
            self.website_url_with_name = kwargs['website_url_with_name']
            self.foldername = kwargs['foldername'] 
        except KeyError:
            print("Keyword missing...")

    def download_chapter(self, url, chapter_index):
        page_res = requests.get(url)
        page_res.raise_for_status()
        soup = bs4.BeautifulSoup(page_res.text, "html.parser")
        elements = soup.select('.page-break img')
        img_src = []
        for i in elements:
            img_src.append(i.get('src').strip())
        print(f"Downloading Chapter {chapter_index + 1}...")
        for link in range(len(img_src)):
            res = requests.get(img_src[link])
            res.raise_for_status()
            filename = f"{link}.webp"
            if os.path.exists(filename):
                print(f"Skipping {filename}. Already downloaded.")
                continue
            with open(filename, 'wb') as fi:
                for chunk in res.iter_content(100000):
                    fi.write(chunk)
        print(f"Download of Chapter {chapter_index + 1} complete.")

    def download_all_chapters(self):
        print("Script started...")
        try:
            page_response = requests.get(self.website_url_with_name)
            page_response.raise_for_status()

            soup = bs4.BeautifulSoup(page_response.text, "html.parser")
            elements = soup.select(".wp-manga-chapter a")
            extracted_chapter_links = []
            for link in elements:
                href = link.get('href').strip()
                if href not in extracted_chapter_links:
                    extracted_chapter_links.append(href)
            
            os.makedirs(self.foldername, exist_ok=True)
            os.chdir(self.foldername)

            for index, link in enumerate(reversed(extracted_chapter_links)):
                chapter_folder = f"Chapter {index + 1}"
                if os.path.exists(chapter_folder):
                    print(f"Skipping {chapter_folder}. Already exists.")
                    continue
                os.makedirs(chapter_folder)
                os.chdir(chapter_folder)

                self.download_chapter(url=link, chapter_index=index)
                os.chdir('..')  
                time.sleep(0.99)

            print(f"Manhwa '{self.foldername}' downloaded successfully.")
 
        except Exception as e:
            print(f"Error: {e}")
        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")

    


url = "https://manhwaclan.com/manga/im-the-only-one-bullied-by-the-new-high-school-student/"
foldername = "highschoolstudent"

manhwa = Comic(website_url_with_name=url, foldername=foldername)
manhwa.download_all_chapters()

