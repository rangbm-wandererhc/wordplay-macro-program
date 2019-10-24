from selenium import webdriver
from selenium.webdriver.common.keys import Keys
import time
from selenium.common.exceptions import NoSuchElementException
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.common.by import By
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import TimeoutException
import random
import sys
English = []
Spanish = []


import os
dirname = os.path.dirname(__file__)
englishlistfile = os.path.join(dirname, 'list\\englishlist.txt')
spanishlistfile = os.path.join(dirname, 'list\\spanishlist.txt')


with open(englishlistfile, 'r',encoding="utf-8") as f: 
    for line in f:
        engelem = line.replace("\n","")
        English.append(engelem)

with open(spanishlistfile, 'r',encoding="utf-8") as f:
    for line in f:
        spaelem = line.replace("\n","")
        Spanish.append(spaelem)


def conver(test_str):			#conversion function
		    word = ''
		    skip1c = 0
		    skip2c = 0
		    skip3c = 0
		    skip4c = 0
		    for i in test_str:
		        if i == '[':
		            skip1c += 1
		        elif i == '(':
		            skip2c += 1
		        elif i == '<':
		        	skip3c += 1
		        elif i == ']' and skip1c > 0:
		            skip1c -= 1
		        elif i == ')'and skip2c > 0:
		            skip2c -= 1
		        elif i=='>' and skip3c>0:
		        	skip3c -= 1

		        elif skip1c == 0 and skip2c == 0 and skip3c ==0:
		            word += i
		    return word
def trimptag(test_str): #trimming p tag
	word = ''
	skip1c = 0
	print(len(test_str))
	length = len(test_str)
	i= 0 
	while i<len(test_str):
		if test_str[length-1] != 'p' and test_str[i] == '<' and test_str[i+1] =='p':
			i+=1
			skip1c+=1
		elif test_str[length-1] != 'p' and test_str[i] == 'p' and test_str[i+1] =='>':
			i+=1
			skip1c -=1
		elif skip1c == 0:
			word += test_str[i]
		i+=1
	return word


def trimspace(test_str): #trimming space
	word = ''
	for i in test_str:
		if i == ' ':
			return word
		else:
			word +=i
	return word


def nextbtnclicker(): #clicking next button
	time.sleep(0.2)
	# page = driver.find_element_by_css_selector('body').get_attribute('innerHTML')
	# if "CONTINUE" in page:
	# 	time.sleep(0.1)
	# 	driver.find_element_by_xpath("//*[text()[contains(., 'CONTINUE')]]").click()
	# page = driver.find_element_by_css_selector('body').get_attribute('innerHTML')
	# if "START" in page:
	# 	time.sleep(0.1)
	# 	driver.find_element_by_xpath("//*[text()[contains(., 'START')]]").click()
	lessonfinished = 1
	btn = driver.find_element_by_class_name('btn') 
	if 'next' in btn.get_attribute('id') : 
		nextbtn = driver.find_element_by_id('next')
		driver.execute_script("$(arguments[0]).click();", nextbtn)
		print("button clicked")
		btn = driver.find_element_by_class_name('btn') 
		if "Review Now" in btn.get_attribute("innerHTML"):
			print("lesson finished")
			return lessonfinished
		else:
			return 0

def mode1():
	time.sleep(3)
	courses = driver.find_elements_by_css_selector('h6') 
	courselist = []
	for course in courses:
		courselist.append(course.get_attribute("innerText"))

	print("choose your course number \n")
	a = 1
	for course_list in courselist:
		print(str(a)+". "+course_list)
		a+=1

	choice1 = input("input: ")
	choice1 = int(choice1)
	choice1 = choice1-1
	selected_course = courselist[choice1]
	print("you chose " + selected_course)
	driver.find_element_by_xpath("//*[text()[contains(., '"+selected_course+"')]]").click()

	time.sleep(2)

	url = driver.current_url

	lessons = driver.find_elements_by_css_selector('h4') 

	lessonlist = []

	for lesson in lessons:
		lessonlist.append(lesson.get_attribute("innerText"))


	print("choose your lesson numbers (seperate each lesson numbers by space) \n")
	a = 1
	for lesson_list in lessonlist:
		print(str(a)+". "+lesson_list)
		a+=1

	choices = []

	print("input: ")
	choices = [int(x) for x in input().split()]

	i = 0

	while i < len(choices):
		mode1_multiplelesson(choices[i],url,lessonlist,i)
		i+=1
	main()

