
from playwright.sync_api import sync_playwright 

def myfunc(resp):
	print(resp)
	
 
url = "https://economictimes.indiatimes.com/finolex-cables-ltd/stocks/companyid-13759.cms" 
 
with sync_playwright() as p: 
	browser = p.chromium.launch() 
	page = browser.new_page() 
 
	page.on("response", lambda response: myfunc)
	 
    #  print("<<", response.status, response.url)) if ('json.bselivefeeds.indiatimes.com' in response.url) else None
	    
	
	page.goto(url, wait_until="networkidle", timeout=90000) 
 
	# print(page.content()) 
 
	page.context.close() 
	browser.close()