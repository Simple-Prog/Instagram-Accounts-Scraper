import re, requests
import pandas as pd
import threading, time, sys
from bs4 import BeautifulSoup


# Global Vars:
ALL_EXCEL_SHEETS = [
    'Christianity',
    'Community Resource', 
    'Complementary or Alternative He', 
    'Core Health Care', 
    'Ecumen & IntFaith Orgs.', 
    'Education in the Arts', 
    'Educational org. not elsewhere ', 
    'Environment', 
    'Foundations', 
    'Foundations Advancing Education', 
    'Foundations Advancing Religions', 
    'Foundations Relieving Poverty', 
    'Health Care Products', 
    'Islam', 
    'Judaism',
    'National Arts Service Organizat', 
    'Organizations Relieving Poverty', 
    'Other Religions', 
    'Protective Health Care', 
    'Public Amenities', 
    'Relief of the Aged', 
    'Research', 
    'Support of Religion',  
    'Support of schools and educatio', 
    'Supportive Health Care', 
    'Teaching Institutions', 
    'Upholding Human Rights'
    ]

THREAD_DELAY = 0.1

SITE_ROUTES = [
    "",
    "/about",
    "/about-us",
    "/contact",
    "/contact-us",
    "/news-media",
    "/news"
]

INPUT_EXCEL_FILE = "./instagram_charities.xlsx"

OUTPUT_EXCEL_FILE = "./output_instagram_charities.xlsx"

    
# Helper Functions:
def scrape_site(url: str , df: pd.DataFrame , index: int):
    
    if pd.isnull(url):
        sys.exit()
    
    session = requests.Session()
    headers = {
        "accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/avif,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.7",
        "accept-language": "en-US,en;q=0.9",
        "priority": "u=0, i",
        "sec-ch-ua": '"Not)A;Brand";v="99", "Google Chrome";v="127", "Chromium";v="127"',
        "sec-ch-ua-mobile": "?0",
        "sec-ch-ua-platform": "Windows",
        "sec-fetch-dest": "document",
        "sec-fetch-mode": "navigate",
        "sec-fetch-site": "none",
        "sec-fetch-user": "?1",
        "upgrade-insecure-requests": "1",
        "user-agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/127.0.0.0 Safari/537.36"
    }
    
    for route in SITE_ROUTES:
        try:
            new_url = "https://" + url + route
            response = session.get(
                url = new_url,
                headers = headers,
                timeout=20
                )
            
            soup = BeautifulSoup(response.text , "html.parser")
            all_anchor_tags = soup.find_all("a")
            
            instagram_done = False
            facebook_done = False

            for a_tag in all_anchor_tags:
                try:
                    if "instagram" in a_tag["href"]:
                        # print(a_tag)
                        instagram_url = a_tag["href"]
                        print(instagram_url)
                        # print(f"Scraped {new_url}")
                        df.at[index , "Instagram Accounts"] = instagram_url
                        instagram_done = True
                    elif "facebook" in a_tag["href"]:
                        facebook_url = a_tag["href"]
                        print(facebook_url)
                        df.at[index , "Facebook Accounts"] = facebook_url
                        facebook_done = True
                        
                    if instagram_done and facebook_done:
                        sys.exit()

                except Exception as e:
                    continue
        except Exception as e:
            print(e)
            continue
        
# Main Program Execution:
if __name__ == "__main__":
    excel_file_data = pd.ExcelFile(INPUT_EXCEL_FILE)
    
    for sheet_name in ALL_EXCEL_SHEETS:
        try:
            df = pd.read_excel(io=INPUT_EXCEL_FILE , sheet_name=sheet_name)
            df["Instagram Accounts"] = None
            df["Facebook Accounts"] = None
            
            total_rows = len(df)
            url_column = df["Contact URL"]
            
            print(f"Scraping Total {total_rows} Urls.")
            
            all_threads = []
            for i in range(0 , total_rows):
                thread = threading.Thread(target=scrape_site , args=(url_column[i] , df , i))
                all_threads.append(thread)
                thread.start()
                time.sleep(THREAD_DELAY)

            for thread in all_threads:
                thread.join()
                
            print(f"Scraping For {sheet_name} Complete.")
            
            # with pd.ExcelWriter(OUTPUT_EXCEL_FILE , mode="w") as writer:
            #     df.to_excel(excel_writer=writer , sheet_name=sheet_name)
                
            with pd.ExcelWriter(OUTPUT_EXCEL_FILE , mode="a") as writer:
                df.to_excel(excel_writer=writer , sheet_name=sheet_name)
                
        except Exception as e:
            print(e)