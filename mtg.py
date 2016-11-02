#MtGTutorUK created by Kyle Burns. Takes in a MtG card name and returns the prices of which several sites sell that card. 
#Uses BeautifulSoup to scrape the data from five popular UK MtG websites and get the type, price and stock of each card.
#BeautifulSoup4 must be installed to run this script.

from bs4 import BeautifulSoup
import string
import requests
import warnings
warnings.filterwarnings("ignore")

#/////

def magicmadhouse(card):

    #Format the input card name to match the URL query. 
    a = card.replace(' ', '-').lower()
    c = "".join(z for z in a if z not in ('!','.',':',",","'"))

    #Request the search page for the website. If this fails, return an error message.
    try:
        r  = requests.get("http://www.magicmadhouse.co.uk/search/magic-the-gathering-c1/" + c,timeout=5)
    except:
        print "Unable to reach website at this time."
        return False

    #Format the data and find all occurences of the 'product_details' class.
    data = r.text
    soup = BeautifulSoup(data,"html.parser")

    test = soup.findAll("div", { "class" : "product_details" })

    #For each product that the search page returns:
    for n in range(len(test)):
        #Scrape the title of the card.
        x = str(test[n].find({ "a" : "product_title"})).lower()[:-4]
        for k in range(3):
            x = x[x.index(">")+2:]
        #If the card title matches the input value or is a variation of the same card (indicated by a '(' character):
        if (x == card.lower() or x[:len(card)+2] == card.lower() + " ("):
            #Print the title, price and quantity of the card.
            print x, ",", str(test[n].find("span",{ "class" : "GBP" }))[20:-7], ",", str(test[n].find("div",{ "class" : "product_stock_status" }))[35:-6]

#/////
            
def magicsingles(card):

    #Format the input card name to match the URL query. 
    a = card.replace(',','%2C').replace(' ','+').lower()

    #Request the search page for the website. If this fails, return an error message.
    try:
        r  = requests.get("http://www.magicsingles.co.uk/index.php?subcats=N&status=A&pshort=N&pfull=N&pname=Y&pkeywords=N&search_performed=Y&match=all&q=" + a + "&dispatch[products.search]=Search",timeout=5)
    except:
        print "Unable to reach website at this time."
        return False

    #Format the data and find all occurences of the 'prod-info' class.
    data = r.text
    soup = BeautifulSoup(data,"html.parser")

    test = soup.findAll("div", { "class" : "prod-info" })

    #For each product that the search page returns:
    for n in range(len(test)):
        #Scrape the title, quantity and price of the card.
        x = str(test[n].findAll("span", {"class" : "price-num"})[1])
        y = str(test[n].find("span",{ "class" : "qty-in-stock"}))
        z = str(test[n].find("a",{ "class" : "product-title"}))
        z = z[z.index(">")+1:-4].lower()

        #Remove unncecessary whitespace and characters present in the data.
        if y != "None":
            y = y[y.index(">")+39:-40]
        if y[0] == "Â":
            y = "1" + y[1:]
        #If the card title matches the input value or is a variation of the same card (indicated by a '(' or '/' character):           
        if(z == card.lower() or z[:len(card)+2] == card.lower() + " (" or z[:len(card)+2] == card.lower() + " /"):
            #Print the title, price and quantity of the card.
            print z, ",", "£" + x[x.index(">")+1:-7] , ",", y.replace("Â","")

#/////
            
def trolltrader(card):

    #Format the input card name to match the URL query. 
    a = card.replace(',','%2C').replace(' ','+').lower()

    #Request the search page for the website. If this fails, return an error message.
    try:
        r  = requests.get("http://www.trolltradercards.com/products/search?q=" + a,timeout=5)
    except:
        print "Unable to reach website at this time."
        return False

    #Format the data and find all occurences of the 'product' class.
    data = r.text
    soup = BeautifulSoup(data,"html.parser")

    test = soup.findAll("li", { "class" : "product"})

    #For each product that the search page returns:
    for n in range(len(test)):
        #Scrape the title, quantity and price of the card.
        x = str(test[n].find("span", {"class" : "price"}, {"itemprop" : "price"}))
        y = str(test[n].find("span",{ "class" : "qty"}))
        z = str(test[n].find("h4", {"class" :"name"}))
        z = z[z.index(">")+1:-5].lower()
        #If quantity is 0, reassemble the data string appropriately.
        if y != "None":
            y = "".join(y[y.index(">")+1:-7].split())
        else:
            y = "0instock"
        #If the card title matches the input value or is a variation of the same card (indicated by a '-' or '/' character):               
        if(z == card.lower() or z[:len(card)+2] == card.lower() + " -" or z[:len(card)+2] == card.lower() + " /"):
            #Print the title, price and quantity of the card.            
            print z, ",", "".join(x[x.index(">")+1:-7].split())[1:], ",", y[:-7], "in stock"

