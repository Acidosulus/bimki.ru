from my_library import *
from bimki_driver import *
import colorama
from colorama import Fore, Back, Style
from urllib.parse import quote
from bs4 import BeautifulSoup as BS
from click import echo, style

def poiskpers(url):
	geourl = '{0}'.format(quote(url))
	return geourl

class Good:
	def __init__(self, ol:WD, pc_good_link, pc_price:str):
		pc_good_link = pc_good_link.replace(r'amp;', '')
		self.pictures = []
		self.sizes = []
		self.prices = []
		self.color = ''
		self.article = ''
		self.name = ''
		self.description= ''
		self.price = ''
		self.brand = ''
		echo(style('Товар: ', fg='bright_yellow') + style(pc_good_link, fg='bright_white') + style('  Прайс:', fg='bright_cyan') + style(pc_price, fg='bright_green'))
		ol.Get_HTML(pc_good_link)
		soup = BS(ol.page_source, features='html5lib')
		self.name = soup.find('h1').text.strip()

		prices = soup.find_all('div',{'class':'ty-product-prices opt-list-bottom-line'})
		self.price = prices[1].find('span',{'class':'ty-price-num'}).text.strip()

		pictures = soup.find('div',{'class':'ty-product-img cm-preview-wrapper'}).find_all('img')
		for picture in pictures:
			if '_mini' not in str(picture['id']):
				append_if_not_exists(picture['src'], self.pictures)

		try:
			self.description = soup.find('div',{'id':'content_description'}).text.strip()
		except: pass
		try:
			self.description = self.description + ' ' +soup.find('div',{'id':'content_features'}).text.strip()
		except: pass
		self.description = reduce(self.description).replace(chr(10),' ').strip()

		table = soup.find('table',{'class':'hidden'}).find_all('tr')
		for element in table:
			sections = element.find_all('td')
			lc_color = (reduce(prepare_str(sections[0].text)).strip()+'|').replace(',|','').replace('|','')
			lc_remain = reduce(prepare_str(sections[1].text)).strip()
			if int(lc_remain)!=0:
				append_if_not_exists(lc_color + '  Остаток: ' + lc_remain +' шт.', self.sizes)
			


		return

		options = soup.find_all('div',{'class':'ty-product-variant-image color-box-variants'})
		self.color = options[0].text.strip()
		if len(options)>=2:
			sizes = options[1].find_all('label')
			for size in sizes:
				append_if_not_exists(size.text.strip(), self.sizes)
