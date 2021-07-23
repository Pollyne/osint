import requests
import json
import argparse
import time
from banner.banner import Banner

__author__ = 'Pollyne Zunino'
__version__ = '1.0'

class Colors:
    # Console colors
    G = '\033[32m'  # green
    P = '\033[35m'  # purple

class Darksearch(object):
    
    def __init__(self, query):
            self.query = query

    def crawl_api(self):
        clr = Colors()
        darksearch_url_response = requests.get('https://darksearch.io/api/search?query=', params=self.query)
        data_json = darksearch_url_response.json()
        json_data = json.dumps(data_json)
        try:
            if json.loads(json_data)['total'] >= 1:
                for key in range(len(json.loads(json_data)['data'])):
                    site_title = json.loads(json_data)['data'][key]['title']
                    site_onion_link = json.loads(json_data)['data'][key]['link']
                    print(clr.G + "Site: "+site_title+clr.P+"\nOnion Link: "+site_onion_link+"\n")
        except IndexError:
            print("[-] No results found for query:"+self.query+"\n")

def darksearch_main():
    bn = Banner()
    bn.LoadBanner()
    time.sleep(1.5)
    parser = argparse.ArgumentParser(prog='darksearch.py')
    parser.add_argument("-v", "--version", action="store_true")
    parser.add_argument("-q", "--query", type=str)
    parser.add_argument("-p", "--page", type=str)
    args = parser.parse_args()

    if args.version:
        print("Darksearch Version: "+__version__+" \n")

    elif args.query:
        if args.page: 
            query = {
                    'query': args.query,
                    'page': args.page
                    }
            print("Searching For: "+args.query+" \n page: "+args.page+"...\n")
            Darksearch(query).crawl_api()
        else:
            query = {
                'query': args.query,
                'page': 1
                }           
            print("Searching For:"+args.query+" on page: 1...\n")
            Darksearch(query).crawl_api()         

if __name__ == "__main__":
    darksearch_main()