import pandas as pd
import numpy as np
from bs4 import BeautifulSoup
import requests

def Amazon(url):  
    headers = {'dnt': '1',
        'upgrade-insecure-requests': '1',
        'user-agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_4) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/83.0.4103.62 Safari/537.36',
        'accept': 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9',
        'sec-fetch-site': 'same-origin',
        'sec-fetch-mode': 'navigate',
        'sec-fetch-user': '?1',
        'sec-fetch-dest': 'document',
        'referer': 'https://www.amazon.com/',
        'accept-language': 'en-GB,en-US;q=0.9,en;q=0.8'}

    r = requests.get(url, headers=headers)#, proxies=proxies)
    content = r.content
    soup = BeautifulSoup(content)
    for data in soup(['style', 'script']):
        data.decompose()
    all1 = []
    productdetailkey =[]
    productdetailvalue =[]
    productdetail ={}
    productOverview ={}
    productOverviewkey =[]
    productOverviewvalue =[]
    productTitle = soup.find('span', attrs={'id':'productTitle'})
    productOverviewfull = soup.find('div', attrs={'id':'productOverview_feature_div'})
    shortdesc = soup.find('div', attrs={'id':'featurebullets_feature_div'})
    productDescriptionfull =soup.find('div', attrs={'id':'productDescription_feature_div'})
    try:
        productOverview1for = productOverviewfull.find_all("td",attrs={'class':'a-span3'})
        productOverview2for = productOverviewfull.find_all("td",attrs={'class':'a-span9'})
        for productOverviewfine1 in productOverview1for:
                productOverviewkey.append(productOverviewfine1.text.replace('\n',''))
        i=0
        for productOverviewfine2 in productOverview2for:
                productOverviewfine2=productOverviewfine2.text.replace('\n\n\n',' ')
                productOverviewvalue.append(productOverviewfine2.replace('\n',''))
                productOverview[productOverviewkey[i]]=productOverviewvalue[i]
                i=i+1
    except AttributeError:
            productOverview = {}
    try:
        productdetailull = soup.find('div', attrs={'id':'detailBullets_feature_div'})
        productdetail1for = productdetailull.find_all("span",attrs={'class':'a-text-bold'})
        productdetail2for = productdetailull.find_all("span",attrs={'class':''})
        for productdetailfine1 in productdetail1for:
                productdetailfine1=(productdetailfine1.text.replace(':',''))
                productdetailkey.append(productdetailfine1.replace('\n',''))
        i=0
        # print(productdetailkey)
        for productdetailfine2 in productdetail2for:
                productdetailfine2=productdetailfine2.text.replace('\n\\n\n',' ')
                productdetailvalue.append(productdetailfine2.replace('\n',''))
                productdetail.update({productdetailkey[i]:productdetailvalue[i]})
                # print(productdetailkey.get('Product Dimensions'))
                if productdetailkey[i] in 'Product Dimensions':
                        productdetail.pop("Product Dimensions")
                        productdetail['Package Dimensions']=productdetailvalue[i]
                if productdetailkey[i] in 'Weight':
                        productdetail.pop("Weight")
                        productdetail['Item Weight']=productdetailvalue[i]
                i=i+1
        # print(productdetail)
    except AttributeError:
            try:
                productdetailull = soup.find('div', attrs={'id':'productDetails_techSpec_section_1'})
                productdetail1for = productdetailull.find_all("th",attrs={'class':'a-color-secondary a-size-base prodDetSectionEntry'})
                productdetail2for = productdetailull.find_all("td",attrs={'class':'a-size-base prodDetAttrValue'})
                for productdetailfine1 in productdetail1for:
                        productdetailkey.append(productdetailfine1.text.replace('\n',''))
                i=0
                # print(productdetailkey)
                for productdetailfine2 in productdetail2for:
                        productdetailfine2=productdetailfine2.text.replace('\n\n\n',' ')
                        productdetailvalue.append(productdetailfine2.replace('\n',''))
                        productdetail.update({productdetailkey[i]:productdetailvalue[i]})
                        # print(productdetailkey['Product Dimensions'])
                        if productdetailkey[i] in 'Product Dimensions':
                                productdetail.pop('Product Dimensions')
                                productdetail['Package Dimensions']=productdetailvalue[i]
                        if productdetailkey[i] in 'Weight':
                                productdetail.pop("Weight")
                                productdetail['Item Weight']=productdetailvalue[i]
                        i=i+1
            except AttributeError:
                productdetail={}

    try:
        productDescription = productDescriptionfull.find('p', attrs={'id':''})
    except AttributeError:
        try:
            productDescription = soup.find('p', attrs={'class':'aplus-description aplus-container-3 aplus-p1'})
        except AttributeError:
            productDescription=''
        
    if productTitle is not None:
            productTitle=productTitle.text.replace('\n\n\n',' ')
            all1.append(productTitle.replace('\n',''))
    else:
            all1.append("") 
    if shortdesc is not None:
            shortdesc=shortdesc.text.replace('\n\n\n',' ')
            all1.append(shortdesc.replace('\n',''))
    else:
            all1.append("") 
    if productDescription is not None:
            productDescription=productDescription.text.replace('\n\n\n',' ')
            all1.append(productDescription.replace('\n',''))
    else:
            all1.append("")
    alls={}
    try:
        alls.update({"Brand":str(productOverview['Brand'])})
    except KeyError:
        alls.update({"Brand":''})
    alls.update({"shortdesc":all1[1]})
    try:
        alls.update({"Package Dimensions":str(productdetail.get('Package Dimensions'))})
    except KeyError:
        alls.update({"Package Dimensions":''})
    try:
        alls.update({'Manufacturer':str(productdetail.get('Manufacturer'))})
    except KeyError:
        alls.update({'Manufacturer':'Manufacturer: '+''})
    try:
        alls.update({'Item Weight':str(productdetail.get('Item Weight'))})
    except KeyError:
        alls.update({'Item Weight':''})
    alls.update({"productDescription":all1[2]})
    return alls
  
with open("urls.txt",'r') as urllist:
  data = []
  i=1
  for url in urllist.read().splitlines():
        data.append(Amazon(url))
        print("complete : "+str(i))
        i=i+1
print("Finesh...")
df = pd.DataFrame(data)
# print(df.iloc[3])
df.to_excel("Product Information.xlsx")
