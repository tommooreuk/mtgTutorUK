from bs4 import BeautifulSoup
import requests
import warnings
warnings.filterwarnings("ignore")

cardname = raw_input("Enter the name of a magic card: ")

a = cardname.replace(' ', '-').lower()
c = "".join(z for z in a if z not in ('!','.',':',",","'"))

r  = requests.get("https://www.magicmadhouse.co.uk/search/magic-the-gathering-c1/singles-english-t85/" + c)
data = r.text
soup = BeautifulSoup(data,"html.parser")

test = soup.findAll("div", { "class" : "product_details" })

print "\n\n", len(test), "MATCHES FOUND FOR", cardname.upper()

for n in range(len(test)):
    print str(test[n].find("span",{ "class" : "GBP" }))[20:-7], ",", str(test[n].find("div",{ "class" : "product_stock_status" }))[35:-6]


