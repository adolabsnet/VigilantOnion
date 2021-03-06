#!/usr/bin/python3
# -*- coding: utf-8 -*-

__author__ = 'Andrey Glauzer'
__license__ = "MIT"
__version__ = "1.0.1"
__maintainer__ = "Andrey Glauzer"
__status__ = "Development"

import requests
from bs4 import BeautifulSoup
import logging
import re
from Observer.modules.database import DataBase


class DiscoverDarkWebService:
	def __init__(
		self,
		host_db=None,
		user_db=None,
		password_db=None,
		database=None):

		self.host_db = host_db
		self.user_db = user_db
		self.password_db = password_db
		self.database_name = database
		self.database = DataBase(
			host_db = self.host_db,
			user_db = self.user_db,
			password_db = self.password_db,
			database = self.database_name,
		)

		self.source = 'Discover Dark Web Hidden Service'
		logging.basicConfig(level=logging.INFO)

		compare_sorce = self.database.compare_source(source=self.source)

		if compare_sorce:
			pass
		else:
			self.database.save_source(source=self.source)

		self.logger = logging.getLogger('Class:DiscoverDarkWebService')
		self.session = requests.session()

		self.proxies = {
			'http': 'socks5h://localhost:9050',

		}

	@property
	def start(self):
		self.database.replaces()
		self.discover_dark_web()

	def discover_dark_web(self):

		url = 'http://3bbaaaccczcbdddz.onion/discover'
		self.logger.info(' Conectando em {url}'.format(url=url))

		try:
			request = self.session.get(url, proxies=self.proxies, timeout=1000)
			soup = BeautifulSoup(request.content, features="lxml")

			list_urls = []
			for raw in soup.find('table', {'class': 'table'}).findAll('a'):

				list_urls.append(raw['href'].replace('/search?q=', ''))

		except(requests.exceptions.ConnectionError,
					requests.exceptions.ChunkedEncodingError,
					requests.exceptions.ReadTimeout,
					requests.exceptions.InvalidURL) as e:
			self.logger.error(' Não consegui conectar na url, porque ocorreu um erro.\n{e}'.format(e=e))
			pass

		self.logger.info(' Aplicando REGEX. Aguarde...')

		regex = re.compile("[A-Za-z0-9]{0,12}\.?[A-Za-z0-9]{12,50}\.onion")
		for lines in list_urls:
			rurls = lines \
				.replace('\xad', '') \
				.replace('\n', '') \
				.replace("http://", '') \
				.replace("https://", '') \
				.replace(r'\s', '') \
				.replace('\t', '')


			xurl = regex.match(rurls)

			if xurl is not None:
				self.database.saveonion(
					url=xurl.group(),
					source=self.source)
