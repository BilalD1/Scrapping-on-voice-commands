import requests
from bs4 import BeautifulSoup
import re
import time
import selenium
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.firefox.options import Options
from selenium.webdriver.firefox.service import Service

options = Options()
options.add_argument("--headless")


def extract_integers_from_html(html):
    soup = BeautifulSoup(html, 'html.parser')
    text = soup.get_text()  # Extract text from HTML
    integers = re.findall(r'\d+', text)
    return [int(i) for i in integers]

class Scrapers:
    def run_scraper(self, keyword):
    ##########################################- Pub Med -##########################################
        print("Starting Pub Med Scrapper")
        base_url = 'https://pubmed.ncbi.nlm.nih.gov/'
        pubmedlink = base_url+'?term=' + keyword
        response = requests.get(pubmedlink)
        html_content = response.text
        integers = extract_integers_from_html(html_content)
        j = 0
        pubmed = []
        for i in integers:
            if j>=7:
                break
            i = str(i)
            if len(i)==8:
                j = j+1
                url = base_url + i +'/'
                pubmed.append(url)
                

    ########################################-IEEE Scrapers-############################################
        print("Starting IEEE Scrapper")
        url = 'https://ieeexplore.ieee.org/rest/search'
        headers = {
            'Accept': 'application/json, text/plain, */*',
            'Accept-Encoding': 'gzip, deflate, br',
            'Accept-Language': 'en-US,en;q=0.9',
            'Connection': 'keep-alive',
            'Content-Length': '120',
            'Content-Type': 'application/json',
            'DNT': '1',
            'Host': 'ieeexplore.ieee.org',
            'Origin': 'https://ieeexplore.ieee.org',
            'Referer': 'https://ieeexplore.ieee.org/search/searchresult.jsp?newsearch=true&queryText=' + keyword,
            'Sec-Fetch-Dest': 'empty',
            'Sec-Fetch-Mode': 'cors',
            'Sec-Fetch-Site': 'same-origin',
            'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_7) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/113.0.0.0 Safari/537.36',
            'sec-ch-ua': '"Google Chrome";v="113", "Chromium";v="113", "Not-A.Brand";v="24"',
            'sec-ch-ua-mobile': '?0',
            'sec-ch-ua-platform': '"macOS"'
        }
        payload = {
            "newsearch": True,
            "queryText": keyword,
            "highlight": True,
            "returnFacets": [
                "ALL"
            ],
            "returnType": "SEARCH",
            "matchPubs": True
        }

        ieee = []
        response = requests.post(url, headers=headers, json=payload)
        data = response.json()
        records = data.get('records', [])
        for record in records:
            title = record.get('articleTitle')
            Link = record.get('documentLink')

            #print('Title: ', title)
            url = "https://ieeexplore.ieee.org" + Link
            ieee.append(url)

    #########################################-ACM Digital Library-#########################################
        print("Starting ACM Scrapper")
        driver = webdriver.Firefox(options=options)
        driver.get("https://dl.acm.org/action/doSearch?AllField="+keyword)
        i = 0
        results = driver.find_elements(By.CSS_SELECTOR,'.dot-separator')
        acm = []
        try:
            for result in results:
                if i>=7:
                    break
                url = result.get_attribute('href')
                if url == None:
                    continue
                acm.append(url)
                i = i + 1
        except:
            print("ACM Scrapping Failed")
        try:
            driver.quit()
            del driver
        except:
            pass

    #########################################-WHO Scrapper-############################################
        print("Starting WHO Scrapper")
        driver = webdriver.Firefox(options=options)
        driver.get("https://www.who.int/home/search?indexCatalogue=genericsearchindex1&searchQuery="+keyword+"&wordsMode=AnyWord")
        results = driver.find_elements(By.CSS_SELECTOR,'.sf-cn-NewsItem')
        i = 0
        who = []
        try:
            for result in results:
                links = result.find_elements(By.TAG_NAME,"a")
                if i>=7:
                    break
                for link in links:
                    url = link.get_attribute('href')
                    if url.startswith("https://www.who.int/publications") or url.startswith("https://www.who.int/news"):
                        who.append(url)
                        i = i+1
        except:
            print("WHO scrapping failed")
        try:
            driver.quit()
            del driver
        except:
            pass

    ###################################################-Arxiv-###################################################
        print("Starting Arxiv Scrapper")
        driver = webdriver.Firefox(options=options)
        driver.get("https://arxiv.org/search/?searchtype=all&query="+keyword+"&abstracts=show&size=50&order=")
        i = 0
        results = driver.find_elements(By.CSS_SELECTOR,'.is-marginless')
        arxiv = []
        try:
            for result in results:
                if i>=5:
                    break
                links = result.find_elements(By.TAG_NAME,"a")
                for link in links:
                    url = link.get_attribute('href')
                    if url.startswith("https://arxiv.org/abs"):
                        i = i+1
                        arxiv.append(url)
        except:
            print("Arxiv Scrapping Failed")

        try:
            driver.quit()
            del driver
        except:
            pass

    #############################################-NLM-######################################
        print("Starting NLM Scrapper")
        driver = webdriver.Firefox(options=options)
        driver.get("https://vsearch.nlm.nih.gov/vivisimo/cgi-bin/query-meta?query="+keyword+"&v%3Aproject=nlm-main-website&_gl=1*15ubsco*_ga*MjAxNzI0MDgyMC4xNjgzMTgwMzk5*_ga_7147EPK006*MTY4NDkwNTM1NS4xLjEuMTY4NDkwNjQyMy4wLjAuMA..*_ga_P1FPTH9PL4*MTY4NDkwNTM1NS4xLjAuMTY4NDkwNTM1NS4wLjAuMA..")
        results = driver.find_elements(By.CSS_SELECTOR,'.title')
        i = 0
        nlm = []
        try:
            for result in results:
                if i>=5:
                    break
                url = result.get_attribute('href')
                i = i+1
                nlm.append(url)
        except:
            pass
        try:
            driver.quit()
            del driver
        except:
            pass

    #############################################-EMBL-##########################################
        print("Starting EMBL Scrapper")
        driver = webdriver.Firefox(options=options)
        driver.get("https://www.ebi.ac.uk/ebisearch/search?db=ebiweb&query="+keyword+"&size=15&requestFrom=searchBox")
        time.sleep(5)
        results = driver.find_elements(By.CSS_SELECTOR,'.vf-link')
        time.sleep(5)
        embl = []
        try:
            for result in results:
                url = result.get_attribute('href')
                if url == None:
                    continue
                elif url.startswith("https://www.ebi.ac.uk/ebisearch") or url.startswith("https://www.ebi.ac.uk/about") or url.startswith("https://www.ebi.ac.uk/ols"):
                    continue
                if url.startswith("https://www.ebi.ac.uk/"):
                    embl.append(url)
        except:
            pass
        try:
            driver.quit()
            del driver
        except:
            pass
    #########################################-Cohrane-################################################
        print("Starting Cohrane Library Scrapper")
        cohrane = []
        driver = webdriver.Firefox(options=options)
        driver.get("https://www.cochranelibrary.com/search?p_p_id=scolarissearchresultsportlet_WAR_scolarissearchresults&p_p_lifecycle=0&_scolarissearchresultsportlet_WAR_scolarissearchresults_searchType=basic&_scolarissearchresultsportlet_WAR_scolarissearchresults_searchBy=1&_scolarissearchresultsportlet_WAR_scolarissearchresults_searchText="+keyword)
        results = driver.find_elements(By.CSS_SELECTOR,'.search-results-item-body')
        i = 0
        try:
            for result in results:
                if i>=7:
                    break
                elements = result.find_elements(By.CSS_SELECTOR,'a')
                for element in elements:
                    url = element.get_attribute('href')
                    if url.startswith("https://www.cochranelibrary.com/cdsr/doi/"):
                        cohrane.append(url)
                        i=i+1
        except:
            pass
        try:
            driver.quit()
        except:
            pass    
        del driver

    ####################################-EU Science Hub-###################################################
        print("Starting EU Science Hub Scrapper")
        driver = webdriver.Firefox(options=options)
        url_long = ""
        esh = []
        i = 0
        try:
            driver.get("https://ec.europa.eu/search/?queryText="+keyword)
            time.sleep(5)
            results = driver.find_elements(By.CSS_SELECTOR,'.ecl-u-mv-m')
            for result in results:
                if i>=7:
                    break
                elements = result.find_elements(By.CSS_SELECTOR,'a')
                for element in elements:
                    if i>=3:
                        break
                    url = element.get_attribute('href')
                    if url in url_long:
                        continue
                    if "research" in url:
                        esh.append(url)
                        url_long+=url
                        i = i+1
        except:
            print("EU Science Hub failed")
        try:
            driver.quit()
            del url_long, driver
        except:
            pass
    ##############################-Returning Results-#########################################
        result_list = ieee + pubmed + acm + who + arxiv + nlm + cohrane + embl + esh
        del ieee , pubmed , acm , who , arxiv , nlm , cohrane , embl , esh
        return result_list
