from selenium import webdriver
import time
import os

dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'chromedriver.exe')
driver=webdriver.Chrome(path)

def parser_wordlisteng(url):
	driver.get(url)
	time.sleep(3)
	words = driver.find_elements_by_class_name('word-e') 
	for word in words:
		print(word.get_attribute("innerText"))

def parser_wordlistspa(url):
	driver.get(url)
	time.sleep(3)
	words = driver.find_elements_by_class_name('word-t') 
	for word in words:
		print(word.get_attribute("innerText"))


print("1. English")
print("2. Spanish")
lang = input("input: ")

if int(lang) == 1:
	url = input("url: ")
	parser_wordlisteng(url)
elif int(lang) ==2:
	url = input("url: ")
	parser_wordlistspa(url)