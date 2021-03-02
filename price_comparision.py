from bs4 import BeautifulSoup
import requests
import math


# Here we are sending a http request to sites so we can get a html data back
header = {
    "User-Agent": "Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/88.0.4324.190 Safari/537.36"}


respons_amazon = requests.get(
    "https://www.amazon.se/dp/B07TWFVDWT/ref=s9_acsd_al_bw_c2_x_0_i?pf_rd_m=ANU9KP01APNAG&pf_rd_s=merchandised-search-2&pf_rd_r=R7G5EHEY4E8E8H92MHY5&pf_rd_t=101&pf_rd_p=28e6ca67-dde9-49c0-a62c-f21d26aa69ac&pf_rd_i=20653045031", headers=header)
respons_amazon.raise_for_status()


respons_prisjakt = requests.get(
    "https://www.computersalg.se/i/5823635/fitbit-versa-2-dimma-gr%C3%A5-smart-klocka-med-band-silikon-sten-bluetooth-40-g?utm_source=prisjaktSe&utm_medium=prisjaktSeLINK&utm_campaign=prisjaktSe", headers=header)
respons_prisjakt.raise_for_status()


# Prices
prices_amazon = []
prices_prisjakt = []
# Here we are creating a beautifulsoup objects
soup_amazon = BeautifulSoup(respons_amazon.content, "html.parser")
soup_prisjakt = BeautifulSoup(respons_prisjakt.content, "html.parser")

# Extracting the data from amazon
product_data_amazon = soup_amazon.find_all(
    class_="centerColAlign centerColAlign-bbcxoverride")

product_name_amazon = product_data_amazon[0].find(
    "span", class_="a-size-large product-title-word-break").text
product_price_amazon = product_data_amazon[0].find(
    "span", class_="a-size-medium a-color-price priceBlockBuyingPriceString").text

prices_amazon.append(product_name_amazon)
prices_amazon.append(product_price_amazon)


# Extracting the data from prisjakt
product_data_prisjakt = soup_prisjakt.find_all(
    class_="wrap spec")

product_name_prisjakt = product_data_prisjakt[0].find_all(
    "td", class_="specLine")[1].text


product_price_data = soup_prisjakt.find_all(class_="product-price-wrap")
pris_jakt_price = product_price_data[0].find("span", itemprop="price").text

prices_prisjakt.append(product_name_prisjakt)
prices_prisjakt.append(pris_jakt_price)

print("Amazon:")
for item in prices_amazon:
    print(item)

print("\n")

print("Computer Salg")

for item in prices_prisjakt:
    print(item)
