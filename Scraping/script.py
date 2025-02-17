import requests 
from bs4 import BeautifulSoup
import pandas as pd

'''
Done - 
1. Lower Parel
2. Worli
3. Tardeo 
4. cumbala hill
5. Colaba
6. Churchgate
7. Bandra
8. kalyan 
9. Dombivli
10. Prabhadevi
11. dadar
12. Mahim
13. Matunga
14. Khar
15. Santacruz
16. Andheri 
17. Ville Parle
18. Juhu
19. Goregaon
20. Malad
21. Kandivali 
22. Borivali
23. Vasai
24. Virar
25. Kurla
26. Ghatkopar
27. Mulund
28. Byculla
29. Sion
30. Bhandup
31. Vikhroli
32. Nahur
33. Chembur
'''

links = [
    'https://www.99acres.com/property-in-bhandup-central-mumbai-suburbs-ffid',
    'https://www.99acres.com/property-in-vikhroli-central-mumbai-suburbs-ffid',
    'https://www.99acres.com/property-in-nahur-central-mumbai-suburbs-ffid',
    'https://www.99acres.com/property-in-chembur-central-mumbai-ffid'
]

def first_page(lin):
    payload = {'api_key':'API_KEY', 'url': f'{lin}'}
    r = requests.get('https://api.scraperapi.com', params=payload)
    #print(r.text)
    soup = BeautifulSoup(r.content, 'html.parser')
    count = 0
    all_links = []
    for link in soup.find_all('a'):
        if 'spid' in str(link.get('href')):
            route = str(link.get('href'))
            links = {
                'id': route[-9:],
                'link': route
            }
            all_links.append(links)
            count += 1
    df = pd.DataFrame(all_links)
    df.to_csv('output.csv', index=False, header=False, mode='a')
    print(count)
    pages_div = soup.find('div', class_='caption_strong_large')
    if pages_div:
        text = pages_div.get_text(strip=True)
        if "of" in text:
            total_pages = text.split("of")[-1].strip()
            return int(total_pages)

def scraping(i, lin):
    payload = {'api_key':'API_KEY', 'url': f'{lin}-page-{i}'}
    r = requests.get('https://api.scraperapi.com', params=payload)
    #print(r.text)
    soup = BeautifulSoup(r.content, 'html.parser')
    count = 0
    all_links = []
    for link in soup.find_all('a'):
        if 'spid' in str(link.get('href')):
            route = str(link.get('href'))
            links = {
                'id': route[-9:],
                'link': route
            }
            all_links.append(links)
            count += 1
    df = pd.DataFrame(all_links)
    df.to_csv('output.csv', index=False, header=False, mode='a')
    print(count)

total_tokens = 10000
for lin in links:
    total_pages = first_page(lin)
    if total_pages > 100: 
        total_pages = 100
    if total_pages > total_tokens:
        total_pages = total_tokens
    for i in range(2, total_pages):
        scraping(i, lin)
    total_tokens -= total_pages
    print("Area completed!")

print("---------------------- Done :-) ----------------------")