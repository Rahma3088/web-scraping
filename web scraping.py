#!/usr/bin/env python
# coding: utf-8

# In[13]:


import csv
from bs4 import BeautifulSoup
import requests


# In[14]:


url = "https://www.baraasallout.com/test.html"
response = requests.get(url)
soup = BeautifulSoup(response.content, "html.parser")


# In[15]:


headings = [h.get_text(strip=True) for h in soup.find_all(['h1', 'h2'])]
paragraphs = [p.get_text(strip=True) for p in soup.find_all('p')]
list_items = [li.get_text(strip=True) for li in soup.find_all('li')]


# In[16]:


with open("Extract_Text_Data.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Type", "Content"])
    for heading in headings:
        writer.writerow(["Heading", heading])
    for paragraph in paragraphs:
        writer.writerow(["Paragraph", paragraph])
    for item in list_items:
        writer.writerow(["List Item", item])


# In[17]:


table_rows = soup.find("table").find_all("tr")
table_data = []

for row in table_rows:
    cols = [col.get_text(strip=True) for col in row.find_all('td')]
    if cols:  # Skip header row
        table_data.append(cols)


with open("Extract_Table_Data.csv", "w", newline='', encoding="utf-8") as csvfile:
    writer = csv.writer(csvfile)
    writer.writerow(["Product Name", "Price", "Stock Status"])
    writer.writerows(table_data)


# In[ ]:


import json


cards = soup.find_all(class_="book-card")
product_info = []

for card in cards:
    title = card.find("h3").get_text(strip=True)
    price = card.find(class_="price").get_text(strip=True)
    availability = card.find(class_="availability").get_text(strip=True)
    button_text = card.find("button").get_text(strip=True)
    product_info.append({
        "Title": title,
        "Price": price,
        "Availability": availability,
        "Button": button_text})


with open("Product_Information.json", "w", encoding="utf-8") as jsonfile:
    json.dump(product_info, jsonfile, indent=4)


# In[20]:


forms = soup.find_all("form")
form_details = []

for form in forms:
    inputs = form.find_all("input")
    for inp in inputs:
        field_name = inp.get("name", "N/A")
        input_type = inp.get("type", "N/A")
        default_value = inp.get("value", "N/A")
        form_details.append({
            "Field Name": field_name,
            "Input Type": input_type,
            "Default Value": default_value})


with open("Form_Details.json", "w", encoding="utf-8") as jsonfile:
    json.dump(form_details, jsonfile, indent=4)


# In[21]:


links = [{"text": a.get_text(strip=True), "href": a.get("href")} for a in soup.find_all("a")]
videos = [{"iframe_src": iframe.get("src")} for iframe in soup.find_all("iframe")]


with open("Links_and_Multimedia.json", "w", encoding="utf-8") as jsonfile:
    json.dump({"Links": links, "Videos": videos}, jsonfile, indent=4)


# In[22]:


featured_products = []
products = soup.select(".featured-product")

for product in products:
    product_id = product.get("data-id")
    name = product.select_one(".name").get_text(strip=True)
    hidden_price = product.select_one(".price").get_text(strip=True)
    colors = product.select_one(".colors").get_text(strip=True)
    featured_products.append({
        "id": product_id,
        "name": name,
        "price": hidden_price,
        "colors": colors})


with open("Featured_Products.json", "w", encoding="utf-8") as jsonfile:
    json.dump(featured_products, jsonfile, indent=4)


# In[ ]:





# In[ ]:





# In[ ]:




