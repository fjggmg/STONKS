import robin_stocks.robinhood as r
import time
import requests
from bs4 import BeautifulSoup


login = r.login('Username','Password')


def buy():
    f = open("files.txt", "r")
    cash = f.readline()
    f.close()
    qty = float(cash) / float(r.get_crypto_quote('BTC', info='bid_price'))
    f = open("files.txt", "w")
    f.write("0")
    f.write("\n" + str(qty))
    print("trade made " + str(qty) + " btc bought")
    f.close()
    # r.order_buy_crypto_by_price('BTC',1.0)
    # r.order_sell_crypto_by_quantity('BTC',0.5,10000)

def buy1():
    cash = str(r.load_phoenix_account(info='account_buying_power'))
    cash = cash.replace("{'currency_code': 'USD', 'currency_id': '1072fc76-1862-41ab-82c2-485837590762', 'amount': '","")
    cash = cash.replace("'}", "")
    cash = float(cash)
    r.order_buy_crypto_by_price('BTC', cash, 'bid_price')
    print(str(r.get_crypto_positions(info='quantity_available')))
    print("bought btc " + str(r.get_crypto_positions(info='quantity_available')))


def sell():
    f = open("files.txt", "r")
    f.readline()
    qty = f.readline()
    f.close()
    f = open("files.txt", "w")
    qty = qty.replace("\n", "")
    cash = float(qty) * float(r.get_crypto_quote('BTC', info='bid_price'))
    f.write(str(cash))
    f.write("\n0" )
    print("trade made " + str(cash) + " btc sold")

    f.close()

def sell1():
    total = str(r.get_crypto_positions(info='quantity_available'))
    total = total.replace("['", "")
    total = total.replace("']", "")
    r.order_sell_crypto_by_quantity('BTC', total)
    cash = str(r.load_phoenix_account(info='account_buying_power'))
    cash = cash.replace("{'currency_code': 'USD', 'currency_id': '1072fc76-1862-41ab-82c2-485837590762', 'amount': '", "")
    cash = cash.replace("'}", "")
    print("sold btc for " + cash)


def logic(total1):
    x = []
    buywatch = False
    sellwatch = False

    while len(x) < 50:
        #f = open("files.txt", "r")
        #cash = float(f.readline())
        #qty = float(f.readline())
        #f.close()
        cash = str(r.load_phoenix_account(info='account_buying_power'))
        cash = cash.replace("{'currency_code': 'USD', 'currency_id': '1072fc76-1862-41ab-82c2-485837590762', 'amount': '", "")
        cash = cash.replace("'}", "")
        cash = float(cash)

        qty = str(r.get_crypto_positions(info='quantity_available'))
        qty = total.replace("['", "")
        qty = total.replace("']", "")
        qty = float(qty)


        y = float(r.get_crypto_quote('BTC', info='bid_price'))
        print(y)
        x.append(y)

        z = len(x) - 1
        dif = round(((x[0]-x[z])/x[z])*100, 5)
        print(dif)


        if dif > .001 and sellwatch == False and cash != 0:
            buywatch = True


        if buywatch:
            if x[z] > x[z - 1] > x[z - 2]:
                buy1()
                sellwatch = True
                buywatch = False
        if qty != 0:
            if x[z] < x[z - 1] < x[z - 2]:
                sell1()
                sellwatch = False
        time.sleep(1)



#f = open("files.txt", "w+")
#f.write('100')
#f.write('\n')
#f.write('0')
#f.close()



def getticks():
    res = requests.get(
        'https://www.tradingview.com/markets/stocks-usa/market-movers-gainers/')
    soup = BeautifulSoup(res.text, "html.parser")
    all_td_tags = []

    # Set all_h1_tags to all h1 tags of the soup
    for element in soup.select('td'):
        all_td_tags.append(element.text)

    # Create seventh_p_text and set it to 7th p element text of the page
    x=0
    tick = ""

    f = open("ticks.txt", "w")
    f.close()
    f = open("ticks.txt", "a")
    while (x < 1100): #1100 for entire list
        s = soup.select('td')[x].text
        s = s.replace("\n", "|")
        s = s.replace("\t", "|")
        if x%11 == 0:
            ress = ''
            for i in range(0, len(s)):
                if i>3 and i<10:
                    ress = ress + s[i]
            s=ress
            s = s.replace("|", "")

            tick = s
            percent = soup.select('td')[x + 2].text
            percent = percent.replace("%", "")
            percent = float(percent)
            if "/" not in s:
                if "." not in s:
                    if soup.select('td')[x + 4].text == "Buy" or soup.select('td')[x + 4].text == "Strong Buy":
                        if percent < 30.00:
                            f.write(tick + "\n")

        s = s.replace("|", "")
        if x%11 == 2:
            s = s.replace("%", "")
            s = float(s)



        if x%11 == 0 or x % 11 == 2 or x % 11 == 4:
            print(s)
        if x%11 == 5:
            print()

        x = x+1

    f.close()




    current = r.get_quotes(tick, info='ask_price')
    print(current)
    cash = str(r.load_phoenix_account(info='account_buying_power'))
    print(cash)
    print(current)

def buyer():
    f = open("prices.txt", "w")
    f.close()
    d = open("shares.txt", "w")
    d.close()
    x=0
    totalcash = 1000.00
    price = 0.0
    z = open("ticks.txt", "r")
    tick = z.readline()
    while tick != '':
        currentbuy = str(r.get_quotes(tick, info='ask_price'))
        f = open("prices.txt", "a")
        currentbuy = currentbuy.replace("['", "")
        currentbuy = currentbuy.replace("']", "")
        f.write(currentbuy + "\n")
        tick = z.readline()
        x=x+1
    z.close()
    f.close()
    f = open("prices.txt", "r")
    d = open("shares.txt", "a")
    price = (f.readline())
    price = price.replace("\n", "")
    price = price.replace(' ', "")
    price = (price)
    coun = x
    while coun > 0:
        share = ((totalcash / x) / float(price))
        print(share)
        price = (f.readline())
        d.write(str(share) + "\n")
        price = price.replace("\n", "")
        price = price.replace(' ', "")
        price = (price)
        coun = coun - 1


    d.close()
    f.close()


def tracker():
    f = open("ticks.txt", "r")
    d = open("shares.txt", "r")
    share = 0
    total = 0
    price = 0
    share = d.readline()
    time.sleep(5)
    while share != '':

        currentTick = f.readline()
        price = str(r.get_quotes(currentTick, info='bid_price'))
        price = price.replace("['", "")
        price = price.replace("']", "")
        total = total + float(share) * float(price)
        share = d.readline()
        share = share.replace("\n", "")
        share = share.replace(" ", "")
    print(total)
    f.close()
    d.close()




getticks()
buyer()
while (True):
    tracker()
x=0
while (x==1):

    total = str(r.get_crypto_positions(info='quantity_available'))
    total = total.replace("['", "")
    total = total.replace("']", "")
    cash = str(r.load_phoenix_account(info='account_buying_power'))
    cash = cash.replace("{'currency_code': 'USD', 'currency_id': '1072fc76-1862-41ab-82c2-485837590762', 'amount': '", "")
    cash = cash.replace("'}", "")
    print(cash)
    print(total)
    logic(total)

    print(current)



#print(cryptocompare.get_price('BTC',curr='USD',full=False))
#r.order_buy_crypto_by_price('BTC',1.0)
#r.order_sell_crypto_limit('BTC',0.5,10000)
