from selenium 					import webdriver
from selenium.webdriver.common.keys 		import Keys
from selenium.webdriver.common.by		import By
from selenium.webdriver.support.ui 		import Select
from selenium.common.exceptions 		import NoSuchElementException
from selenium.webdriver.chrome.options 		import Options
from selenium.webdriver.common.action_chains 	import ActionChains
from selenium.common.exceptions 		import InvalidSessionIdException
from bs4 					import BeautifulSoup

import time
import re
import requests








def check_sign_up(Login, Password):

	# ошибки
	Error 			= ''

	# значения по умолчанию
	steam_id 		= ''
	img_account = ''
	nickname 		= ''


	driver = webdriver.Chrome("chromedriver/chromedriver.exe")
	driver.get('https://steamcommunity.com/login/home/?goto=')

	time.sleep(2)
	
	# получение полей логин и пароля
	login 					= driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input')
	password				= driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input')

	login.send_keys(Login)
	password.send_keys(Password)
	
	# кнопка войти
	button_sign_in	= driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button')
	button_sign_in.click()

	time.sleep(3)

	# проверка есть ли на форме ошибка
	if check_exists_by_xpath(driver, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[5]'):

		driver.quit()

		return False, steam_id, img_account, nickname
	

	# если нет ошибки в заполнении данных
	else:	

		sign_in = True
		
		# если перешло в подтверждение через Steam Guard
		if check_exists_by_xpath(driver, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/div[2]'):

			sign_in = False
			time.sleep(2)

			url 		= 'https://steamcommunity.com/login/home/?goto='

			# проверяет остается ли на странице входа
			while url == 'https://steamcommunity.com/login/home/?goto=':

				time.sleep(2)

				url = driver.current_url

				if check_exists_by_xpath(driver, "/html/body/div[1]/div[7]/div[6]/div[3]/div[1]/div/div/div/div/div/div[2]"):
					if driver.find_element(By.XPATH("/html/body/div[1]/div[7]/div[6]/div[3]/div[1]/div/div/div/div/div/div[2]")).getText() == 'Истёк срок действия запроса на вход в аккаунт':

						Error = 'Steam Guard not confirmed'

						break

	# если ошибок нет, то вход выполнен
	if Error == '':
		driver.get('https://store.steampowered.com/account/')

		id_web 			= driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[3]/div/div[2]').text 		
		steam_id 		= re.findall(r'\b\d+\b', id_web)
		img_account = driver.find_element(By.XPATH, '//*[@id="global_actions"]/a/img').get_attribute('src')
		nickname		= driver.find_element(By.XPATH, '//*[@id="account_pulldown"]').text

		driver.close()

		return True, steam_id[0], img_account, nickname

	else:

		driver.close()

		return False, steam_id, img_account, nickname



def user_steam(Login, Password, stick_1, stick_2, stick_3, stick_4, FN, MW, FT, WW, BS, select_weapon, select_type, min_balance, max_balance, balance_total):

	
	Error 		= ''
	check 		= True
	buy_price = 0
	f 				= open('result.txt', 'w')

	driver 		= webdriver.Firefox('geckodriver.exe')
	action 		= ActionChains(driver)

	balance_remainder = balance_total

	driver.get('https://steamcommunity.com/login/home/?goto=')

	

	time.sleep(2)
	# получение полей логин и пароля
	login 		= driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[1]/input')
	password	= driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[2]/input')

	login.clear()
	password.clear()

	login.send_keys(Login)
	password.send_keys(Password)
	
	# кнопка войти
	button_sign_in = driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[4]/button')
	button_sign_in.click()

	time.sleep(2)

	# проверка есть ли на форме ошибка
	if check_exists_by_xpath(driver, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/form/div[5]'):

		Error = 'Error data'

	
	# если нет ошибки в заполнении данных
	else:	
		sign_in = True
		# если перешло в подтверждение через Steam Guard
		if check_exists_by_xpath(driver, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div[2]/div/div[2]'):
			sign_in = False

			time.sleep(2)

			url = 'https://steamcommunity.com/login/home/?goto='

			# проверяет остается ли на странице входа
			while url == 'https://steamcommunity.com/login/home/?goto=':

				time.sleep(2)

				url = driver.current_url

				if check_exists_by_xpath(driver, "/html/body/div[1]/div[7]/div[6]/div[3]/div[1]/div/div/div/div/div/div[2]"):
					if driver.find_element(By.XPATH("/html/body/div[1]/div[7]/div[6]/div[3]/div[1]/div/div/div/div/div/div[2]")).getText() == 'Истёк срок действия запроса на вход в аккаунт':
						Error = 'Steam Guard not confirmed'
						# return 'Steam Guard not confirmed'
						break
			
			# если ошибок нет, то вход выполнен
			if Error == '':
				sign_in = True

			time.sleep(2)

		print(sign_in)
		# если вход выполнен
		if sign_in == True:
			# баланс пользователя
			balance = get_balance(driver)
			# balance = balance
			time.sleep(1)

			# если у пользователя есть баланс и он не равен 0
			if (int(balance) > 0) or check == True:

				# переходим на торговую площадку
				driver.get('https://steamcommunity.com/market/')

				time.sleep(2)

				# если есть ограничение на торговлю через Steam
				if check_exists_by_xpath(driver, '//*[@id="market_warning_header"]') and check == False:
					# получит ошибку Steam из-за которого невозможно торговать
					Error = 'Market warning'
					print(Error)

				else:
					# переход на игру Counter Strike
					driver.get('https://steamcommunity.com/market/search?appid=730')

					time.sleep(2)
					# заполнение формы для поиска оружия и покупки его (дополнительные настройки поиска)
					#  нажатие на кнопку дополнительные настройки поиска
					driver.find_element(By.XPATH, '//*[@id="findItemsSearchBox"]').click()

					# искать в описаниях, иначе не пройдет поиск по стикерам
					driver.find_element(By.XPATH, '//*[@id="market_search_advanced_show"]/div').click()
					driver.find_element(By.XPATH, '//*[@id="market_advanced_searchdescriptions_checkbox"]').click()

					# заполнение форма "ПОИСК"
					search = driver.find_element(By.XPATH, '//*[@id="advancedSearchBox"]')

					time.sleep(2)

					if stick_1 != 'Empty' and stick_2 == 'Empty' and stick_3 == 'Empty' and stick_4 == 'Empty':
						search.send_keys('"' + stick_1 + '"')
					if stick_1 != 'Empty' and stick_2 != 'Empty' and stick_3 == 'Empty' and stick_4 == 'Empty':
						search.send_keys('"' + stick_1 + ', ' + stick_2 + '"')
					if stick_1 != 'Empty' and stick_2 != 'Empty' and stick_3 != 'Empty' and stick_4 == 'Empty':
						search.send_keys('"' + stick_1 + ', ' + stick_2 + ', ' + stick_3 + '"')
					if stick_1 != 'Empty' and stick_2 != 'Empty' and stick_3 != 'Empty' and stick_4 != 'Empty':
						search.send_keys('"' + stick_1 + ', ' + stick_2 + ', ' + stick_3 + ', ' + stick_4 + '"')

					# выбор оружия
					if select_weapon != 'Any weapon':
						sel_weapon = Select(driver.find_element(By.XPATH, '//*[@id="market_advancedsearch_filters"]/div[7]/select'))
						sel_weapon.select_by_visible_text(select_weapon)


					if FN == True :			
						driver.find_element(By.XPATH, '//*[@id="tag_730_Exterior_WearCategory0"]').click()
					if MW == True :
						driver.find_element(By.XPATH, '//*[@id="tag_730_Exterior_WearCategory1"]').click()
					if FT == True :
						driver.find_element(By.XPATH, '//*[@id="tag_730_Exterior_WearCategory2"]').click()
					if WW == True :
						driver.find_element(By.XPATH, '//*[@id="tag_730_Exterior_WearCategory3"]').click()
					if BS == True :
						driver.find_element(By.XPATH, '//*[@id="tag_730_Exterior_WearCategory4"]').click()
					
					time.sleep(1)
					# выбрать категорию оружия
					if select_type != 'Any type':
						match select_type:
							case "StatTrack":
								driver.find_element(By.XPATH, '//*[@id="tag_730_Quality_strange"]').click()
							
							case "Souvenir":
								driver.find_element(By.XPATH, '//*[@id="tag_730_Quality_tournament"]').click()


					# кнопка поиск
					driver.find_element(By.XPATH, '//*[@id="market_advancedsearch_dialog"]/div[2]/div').click()

					time.sleep(2)


					if check_exists_by_xpath(driver, '//*[@id="searchResultsRows"]/div/div[1]/div[1]'):

						# для сортировки по самой низкой цене
						driver.find_element(By.XPATH, '//*[@id="searchResultsRows"]/div/div[1]/div[1]').click()

						time.sleep(2)

						print(get_currency())
						# валюта
						currency 			= float(get_currency())

						# количество страниц с оружиями

						page_count = int(driver.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[4]/div[2]/div[2]/div/div[2]/div[1]/span[2]/span[7]').text) 

						for x in range(page_count):

							if check_exists_by_class_name(driver, 'market_listing_row_link'):
								price_weapon 	= driver.find_elements(By.CLASS_NAME, 'market_listing_row_link')
							else:
								action.send_keys(Keys.F5).perform()
								time.sleep(3)
								price_weapon 	= driver.find_elements(By.CLASS_NAME, 'market_listing_row_link')
							# для возвращения назад
							url 					= driver.current_url
							# количество элементов на странице
							# невозможно получить все т.к сессия потребует новые значения
							for i in range(len(price_weapon)):
								
								balance = get_balance(driver)

								if check_exists_by_css_selector(driver, '#result_' + str(i) + ' > div:nth-child(2) > div:nth-child(2) > span:nth-child(1) > span:nth-child(2)'):
									element = driver.find_element(By.CSS_SELECTOR, '#result_' + str(i) + ' > div:nth-child(2) > div:nth-child(2) > span:nth-child(1) > span:nth-child(2)')
								else:
									action.send_keys(Keys.F5).perform()
									time.sleep(3)
									element = driver.find_element(By.CSS_SELECTOR, '#result_' + str(i) + ' > div:nth-child(2) > div:nth-child(2) > span:nth-child(1) > span:nth-child(2)')

								# мы не должны покупать наклейки
								if check_exists_by_class_name(driver, 'market_listing_item_name'):
									name 		= driver.find_elements(By.CLASS_NAME, 'market_listing_item_name')[i]
								else:
									action.send_keys(Keys.F5).perform()
									time.sleep(3)
									name 		= driver.find_elements(By.CLASS_NAME, 'market_listing_item_name')[i]

								name_weapon = name.text
								
								if name.text.find('Наклейка') == -1:

									element_price = element.text
									price_weapon 	= re.findall(r'\b\d+\b', element_price)
									price_weapon 	= float(price_weapon[0]) + ( float(price_weapon[1]) / 100)

									# получаем валюту доллар и умножаем получаемую сумму со страницы, чтобы получить значение в рублях
									price_weapon *= currency
									price_weapon	= round(price_weapon, 2)

									element.click()

									# баланс купленного оружия
									buy_price += round(price_weapon,2)
							
									if buy_price >= balance_total:
										buy_price -= round(price_weapon,2)
										Error = 'Balance is over. Last weapon = ' + str(round(price_weapon,2))
										break
									else:
										balance_remainder -= round(price_weapon,2)


								# добавляем элемент который удовлетворяет по условиям цены
									if price_weapon < max_balance and price_weapon > min_balance:
										if balance > 0:
											if balance >= price_weapon:
												f.write(str(name_weapon) + '| price weapon = ' + str(price_weapon) + '\n')
												driver.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[4]/div[1]/div[4]/div[1]/div[3]/div[4]/div[2]/div[2]/div[2]/div[1]/div/a').click()	# купить
												driver.find_element(By.XPATH, '/html/body/div[39]/div[3]/div/div[7]/div/div/div[2]/div[2]/input').click()																			# принять условие
												driver.find_element(By.XPATH, '/html/body/div[39]/div[3]/div/div[7]/div/div/div[2]/a[1]').click()																							# купить


												time.sleep(3)
												driver.get(url)
												time.sleep(5)

											else:
												Error = 'Balance < price weapon'
												break

										else:
											Error = 'Balance ~ 0'
											break

									# if price_weapon > max_balance:
									# 	# баланс который был потрачен на покупку оружия
									# 	Error = 'Weapon > max. Last weapon = ' + str(round(price_weapon,2)) + '| funds spent = ' + str(balance_total)
									# 	break

							if Error != '':
								break

							if check_exists_by_xpath(driver, '/html/body/div[1]/div[7]/div[2]/div/div[2]/div/h3'):
								if driver.find_element(By.XPATH, '/html/body/div[1]/div[7]/div[2]/div/div[2]/div/h3'). text == 'Вы делали слишком много запросов. Пожалуйста, подождите и повторите запрос позже.':
										action.send_keys(Keys.F5).perform()
										time.sleep(3)

							if driver.current_url == url:
								driver.execute_script("window.scrollTo(0, 600)")
							else:
								driver.get(url)
								driver.execute_script("window.scrollTo(0, 600)")

							time.sleep(2)
							if check_exists_by_xpath(driver, '//*[@id="searchResults_btn_next"]'):
								driver.find_element(By.XPATH, '//*[@id="searchResults_btn_next"]').click()
							else:
								action.send_keys(Keys.F5).perform()
								time.sleep(3)
								driver.find_element(By.XPATH, '//*[@id="searchResults_btn_next"]').click()

							time.sleep(2)


										
			else:
				if sign_in == False:
					Error = 'Sign in Error'
					# return 'Sign in Error'
				if balance == 0:
					Error = 'Not balance'
					# return 'Not balance'
				else:
					if balance < 1:
						Error = 'Balance < 1'
						# return 'Balance < 1'

	driver.close()
	
	f.write(Error + '\n')
	f.write(str(buy_price))
	f.close()

	return ""

# для проверки прошла ли переадресация при подтверждении
def check_url(driver):
	time.sleep(4)
	# если не произошло переадресации вернет False
	if driver.current_url == 'https://steamcommunity.com/login/home/?goto=':
		# если появился элемент повторить нажмет "ПОВТОРИТЬ"
		if check_exists_by_xpath(driver, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div/div/div[3]/button'):
			driver.find_element(By.XPATH, '//*[@id="responsive_page_template_content"]/div[1]/div[1]/div/div/div/div/div/div[3]/button').click()
			return True
		
		return False
	else:
		return True
	
def get_balance(driver):
	# получаем баланс аккаунта
	if check_exists_by_xpath(driver, '//*[@id="header_wallet_balance"]'):
		text_balance 	= driver.find_element(By.XPATH, '//*[@id="header_wallet_balance"]').text
		if text_balance.find('usd') != -1:
			balance 	= re.findall(r'\b\d+\b', text_balance)
			currency 	= float(get_currency())
			balance 	= balance * currency

		if text_balance.find('руб') != -1:
			balance 	= re.findall(r'\b\d+\b', text_balance)
		print(balance)
		return balance

	else:
		return 0

def check_exists_by_xpath(driver, xpath):
	try:
			driver.find_element(By.XPATH, xpath)
	except NoSuchElementException:
			return False
	
	return True

def check_exists_by_class_name(driver, class_name):
	try:
			driver.find_element(By.CLASS_NAME, class_name)
	except NoSuchElementException:
			return False
	
	return True

def check_exists_by_css_selector(driver, css_selector):
	try:
			driver.find_element(By.CSS_SELECTOR, css_selector)
	except NoSuchElementException:
			return False
	
	return True



def get_currency():
	usd = 'https://www.google.com/search?sxsrf=ALeKk01NWm6viYijAo3HXYOEQUyDEDtFEw%3A1584716087546&source=hp&ei=N9l0XtDXHs716QTcuaXoAg&q=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+%D0%BA+%D1%80%D1%83%D0%B1%D0%BB%D1%8E&oq=%D0%B4%D0%BE%D0%BB%D0%BB%D0%B0%D1%80+&gs_l=psy-ab.3.0.35i39i70i258j0i131l4j0j0i131l4.3044.4178..5294...1.0..0.83.544.7......0....1..gws-wiz.......35i39.5QL6Ev1Kfk4'
	headers = {'User-Agent': 'Mozilla/5.0 (Macintosh; Intel Mac OS X 10_15_3) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/80.0.3987.149 Safari/537.36'}

	# Парсим всю страницу
	full_page = requests.get(usd, headers=headers)

	# Разбираем через BeautifulSoup
	soup = BeautifulSoup(full_page.content, 'html.parser')

	time.sleep(2)

	convert = soup.find("input", {"class": "lWzCpb a61j6"})['value']
	
	return convert


# срок работы проверки подтверждения 5 минут, вставить таймер чтобы пользователь 
# time.sleep(120)


# user_steam(Login, Password, SearchItem, weapon, type_weapon, design, max_price, min_price)
