'''
a) collect ID, planet name, abbr of planet name, url for detail,type
b) resource for planet, resouce icon

'''

import urllib.request as req
from bs4 import BeautifulSoup
import pandas as pd
import time
import random
import os

def open_web(url):
	headers = {
		'User-Agent': 'Mozilla/5.0 (Linux; Android 6.0; Nexus 5 Build/MRA58N) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/67.0.3396.99 Mobile Safari/537.36'}
	html_req = req.Request(url, headers=headers)
	page = req.urlopen(html_req)
	html = page.read()
	return html

def main_list(url):
	html = open_web(url)
	df = pd.DataFrame()
	web = BeautifulSoup(html, 'html.parser')
	planet_list_source = web.find('div', attrs={'class': 'planets-list'})
	nodes = planet_list_source.find_all('a', attrs={'class': 'planets-item'})
	for node in nodes:
		# node = nodes[0]
		link_ID = node.find('span', attrs={'class': ['code']}).string
		link_name = node.find('div', attrs={'class': 'name'}).string
		link_suffix = node.get('href')
		link_abbr = link_suffix.split('/')[-1]
		link_url = 'http://walkrgame.com/en' + link_suffix
		link_type = node.get('data-category')
		df = df.append({'Planet_ID': link_ID,
						'Planet_name': link_name,
						'Planet_abbr': link_abbr,
						'Planet_url': link_url,
						'Planet_type': link_type}
						,ignore_index=True)
	return(df)

def get_resource(url):
	time.sleep(random.uniform(1,15))
	#url = planet_list['Planet_url'][0]
	detail_html = open_web(url)
	detail_web = BeautifulSoup(detail_html, 'html.parser')
	planet_name = detail_web.select('body > div.section.section--first > div.dicshow-planet > div.dicshow-planet-info > div.name')[0].string
	details = detail_web.find('div',attrs={'class':'dicshow-more'})
	resource_text = details.select('ul > li:nth-child(2) > div.details > div.value')[0].string
	icon_url = 'http://walkrgame.com/'+ details.select('ul > li:nth-child(2) > div.icon')[0].find('img').get('src')
	pic_file = open_web(icon_url)
	if os.path.exists(save_loc + "/" +planet_name+'.png')==False:
		with open(save_loc + "/" +planet_name+'.png',"wb") as file:
			file.write(pic_file)
	return resource_text

url = 'http://walkrgame.com/en/planets'
save_loc = "/Users/nanzou/Documents/GitHub/walkr_collect/prework/resouce_icon/"

planet_list = main_list(url)
planet_list['Planet_resource']=''

planet_list.loc[:,'Planet_resource'] = planet_list.loc[:,'Planet_url'].apply(get_resource)
planet_list.to_excel('/Users/nanzou/Documents/GitHub/walkr_collect/planet_list.xlsx')