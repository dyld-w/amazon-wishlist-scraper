# from urllib.request import urlopen
import os
import re  # https://www.geeksforgeeks.org/check-if-an-url-is-valid-or-not-using-regular-expression/
import tkinter as tk

import requests
#  from selenium import webdriver
#  from selenium.webdriver.chrome.options import Options
import undetected_chromedriver as uc  # https://github.com/ultrafunkamsterdam/undetected-chromedriver
from bs4 import BeautifulSoup as BS


# function that does the actual calculating
# takes one argument which is the url to an Amazon wishlist
# returns a tuple of the number of items considered in the calculation and total cost of those items
def costCalc(url, costS=0, itemsS=0, prodList=""):
    # variables to keep track of cost and num of items
    items = itemsS
    cost = costS
    prodL = prodList
    # open webpage with selenium using Chrome
    options = uc.ChromeOptions()
    options.headless = True
    options.add_argument("--headless")
    chrome = uc.Chrome(options=options)
    chrome.get(url)
    # get source of page
    src = chrome.page_source
    chrome.quit()
    # make a soup object
    soup = BS(src, 'html.parser')
    # find body of page whre all of the relevant content is
    body = soup.find("body")
    #  print(body)

    # find the unordered list where all of the info is
    ul = body.find(
        "ul", {
            'class':
            'a-unordered-list a-nostyle a-vertical a-spacing-none g-items-section ui-sortable'
        })
    #  print(ul['id'])
    # deal with the infinite scrolling characteristic
    baseURL = "https://www.amazon.com"
    # find the section that has the end of list marker
    # will only be found at the very end of the list and will be None at any point before the end
    end = ul.find("div", {'id': "endOfListMarker"})

    if end == None:
        # find the rest of the URL that contains the next set of items
        #  print(ul['id'])
        nextPg = ul.find(
            "a", {
                'class':
                "a-size-base a-link-nav-icon a-js g-visible-no-js wl-see-more"
            })
        # add inp to the baseURL to get the URL of the next "page"
        #  print(nextPg['href'])
        loadMore = baseURL + nextPg['href']

    # for every item li in the unordered list:

    for li in ul.find_all("li"):
        # get the name
        nameSect = li.find('a', {'class': "a-link-normal"})
        product = nameSect.get("title")
        # and the price of that item
        price = li.get('data-price')

        # print the product and the product's price
        # if the product has a name and a price

        if product != None and price != '-Infinity':
            # print the name and price
            prodInfo = "\n" + product + " --- $" + price + "\n"
            prodL += prodInfo
            # add the price of the item to the total cost
            cost += float(price)
            # inc the number of items
            items += 1
        # if the product has a name but not a price, print the name and a statement saying it won't be included in the calculation, so won't add to sum cost or inc num of items
        elif product != None and price == '-Infinity':
            prodInfo = "\n" + product + " has an unknown price and won't be included in the calculation. \n"
            prodL += prodInfo

        # if end is not None that means it has been found which means we've reached the end of the list and should return the sumCost and sumItems
    # this is our base case

    if end != None:
        sumCost = round(cost, 2)
        sumItems = items

        return [sumCost, sumItems, prodL]
    # if end is None then we need to do the calculation again except this time starting on the loadMore page
    else:
        return costCalc(loadMore, cost, items, prodL)


# function to check that a string is a valid URL from  https://www.geeksforgeeks.org/check-if-an-url-is-valid-or-not-using-regular-expression/
def isValidURL(str):
    # Regex to check valid URL
    regex = ("((http|https)://)(www.)?" + "[a-zA-Z0-9@:%._\\+~#?&//=]" +
             "{2,256}\\.[a-z]" + "{2,6}\\b([-a-zA-Z0-9@:%" + "._\\+~#?&//=]*)")
    # Compile the ReGex
    p = re.compile(regex)
    # If the string is empty
    # return false

    if (str == None):
        return False
    # Return if the string
    # matched the ReGex

    if (re.search(p, str)):
        return True
    else:
        return False


# https://stackoverflow.com/questions/4719438/editing-specific-line-in-text-file-in-python
def replace_line(file_name, line_num, text):
    lines = open(file_name, 'r').readlines()
    lines[line_num] = text
    out = open(file_name, 'w')
    out.writelines(lines)
    out.close()


path = "/home/dylan/projects/wishscraper/lists.txt"


def nameCheck(n):
    name = n
    name = name.lower()
    curCost = 0
    curItems = 0
    prevCost = 0
    prevItems = 0
    ex = os.path.exists(path)
    # check to make sure the lists.txt exists in the desired directory and if not, create it

    if ex == False:
        # print("DOESN'T EXIST")
        f = open(path, "x")
        f.close()

    #  open lists.txt for reading to see if the inputted wishlist is already in lists.txt
    f = open(path, "r+")
    url = ""
    #line counter so replace_line knows which line to replace
    lnC = -1
    itemizedList = ""

    for line in f.readlines():
        nameI = line.find(name)
        lnC += 1

        if nameI != -1 and line[nameI + len(name)] == " ":
            # print(lnC)
            url = line[nameI + len(name) + 1:]
            url = url.strip()
            spaceI = line.find(" ")
            prevItems = int(line[:spaceI])
            prevCost = float(line[spaceI + 1:nameI])
            infoList = costCalc(url)
            replace_line(
                path, lnC,
                str(infoList[1]) + " " + str(infoList[0]) + " " + name + " " +
                url + "\n")
            print(str(prevCost) + " " + str(prevItems))
            outputs(infoList, prevCost, prevItems)
            f.close()

            return
    f.close()
    unknownNameFrame(name)

    return


