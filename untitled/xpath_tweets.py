from lxml import html
import os

os.chdir('/Users/jiayuan/Documents/data/twitter_crawler/data')
douban = html.parse('http://163.com')

headers = douban.xpath('//h2|//h3')
lists = douban.xpath('//ul')

f = open('xpath_tweets.txt','w+')
for header,list in zip(headers,lists):
	#print header.text_content()
	for  li in list.getchildren():
		if len(li.xpath('a')):
			f.write(li.xpath('a')[0].text_content().encode('utf-8')+'\n')
		if len(li.xpath('a/span/em')):
			f.write(li.xpath('a/span/em')[0].text.encode('utf-8')+'\n')
f.close()
	
	
