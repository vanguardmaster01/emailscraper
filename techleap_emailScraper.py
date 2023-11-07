import csv
import time

import regex
from bs4 import BeautifulSoup as soup
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities
from selenium.webdriver.firefox.options import Options

headers = {
    "Accept-Language": "en-US,en;q=0.9",
    "Accept-Encoding": "br, gzip, deflate",
    "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8,application/signed-exchange;v=b3;q=0.9",
    "Referer": "https://www.google.com/"
}
pages = []
names = []
los = []
e_data = []


################################################
def load_files():
    in1 = input("Enter Input CSV Name:")
    in2 = input("Enter Output CSV Name:")
    with open(in1, 'r', encoding="utf-8") as file:
        reader = csv.reader(file)
        for row in reader:
            if "Company_name" != row[0]:
                pages.append(row[1])
                names.append(row[0])
                los.append(row[2])
    print(len(pages), "found in csv")
    return in2


in2 = load_files()
p = 1


######################################################
######################################################
def Scrape():
    global p
    for i in pages:
        try:
            options = Options()
            d = DesiredCapabilities.FIREFOX
            d["marionette"] = True
            driver = webdriver.Firefox(desired_capabilities=d, options=options)
            driver.header_overrides = headers
            time.sleep(3.5)
            driver.get(i)
            time.sleep(3.4)
            emails = regex.findall(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', driver.page_source,
                                   timeout=100)
            email1 = list(emails)
            sp = soup(driver.page_source, "lxml")
            contact = sp.findAll("a")
            for tag in contact:
                try:
                    if tag["href"] == "Contact" or tag["href"] == "contact" or tag[
                        "href"] == "Contact Us" or "Contact" in tag["href"] or "contact" in tag[
                        "href"] or "CONTACT US" in tag["href"] or "contact-us" in tag[
                        "href"] or tag.text == "Contact" or tag.text == "contact" or tag.text == "Contact Us" or "Contact" in tag.text or "contact" in tag.text or "CONTACT US" in tag.text or "contact-us" in tag.text:
                        k = tag["href"]
                        break
                except Exception as e:
                    continue
            else:
                k = "None"
            if "http" in k or "https" in k:
                url = k
            else:
                counter = 0
                for l in k:
                    if "/" == l:
                        counter += 1
                if counter > 1:
                    k = k
                else:
                    k = k.replace("/", "")
                    k = k.replace("en", "")
                if "html" in k:
                    k = k
                else:
                    k = k.replace(".", "")
                url = i + "/"
                url = url.replace("//", "/")
                url = url.replace("///", "/")
                url = url + k
            try:
                driver.get(url)
                time.sleep(3.9)
                emails = regex.findall(r'([a-zA-Z0-9+._-]+@[a-zA-Z0-9._-]+\.[a-zA-Z0-9_-]+)', driver.page_source,
                                       timeout=100)
                email2 = list(emails)
            except Exception as e:
                email2 = []
        except Exception as e:
            email1 = []
            email2 = []
        email_o = email1 + email2
        for n in email_o:
            if ".png" in n or ".jpg" in n or "fancybox@3.5.7" in n or "jquery" in n or " focus-within-polyfill@5.0.9" in n or "requirejs-bolt@2.3.6" in n or "core-js-bundle@" in n or "lodash@4.17.15" == n:
                email_o.remove(n)
        email_o = str(email_o).replace(",", "|")
        e_data.append(email_o)
        print(p, email_o)
        p += 1
        driver.quit()


if __name__ == "__main__":
    Scrape()
    f = open(in2, "w", encoding="utf-8")  # csv name
    f.write("Company_Name,website,location,Email\n")
    for i in range(len(names)):
        f.write(names[i] + "," + pages[i] + "," + los[i] + "," + e_data[i] + "\n")
    f.close()