def unknownNameFrame(name):
    # unknown wishlist
    unknownFrame = tk.Frame(root, bg='#80c1ff', bd=5)
    unknownFrame.place(relx=0.5,
                       rely=0.12,
                       relwidth=0.8,
                       relheight=0.05,
                       anchor='n')

    unknownLabel = tk.Label(unknownFrame,
                            text='Wishlist unknown. Paste URL below:',
                            bg='#80c1ff',
                            font=40)
    unknownLabel.place(relx=0.00, rely=0, relwidth=0.5, relheight=0.5)

    unknownButton = tk.Button(
        unknownFrame,
        text='Submit URL',
        bg='gray',
        command=lambda: nameNotInList(name, unknownFrame, unknownEntry,
                                      unknownLabel))
    unknownButton.place(relx=0.5, rely=0, relwidth=0.5, relheight=0.5)

    unknownEntry = tk.Entry(unknownFrame)
    unknownEntry.pack(side=tk.BOTTOM, fill=tk.X)


def nameNotInList(n, frame, entry, label):
    # if the input wishlist is not in lists.txt,
    # ask for the link to the wishlist
    # check to make sure the input is at least a valid URL
    name = n
    name = name.lower()
    curCost = 0
    curItems = 0
    prevCost = 0
    prevItems = 0

    # print("URL empty")
    f = open(path, "a+")
    #  link = input("Wishlist unkown, please insert URL to the Amazon wishlist: ")
    url = entry.get()
    valid = isValidURL(url)

    if valid == False:
        label['text'] = 'Invalid URL. Please try again.'

        return
    frame.destroy()
    infoList = costCalc(url)
    f.write(
        str(infoList[1]) + " " + str(infoList[0]) + " " + name + " " + url +
        "\n")
    outputs(infoList)
    f.close()


def outputs(infoList, prevCost=0, prevItems=0):
    print('should be getting outputs now')
    curCost = infoList[0]
    curItems = infoList[1]
    prodText.insert(tk.END, infoList[2])
    outText.insert(
        tk.INSERT, "Previously known total cost was $" + str(prevCost) +
        " for " + str(prevItems) + " items. \n")
    outText.insert(
        tk.END, "Current total cost of $" + str(curCost) + " for " +
        str(curItems) + " items. \n")
    outText.insert(
        tk.END, "Change of $" + str(round((curCost - prevCost), 2)) + " and " +
        str(round((curItems - prevItems), 2)) + " items. \n")


def reset():
    #  print(unknownLabel.cget("text"))
    #
    #  if unknownFrame != None:
    #  unknownFrame.destroy()
    prodText.delete(1.0, tk.END)
    outText.delete(1.0, tk.END)


# gui setup
root = tk.Tk()
root.title('Amazon Wishlist Scraper')
HEIGHT = 1000
WIDTH = 800
canvas = tk.Canvas(root, height=HEIGHT, width=WIDTH)
canvas.pack()

# getting input from user
frame = tk.Frame(root, bg='#80c1ff', bd=5)
frame.place(relx=0.5, rely=0.01, relwidth=0.8, relheight=0.1, anchor='n')

label = tk.Label(frame, text='Wishlist:', bg='#80c1ff', font=40)
label.place(relx=0.01, rely=0, relwidth=0.1, relheight=1)

entry = tk.Entry(frame)
entry.place(relx=0.15, rely=0, relwidth=0.73, relheight=1)

button = tk.Button(frame,
                   text="Calculate!",
                   bg='gray',
                   command=lambda: nameCheck(entry.get()),
                   font=40)
button.place(relx=0.75, rely=0, relwidth=0.25, relheight=1)

# printing out the itemized list of products
prodFrame = tk.Frame(root, bg='#80c1ff', bd=5)
prodFrame.place(relx=0.5, rely=0.18, relwidth=0.8, relheight=0.6, anchor='n')

prodText = tk.Text(prodFrame,
                   height=20,
                   width=60,
                   bg='white',
                   font=40,
                   state='normal')
prodText.place(relx=0, relwidth=0.95, relheight=1)

prodScroll = tk.Scrollbar(prodFrame)
prodScroll.place(relx=0.97, relheight=1)

prodScroll.config(command=prodText.yview)
prodText.config(yscrollcommand=prodScroll.set)

# output
outFrame = tk.Frame(root, bg='#80c1ff', bd=5)
outFrame.place(relx=0.5, rely=0.79, relwidth=0.8, relheight=0.2, anchor='n')

outText = tk.Text(outFrame, height=3, font=40, state='normal')
outText.place(relx=0, rely=0, relwidth=1, relheight=0.5)

clearButton = tk.Button(outFrame,
                        text="Reset",
                        bg='gray',
                        command=reset,
                        font=40)
clearButton.place(relx=0.5, rely=0.51, relwidth=0.5, relheight=0.5, anchor='n')

root.mainloop()
