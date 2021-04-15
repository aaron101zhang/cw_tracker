from selenium import webdriver
from selenium.webdriver.common.action_chains import ActionChains
import time
import numpy as np
import math
import re
from .models import AuthorizedUser, DailyData, Participant
from datetime import datetime, timedelta


# Grabs pseudonyms and messages, parses for names using messages that begin with '!'. 
def grab_userMap(driver, userList):
    senders = driver.find_elements_by_class_name("chat--message--sender")
    messages = driver.find_elements_by_class_name("chat--message--text")
    print("Found {} senders".format(len(senders)))

    #html_file = open("senders.txt", "w")
    chat_count = len(senders)

    #Uses color as key for username
    userMap = {}
    for msg in range(chat_count):
        username = messages[msg].text[1:]
        if len(messages[msg].text) > 0:
            if(messages[msg].text[0] == '!' and (username in userList)):
                #Checks for !, adds to dictionary

                #locates sender color, saves as tuple of ints
                senderElem = senders[msg]
                strin = senderElem.value_of_css_property('color')
                color = tuple(map(int, re.findall(r'\d+', strin)[0:3]))

                userMap[color] = username

    #returns color key relating color tuple to sender string
    return userMap

def attributeSquares(color_arr, userMap):
    contributions = {}

    dim = len(color_arr)
    textCellCount = 0
    for i in range(dim):
        for j in range(dim):
            userColor = color_arr[i][j]
            
            #exclude black squares
            if(userColor != (21,21,21)):
                textCellCount += 1
                name = userMap.get(userColor)
                if(name is not None):
                    contributions[name] = contributions.get(name,0) + 1
    print(textCellCount)
    return contributions

    #return a dict containing person:cellcount

#users = ["T","jeff", "arthur", "kevin", "aaron", "urmom", "stanley", "derk", "Monke", "jess", "guh", "stephen", "bess", "3kandy", "trum", "me", "unlucky", "truman", "monke"]
def scrapeData(input1, users):

    options = webdriver.ChromeOptions()
    options.add_argument('--ignore-certificate-errors')
    options.add_argument('--incognito')
    #options.add_argument('--headless')
    driver = webdriver.Chrome("C:\\Users\\aaron\\Desktop\\Crossword-tracker\\chromedriver_win32_89\\chromedriver.exe", chrome_options = options)


    print("Input crossword URL:")
    #input()
    #Takes in URL
    #print("Tries to obtain driver")
    driver.implicitly_wait(10)
    driver.get(input1)
    #print("Driver obtained")




    #Options menu
    element = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[1]/div/div[1]/div[5]")
    element.click()
    driver.implicitly_wait(10)

    #Clicks "Color Attribution"
    element2 = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[1]/div/div[1]/div[5]/div/div[3]")

    action=ActionChains(driver)
    action.move_to_element(element2)
    action.click(element2).perform()
    driver.implicitly_wait(10)
    #cells = grab_cell_colors(driver)



    first_cells = driver.find_elements_by_class_name("grid--cell")
    cw_size = math.isqrt(len(first_cells))
    color_arr = np.empty((cw_size,cw_size), dtype=list)

    #grab initial cell colors for grid
    for i in range(cw_size):
        for j in range(cw_size):
            elem = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/table/tbody/tr[{}]/td[{}]/div".format(i+1, j+1))
            
            strin = elem.value_of_css_property('background-color')
            color_arr[i][j] = tuple(map(int, re.findall(r'\d+', strin)[0:3]))

    covered_cells = np.empty(0)

    first_colored = (0,0,0)
    #find the first non-black element on first row
    for col in range(cw_size):
        if(color_arr[0][col] != (21,21,21)):
            first_colored = color_arr[0][col]
            break
    print(first_colored)

    #find the covered elements on first row
    for col in range(cw_size):
        if((color_arr[0][col] == first_colored) or (color_arr[0][col] == (31,255,61))):
            covered_cells = np.append(covered_cells,int(col))
    print(covered_cells)

    #finds another cell to click
    print("attempts to press button")

    for j in range(cw_size):
        if(color_arr[1][int(j)] != (21,21,21)):
            driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/table/tbody/tr[{}]/td[{}]/div".format(2, j+1)).click()
            break


    driver.implicitly_wait(5)


    #regrabs the selected colors, after moving the cursor elsewhere
    for j in covered_cells:
        elem = driver.find_element_by_xpath("//*[@id=\"root\"]/div/div/div[2]/div[1]/div/div[2]/div/div[1]/div/div/div[1]/div[2]/table/tbody/tr[{}]/td[{}]/div".format(1, j+1))
        
        strin = elem.value_of_css_property('background-color')
        type(j)
        color_arr[0][int(j)] = tuple(map(int, re.findall(r'\d+', strin)[0:3]))

    print(color_arr)


    #we have extracted array of colors

    userMap = grab_userMap(driver, users)
    attSquares = attributeSquares(color_arr, userMap)

    playerContributions = attSquares
    #textCellCount = attSquare.1

    print(playerContributions)



    #Grabs date
    dateElem = driver.find_element_by_class_name("chat--header--title")
    destring = dateElem.text
    
    x = (list(filter(None, re.split('\s|,', destring))))

    date = x[3] + " " + x[4] + " " + x[5]

    dt = datetime.strptime(date,"%B %d %Y")


    #Grabs time
    timer = driver.find_element_by_class_name("clock").text

    colons = timer.count(":")
    timer = timer[1:(len(timer)-1)]
    delta = timedelta(hours=0)

    if(colons == 1):
        times = timer.split(":")
        delta = timedelta(hours = 0, minutes = int(times[0]), seconds = int(times[1]))
    elif(colons == 2):
        times = timer.split(":")
        delta = timedelta(hours = int(times[0]), minutes = int(times[1]), seconds = int(times[2]))


    driver.quit()
    return (playerContributions, dt, delta)