def mode1_multiplelesson(choice1, url,lessonlist,i):
	driver.get(url)
	time.sleep(2)
	selected_lesson = lessonlist[choice1-1]
	print("you chose " + selected_lesson)
	lessons = driver.find_elements_by_xpath("//*[text()[contains(., '"+selected_lesson+"')]]")
	if len(lessons) > 1:
		dupprev = choice1 -1
		lessons[dupprev].click()
	else:
		lessons[0].click()
	# if len(lessons)>1:
	# 	lessons[i].click()
	# else:
	# 	lessons[0].click()
	time.sleep(2)

	progpercent = driver.find_element_by_class_name('CircularProgressbar-text')
	print(progpercent.get_attribute("innerHTML"))
	if "0" == progpercent.get_attribute("innerHTML"):
		print("0% mastery begin lesson")
		driver.find_element_by_xpath("//*[text()[contains(.,'PLAY')]]").click()
	elif "100" == progpercent.get_attribute("innerHTML"):
		print("\nyou have already done this lesson\n")
		return 
	else:
		driver.find_element_by_xpath("//*[text()[contains(.,'PLAY')]]").click()
		time.sleep(2)
		driver.find_element_by_xpath("//*[text()[contains(.,'Continue Play')]]").click()

	print('''

	-----------------------------

		wait 30 seconds...

	-----------------------------

		''')
	time.sleep(25)

	driver.implicitly_wait(60)
	key = ' '
	prevkey = 'sample'
	s1 = 0
	while True:
		time.sleep(2)
		escaper = nextbtnclicker()
		if escaper == 1:
			return
		time.sleep(1)
		print("loop began")
		lessonmode = driver.find_element_by_class_name('game-note')
		lesson_mode = lessonmode.get_attribute("innerText")
		print(lesson_mode+"\n")
		escaper = nextbtnclicker()
		if escaper == 1:
			return
		if "select correct match" in lesson_mode:
			timecontroller(0,1)
			shownword =	driver.find_element_by_class_name('prompt') 

			shown_word= shownword.get_attribute("innerHTML")
			shown_word = trimptag(shown_word)
			shown_word = conver(shown_word).replace("&nbsp;", "")
			shown_word = shown_word.replace(" ","")
			# shown_word = trimspace(shown_word)
			print("shown word " +shown_word)

			rand = random.randint(0,2)
			print("random number: "+str(rand))
			if rand == 0:
				s = 0
				while s < len(Spanish):
					if shown_word == (conver(Spanish[s]).replace(" ","")):
						key = conver(English[s])
						print("key:"+(conver(key)).replace(" ",""))
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					elif shown_word == (conver(English[s]).replace(" ","")):
						key = conver(Spanish[s])
						print("key:"+(conver(key)).replace(" ",""))
						if prevkey == key:
							print("wrong")
							s+=1
							continue
						break
					else:
						s+=1

			elif rand == 1:
				s1 = len(Spanish)-1
				while s1 >= 0:
					if shown_word == (conver(Spanish[s1]).replace(" ","")):
						key = conver(English[s1])
						print("key:"+(conver(key)).replace(" ",""))
						if prevkey == key:
							print("wrong")
							s1 -=1
							continue
						break
					elif shown_word == (conver(English[s1]).replace(" ","")):
						key = conver(Spanish[s1])
						print("key:"+(conver(key)).replace(" ",""))
						if prevkey == key:
							print("wrong")
							s1-=1
							continue
						break
					else:
						s1-=1
	
			elif rand == 2:
				s = random.randint(0,1970)
				while s < len(Spanish):
					if shown_word == (conver(Spanish[s]).replace(" ","")):
						key = conver(English[s])
						print("key:"+(conver(key)).replace(" ",""))
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					elif shown_word == (conver(English[s]).replace(" ","")):
						key = conver(Spanish[s])
						print("key:"+(conver(key)).replace(" ",""))
						if prevkey == key:
							print("wrong")
							s+=1
							continue
						break
					else:
						s+=1
			escaper = nextbtnclicker()
			if escaper == 1:
				return
			timecontroller(0,1)
			tile1 = driver.find_element_by_xpath('//*[@id="my-content"]/div[2]/div[2]/div[3]/div/div[1]')
			tile2 = driver.find_element_by_xpath('//*[@id="my-content"]/div[2]/div[2]/div[3]/div/div[2]')
			tile3 = driver.find_element_by_xpath('//*[@id="my-content"]/div[2]/div[2]/div[3]/div/div[3]')
			tile4 = driver.find_element_by_xpath('//*[@id="my-content"]/div[2]/div[2]/div[3]/div/div[4]')

			tile_1 = tile1.get_attribute("innerHTML")
			tile_1 = trimptag(tile_1).replace(" ","")
			tile_1 = conver(tile_1).replace("&nbsp;", "")

			tile_2 = tile2.get_attribute("innerHTML")
			tile_2 = trimptag(tile_2).replace(" ","")
			tile_2 = conver(tile_2).replace("&nbsp;", "")


			tile_3 = tile3.get_attribute("innerHTML")
			tile_3 = trimptag(tile_3).replace(" ","")
			tile_3 = conver(tile_3).replace("&nbsp;", "")

			tile_4 = tile4.get_attribute("innerHTML")
			tile_4 = trimptag(tile_4).replace(" ","")
			tile_4 = conver(tile_4).replace("&nbsp;", "")

			print("tile1:"+tile_1)
			print("tile2:"+tile_2)
			print("tile3:"+tile_3)
			print("tile4:"+tile_4)

			timecontroller(0,1)

			if (conver(key)).replace(" ","") in tile_1:
					tile1.click()
			elif (conver(key)).replace(" ","") in tile_2:
					tile2.click()
			elif (conver(key)).replace(" ","") in tile_3:
					tile3.click()
			elif (conver(key)).replace(" ","") in tile_4:
					tile4.click()
			else:
				print("tile not detected, skip")

			timecontroller(0,1)
			escaper = nextbtnclicker()
			if escaper == 1:
				return


				
			prevkey = key

			print("prevkey: " +prevkey)
			time.sleep(1)
			escaper = nextbtnclicker()
			if escaper == 1:
				return

		elif "tap letters to unscramble" in lesson_mode:
			escaper = nextbtnclicker()
			if escaper == 1:
				return
			timecontroller(0,1)
			escaper = nextbtnclicker()
			if escaper == 1:
				return
			shownword = driver.find_element_by_class_name('text-primary')
			shown_word = shownword.get_attribute("innerHTML")
			shown_word = trimptag(shown_word)
			shown_word = conver(shown_word).replace("&nbsp;", "")
			print("shown word:"+shown_word)
			
			rand = random.randint(0,2)
			print("random number: "+str(rand))
			if rand == 0:
				s1 = len(Spanish)-1
				while s1 >=0:
					if (conver(shown_word).replace(" ","")) == (conver(Spanish[s1]).replace(" ","")):
						key = English[s1].replace("\u0029\u0020","\u0029") # replacing "( " with "("
						key = conver(key)
						print("key:"+ key)
						timecontroller(0,1)

						for keyelem in key:
							print(keyelem)
							driver.find_element_by_id("blur-hack").send_keys(keyelem)
							time.sleep(0.2)
							escaper = nextbtnclicker()
							if escaper == 1:
								return
							errorbuttons = driver.find_elements_by_css_selector(".btn-primary")
						for errorbutton in errorbuttons:
							errordetect = errorbutton.get_attribute('class')
							if "btn-highlight" in errordetect:
								continue	
						if prevkey == key:
							print("wrong")
							s1 -=1
							continue					
						break
					elif (conver(shown_word).replace(" ","")) == (conver(English[s1]).replace(" ","")):
						key = Spanish[s1].replace("\u0029\u0020","\u0029") # replacing "( " with "("
						key = conver(key)
						print("key:"+key)	
						timecontroller(0,1)
						for keyelem in key:
							print(keyelem)
							escaper = nextbtnclicker()
							if escaper == 1:
								return
							driver.find_element_by_id("blur-hack").send_keys(keyelem)
							time.sleep(0.2)
							errorbuttons = driver.find_elements_by_css_selector(".btn-primary")
						for errorbutton in errorbuttons:
							errordetect = errorbutton.get_attribute('class')
							if "btn-highlight" in errordetect:
								continue	
						if prevkey == key:
							print("wrong")
							s1 -=1
							continue
						break
					else:
						s1=s1-1
				escaper = nextbtnclicker()
				if escaper == 1:
					return
			elif rand == 1:
				escaper = nextbtnclicker()
				if escaper == 1:
					return
				s = 0
				while s < len(Spanish):
					if (conver(shown_word).replace(" ","")) == (conver(Spanish[s]).replace(" ","")):
						key = English[s].replace("\u0029\u0020","\u0029") # replacing "( " with "("
						key = conver(key)
						timecontroller(0,1)
						print("key:"+key)
						for keyelem in key:
							print(keyelem)
							escaper = nextbtnclicker()
							if escaper == 1:
								return
							driver.find_element_by_id("blur-hack").send_keys(keyelem)
							time.sleep(0.2)
							errorbuttons = driver.find_elements_by_css_selector(".btn-primary")
						for errorbutton in errorbuttons:
							errordetect = errorbutton.get_attribute('class')
							if "btn-highlight" in errordetect:
								continue	
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					elif (conver(shown_word).replace(" ","")) == (conver(English[s]).replace(" ","")):
						key = Spanish[s].replace("\u0029\u0020","\u0029") # replacing "( " with "("
						key = conver(key)
						print("key:"+key)	
						timecontroller(0,1)
						for keyelem in key:
							print(keyelem)
							escaper = nextbtnclicker()
							if escaper == 1:
								return
							driver.find_element_by_id("blur-hack").send_keys(keyelem)
							time.sleep(0.2)
							errorbuttons = driver.find_elements_by_css_selector(".btn-primary")
						for errorbutton in errorbuttons:
							errordetect = errorbutton.get_attribute('class')
							if "btn-highlight" in errordetect:
								continue
						if prevkey == key:
							print("wrong")
							s +=1
							continue	
						break
					else:
						s=s+1
				escaper = nextbtnclicker()
				if escaper == 1:
					return		
			elif rand == 2:
				escaper = nextbtnclicker()
				if escaper == 1:
					return
				s = random.randint(0,1970)
				while s < len(Spanish):
					if (conver(shown_word).replace(" ","")) == (conver(Spanish[s]).replace(" ","")):
						key = English[s].replace("\u0029\u0020","\u0029") # replacing "( " with "("
						key = conver(key)
						timecontroller(0,1)
						print("key:"+key)
						for keyelem in key:
							print(keyelem)
							escaper = nextbtnclicker()
							if escaper == 1:
								return
							driver.find_element_by_id("blur-hack").send_keys(keyelem)
							time.sleep(0.2)
							errorbuttons = driver.find_elements_by_css_selector(".btn-primary")
						for errorbutton in errorbuttons:
							errordetect = errorbutton.get_attribute('class')
							if "btn-highlight" in errordetect:
								continue	
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					elif (conver(shown_word).replace(" ","")) == (conver(English[s]).replace(" ","")):
						key = Spanish[s].replace("\u0029\u0020","\u0029") # replacing "( " with "("
						key = conver(key)
						print("key:"+key)	
						timecontroller(0,1)
						for keyelem in key:
							print(keyelem)
							escaper = nextbtnclicker()
							if escaper == 1:
								return
							driver.find_element_by_id("blur-hack").send_keys(keyelem)
							time.sleep(0.2)
							errorbuttons = driver.find_elements_by_css_selector(".btn-primary")
						for errorbutton in errorbuttons:
							errordetect = errorbutton.get_attribute('class')
							if "btn-highlight" in errordetect:
								continue
						if prevkey == key:
							print("wrong")
							s +=1
							continue	
						break
					else:
						s=s+1
				escaper = nextbtnclicker()
				if escaper == 1:
					return			
				
			prevkey = key

		elif "CAPITALIZATION AND PUNCTUATION ARE IGNORED" in lesson_mode:
			escaper = nextbtnclicker()
			if escaper == 1:
				return		
			timecontroller(0,1)
			escaper = nextbtnclicker()
			if escaper == 1:
				return		
			shownword = driver.find_element_by_class_name('text-white')
			shown_word= shownword.get_attribute("innerHTML")
			shown_word = trimptag(shown_word)
			shown_word = conver(shown_word).replace("&nbsp;", "")
			print("shown word:"+shown_word)
			rand = random.randint(0,4)
			print("random number: "+str(rand))
			if rand == 0:
				s = 0
				while s < len(Spanish):
					if (conver(shown_word).replace(" ","")) == (conver(Spanish[s]).replace(" ","")):
						key = conver(English[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					elif (conver(shown_word).replace(" ","")) == (conver(English[s]).replace(" ","")):
						key = conver(Spanish[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					else:
						s=s+1
			elif rand == 1:
				s= int((len(Spanish))/2)
				while s < len(Spanish):
					if (conver(shown_word).replace(" ","")) == (conver(Spanish[s]).replace(" ","")):
						key = conver(English[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					elif (conver(shown_word).replace(" ","")) == (conver(English[s]).replace(" ","")):
						key = conver(Spanish[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					else:
						s=s+1

			elif rand == 2:
				s1 = len(Spanish)-1
				while s1 >=0:
					if (conver(shown_word).replace(" ","")) == (conver(Spanish[s1]).replace(" ","")):
						key = conver(English[s1])
						if prevkey == key:
							print("wrong")
							s1 -=1
							continue
						break
					elif (conver(shown_word).replace(" ","")) == (conver(English[s1]).replace(" ","")):
						key = conver(Spanish[s1])
						if prevkey == key:
							print("wrong")
							s1 -=1
							continue
						break
					else:
						s1=s1-1

			elif rand == 3:
				s= random.randint(0,1970)
				while s < len(Spanish):
					if (conver(shown_word).replace(" ","")) == (conver(Spanish[s]).replace(" ","")):
						key = conver(English[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					elif (conver(shown_word).replace(" ","")) == (conver(English[s]).replace(" ","")):
						key = conver(Spanish[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					else:
						s=s+1
			elif rand == 4:
				s= 1800
				while s < len(Spanish):
					if (conver(shown_word).replace(" ","")) == (conver(Spanish[s]).replace(" ","")):
						key = conver(English[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					elif (conver(shown_word).replace(" ","")) == (conver(English[s]).replace(" ","")):
						key = conver(Spanish[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					else:
						s=s+1

			if key == prevkey or key ==' ':
				print("not detected")
				s = 0
				while s < len(Spanish):
					if (conver(shown_word).replace(" ","")) == (conver(Spanish[s]).replace(" ","")):
						key = conver(English[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					elif (conver(shown_word).replace(" ","")) == (conver(English[s]).replace(" ","")):
						key = conver(Spanish[s])
						if prevkey == key:
							print("wrong")
							s +=1
							continue
						break
					else:
						s=s+1				

			print("key:"+key)
			timecontroller(0,1)
			escaper = nextbtnclicker()
			if escaper == 1:
				return		
			driver.find_element_by_id("type-input").send_keys(key)
			driver.find_element_by_css_selector('#done-btn').send_keys("\n")
			time.sleep(0.5)
			driver.find_element_by_xpath('//*[@id="type-input"]').send_keys(30 * Keys.BACKSPACE)  
			time.sleep(1.5)
			# element = driver.find_element_by_xpath('//*[@id="altModal"]')
			# hidden_box = element.get_attribute('class')

			# if hidden_box=="modal fade in":
			# 	driver.find_element_by_xpath('//*[@id="altModal"]/div/div/div[3]/button').click()
			prevkey = key
			escaper = nextbtnclicker()
			if escaper == 1:
				return

def continuebtnclicker():
	time.sleep(0.1)
	page = driver.find_element_by_css_selector('body').get_attribute('innerHTML')
	if "CONTINUE" in page:
		driver.find_element_by_xpath("//*[text()[contains(., 'CONTINUE')]]").click()
def mode2():
	print("choose your mode \n")
	print("1. Regular mode \n")
	print("2. Error mode \n")
	mode = input("input: ")
	mode = float(mode)
	if mode == 1:
		print("you chose regular mode")
		numofwords = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/h5')
		num_of_word= numofwords.get_attribute("textContent")
		numofwords2 = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[3]/h5')
		num_of_word2= numofwords2.get_attribute("textContent")
		fin_num_of_words = int(num_of_word) + int(num_of_word2)

		# gets on to the dashboard & clicks review now

		driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/a').click()

		print('\n\n\ntotal words: ')
		print(fin_num_of_words)
		print('\n')

		# ad

		print('''

		-----------------------------

			wait 30 seconds...

		-----------------------------

			''')

		driver.implicitly_wait(60)
		time.sleep(30)
		key=''

		i2 = 0 # num of words

		#retention

		while i2<fin_num_of_words:
			url = driver.current_url
			print(url)
			if url == "https://www.wordplay.com/account":
				break
			timecontroller(0,1)
			continuebtnclicker()

			shownword = driver.find_element_by_xpath('//*[@id="review-content"]/div[2]/div[2]/div[1]/div/h3')
			shown_word= shownword.get_attribute("textContent")

			i = 0 #words
			continuebtnclicker()
			while i < len(Spanish):

				if (conver(shown_word).replace(" ","")) == (conver(Spanish[i]).replace(" ","")):
					print("-")
					key = conver(English[i])
					timecontroller(0,2)
					continuebtnclicker()
					driver.find_element_by_xpath('//*[@id="type-input"]').send_keys(key)
					continuebtnclicker()
					driver.find_element_by_css_selector('#done-btn').send_keys("\n")
					time.sleep(0.5)
					continuebtnclicker()
					driver.find_element_by_xpath('//*[@id="type-input"]').send_keys(30 * Keys.BACKSPACE)        
					time.sleep(0.5)
					continuebtnclicker()
					element = driver.find_element_by_xpath('//*[@id="altModal"]')
					hidden_box = element.get_attribute('class')
					continuebtnclicker()
					element2 = driver.find_element_by_xpath('//*[@id="wrongEx"]')
					incorrect_mark = element2.get_attribute('style')
					continuebtnclicker()
					if hidden_box=="modal fade in":
						driver.find_element_by_xpath('//*[@id="altModal"]/div/div/div[3]/button').click()
						i = i+1
						continue
					elif "inline" in incorrect_mark:
						i = i+1
						continue
					else:
						break

				elif (conver(shown_word).replace(" ","")) == (conver(English[i]).replace(" ","")):
					print("-")
					key = conver(Spanish[i])
					continuebtnclicker()
					driver.find_element_by_xpath('//*[@id="type-input"]').send_keys(key)
					continuebtnclicker()
					driver.find_element_by_css_selector('#done-btn').send_keys("\n")
					time.sleep(1)
					continuebtnclicker()
					driver.find_element_by_xpath('//*[@id="type-input"]').send_keys(30 * Keys.BACKSPACE)        
					time.sleep(2)
					continuebtnclicker()
					element = driver.find_element_by_xpath('//*[@id="altModal"]')
					hidden_box = element.get_attribute('class')
					continuebtnclicker()
					element2 = driver.find_element_by_xpath('//*[@id="wrongEx"]')
					incorrect_mark = element2.get_attribute('style')
					continuebtnclicker()
					if hidden_box=="modal fade in":
						driver.find_element_by_xpath('//*[@id="altModal"]/div/div/div[3]/button').click()
						i = i+1
						continue
					elif "inline" in incorrect_mark:
						i = i+1
						continue
					else:
						break
				else:
					i=i+1
					
			i2 = i2+1
			print('\n')
			print(fin_num_of_words-i2)
			print('words left...\n')
		print("retention finished")
		main()
	elif mode == 2:
		print("you chose error mode")
		numofwords = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[2]/h5')
		num_of_word= numofwords.get_attribute("textContent")
		numofwords2 = driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[1]/div[2]/div/div[3]/h5')
		num_of_word2= numofwords2.get_attribute("textContent")
		fin_num_of_words = int(num_of_word) + int(num_of_word2)

		# gets on to the dashboard & clicks review now

		driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div[3]/div[2]/div[1]/div[2]/div[2]/a').click()

		print('\n\n\ntotal words: ')
		print(fin_num_of_words)
		print('\n')

		# ad

		print('''

		-----------------------------

			wait 30 seconds...

		-----------------------------

			''')

		driver.implicitly_wait(60)
		time.sleep(30)
		key=''

		i2 = 0 # num of words

		#retention

		while i2<fin_num_of_words:
			url = driver.current_url
			print(url)
			if url == "https://www.wordplay.com/account":
				break
			continuebtnclicker()
			page = driver.find_element_by_css_selector('body').get_attribute('innerHTML')

			timecontroller(0,1)
			shownword = driver.find_element_by_xpath('//*[@id="review-content"]/div[2]/div[2]/div[1]/div/h3')
			shown_word= shownword.get_attribute("textContent")

			i = 0 #words
			continuebtnclicker()
			while i < len(Spanish):

				if (conver(shown_word).replace(" ","")) == (conver(Spanish[i]).replace(" ","")):
					continuebtnclicker()
					key = conver(English[i])
					timecontroller(0,2)
					rand = random.randint(1,10)
					if rand == 10:
						key = "random"
						print("error mode activated")
					continuebtnclicker()
					driver.find_element_by_xpath('//*[@id="type-input"]').send_keys(key)
					continuebtnclicker()
					driver.find_element_by_css_selector('#done-btn').send_keys("\n")
					time.sleep(0.5)
					continuebtnclicker()
					driver.find_element_by_xpath('//*[@id="type-input"]').send_keys(30 * Keys.BACKSPACE)        
					time.sleep(0.5)
					continuebtnclicker()
					element = driver.find_element_by_xpath('//*[@id="altModal"]')
					hidden_box = element.get_attribute('class')
					continuebtnclicker()
					element2 = driver.find_element_by_xpath('//*[@id="wrongEx"]')
					incorrect_mark = element2.get_attribute('style')
					continuebtnclicker()
					if hidden_box=="modal fade in":
						driver.find_element_by_xpath('//*[@id="altModal"]/div/div/div[3]/button').click()
						i = i+1
						continue
					elif "inline" in incorrect_mark:
						i = i+1
						continue
					else:
						break

				elif (conver(shown_word).replace(" ","")) == (conver(English[i]).replace(" ","")):
					continuebtnclicker()
					key = conver(Spanish[i])
					timecontroller(0,2)
					rand = random.randint(1,10)
					if rand == 10:
						key = "random"
						print("error mode activated")
					continuebtnclicker()
					driver.find_element_by_xpath('//*[@id="type-input"]').send_keys(key)
					continuebtnclicker()

					driver.find_element_by_css_selector('#done-btn').send_keys("\n")
					time.sleep(1)
					continuebtnclicker()

					driver.find_element_by_xpath('//*[@id="type-input"]').send_keys(30 * Keys.BACKSPACE)        
					time.sleep(2)
					continuebtnclicker()

					element = driver.find_element_by_xpath('//*[@id="altModal"]')
					hidden_box = element.get_attribute('class')
					continuebtnclicker()

					element2 = driver.find_element_by_xpath('//*[@id="wrongEx"]')
					incorrect_mark = element2.get_attribute('style')
					continuebtnclicker()

					if hidden_box=="modal fade in":
						driver.find_element_by_xpath('//*[@id="altModal"]/div/div/div[3]/button').click()
						i = i+1
						continue
					elif "inline" in incorrect_mark:
						i = i+1
						continue
					else:
						break
				else:
					i=i+1
					
			i2 = i2+1
			print('\n')
			print(fin_num_of_words-i2)
			print('words left...\n')
		print("retention finished")
		main()		

def timecontroller(rand1, rand2):
	rand = random.randint(rand1,rand2)
	print("Random wait time:"+str(rand))
	time.sleep(rand)


def main():
	driver.get('https://wordplay.com/account')	

	print("choose your mode")
	print("1.Lesson")
	print("2.Retention")
	print("3.Close")
	mode = input("\ninput: ")
	mode = float(mode)

	if mode == 1:
		mode1()

	elif mode == 2: 
		mode2()
	elif mode == 3:
		print("program ended")
		print("contact: rangbm.wandererhc@gmail.com")
		sys.exit()


#program start
dirname = os.path.dirname(__file__)
path = os.path.join(dirname, 'chromedriver.exe')

print("""
_________________________________

Wordplay Macro Program 

_________________________________

	""")


username = input("\n\nusername: ")
password = input("password: ")



print("\n\nWELCOME!")

print("\n_______________________________\n")
print("USER: " + username)
print("\n_______________________________\n")
driver=webdriver.Chrome(path)

# opening wordplay website
driver.get('https://wordplay.com/login')

driver.find_element_by_id('username').send_keys(username)

driver.find_element_by_id('password').send_keys(password)

driver.find_element_by_xpath('//*[@id="root"]/div/div/div/div/div/div/div[1]/form/button').click()

time.sleep(5)

main()








