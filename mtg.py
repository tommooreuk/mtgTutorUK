from bs4 import BeautifulSoup
import string
import requests
import warnings
warnings.filterwarnings("ignore")

def magicmadhouse(card):
    a = card.replace(' ', '-').lower()
    c = "".join(z for z in a if z not in ('!','.',':',",","'"))

    r  = requests.get("https://www.magicmadhouse.co.uk/search/magic-the-gathering-c1/singles-english-t85/" + c)
    data = r.text
    soup = BeautifulSoup(data,"html.parser")

    test = soup.findAll("div", { "class" : "product_details" })

    print len(test), "MATCHES FOUND FOR", card.upper()

    for n in range(len(test)):
        print str(test[n].find("span",{ "class" : "GBP" }))[20:-7], ",", str(test[n].find("div",{ "class" : "product_stock_status" }))[35:-6]

def magicsingles(card):
    a = card.replace(',','%2C').replace(' ','+').lower()

    r  = requests.get("http://www.magicsingles.co.uk/index.php?subcats=N&status=A&pshort=N&pfull=N&pname=Y&pkeywords=N&search_performed=Y&match=all&q=" + a + "&dispatch[products.search]=Search")
    data = r.text
    soup = BeautifulSoup(data,"html.parser")

    test = soup.findAll("div", { "class" : "prod-info" })

    print len(test), "MATCHES FOUND FOR", card.upper()
    
    for n in range(len(test)):
        x = str(test[n].findAll("span", {"class" : "price-num"})[1])
        y = str(test[n].find("span",{ "class" : "qty-in-stock"}))
        if y != "None":
            y = y[y.index(">")+39:-40]
        if y[0] == "Â":
            y = "1" + y[1:]
        print "£" + x[x.index(">")+1:-7] + " , " + y.replace("Â","")

        #print str(test[n].find("span", {"class" : "price"}))[142:-14]
    
a = raw_input("Enter a card name: ")

print "\nMagicSingles:\n"   
magicsingles(a)

print "\nMagicMadhouse:\n"
magicmadhouse(a)