#/////
            
def manaleak(card):

    #Format the input card name to match the URL query. 
    a = card.replace(',','%2C').replace(' ','+').lower()

    #Request the search page for the website. If this fails, return an error message.
    try:
        r  = requests.get("http://www.manaleak.com/magic-the-gathering/advanced_search_result.php?keywords=" + a,timeout=5)
    except:
        print "Unable to reach website at this time."
        return False

    #Format the data and find all occurences of the 'product_info_wrapper' class.    
    data = r.text
    soup = BeautifulSoup(data,"html.parser")    

    test = soup.findAll("div", { "class" : "product_info_wrapper"})
    test = test[:-8]

    #For each product that the search page returns:
    for n in range(len(test)):
        #Scrape the title, quantity and price of the card.
        x = str(test[n].find("span", {"class" : "productSpecialPrice"}))[35:-7]
        y = str(test[n].find("button", {"class" : "pull-left qty_change qty_minus"}))[61]
        z = str(test[n].find("h3", {"class" : "product_name_wrapper name equal-height_listing_name"}))[70:-16]
        z = z[z.index(">")+1:].lower()
        #If the card title matches the input value or is a variation of the same card (indicated by a '(' or '/' character):   
        if(z == card.lower() or z[:len(card)+2] == card.lower() + " -" or z[:len(card)+2] == card.lower() + " /" or z[:len(card)+2] == card.lower() + " ("):
            #Print the title, price and quantity of the card.             
            print z, ",", x,",", y, "in stock"
    

#/////

def magiccardtrader(card):

    #Format the input card name to match the URL query.     
    a = card.replace(',','%2C').replace(' ','+').lower()

    #Request the search page for the website. If this fails, return an error message.
    try:
        r  = requests.get("http://www.themagiccardtrader.com/products/search?query=" + a + "&x=0&y=0",timeout=5)
    except:
        print "Unable to reach website at this time."
        return False

    #Format the data and find all entries in the product list. (The HTML data for this website was awkward to scrape)      
    data = r.text
    soup = BeautifulSoup(data,"html.parser")

    test = soup.findAll("td", {"width":"100%"}, {'valign':"top"})

    #For each product that the search page returns:
    for n in range(len(test)):
        #Scrape the title, quantity and price of the card.
        x = str(test[n].find("td", {"class" : "qty"}))
        y = str(test[n].find("td", {"class" : "price"}))[19:-5].strip()
        #If quantity is 0, reassemble the data string appropriately.        
        if x == "None":
            x = "x 0"
        else:
            x = x[17:-5]
            y = y[1:]
        z = str(test[n])[31:]
        z = z[z.index(">")+1:]
        z = z[:z.index("<")].lower()

        #If the card title matches the input value or is a variation of the same card (indicated by a '-' or '/' character):          
        if(z == card.lower() or z[:len(card)+2] == card.lower() + " -" or z[:len(card)+2] == card.lower() + " /"):
            #Print the title, price and quantity of the card.  
            print z, ",", y,",", x.strip()

while True:
    a = raw_input("\nEnter a card name or enter q to quit: ")    #Repeatedly prompt user to enter a card name until Q is entered.

    if a == "q":
        quit()
        
    print "\nMagicSingles:\n"   
    magicsingles(a)

    print "\nTrollTraders:\n"
    trolltrader(a)

    print "\nManaLeak:\n"
    manaleak(a)

    print "\nTheMagicCardTrader:\n"
    magiccardtrader(a)

    print "\nMagicMadhouse:\n"
    magicmadhouse(a)


