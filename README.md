# LAZADA SCRAPER
Lazada Scraper GUI is a lightweight desktop tool that extracts product data from Lazada Philippines based on user-defined keywords.

Built with Python, Selenium, BeautifulSoup, and Tkinter, it automates product searches and displays:

![image alt](https://github.com/Ryan402521/The-requirements.txt/blob/2e2ce3b69891722ea4b85f4af9c7ae8ae6c25520/Screenshot%20(324).png)
Results are shown in a clean, sortable table and can be saved as a CSV file for further analysis.
Perfect for researchers, online sellers, and data enthusiasts—no coding required.


## Features

**keyword Search:**
Enter any keyword (laptop, makeup, shoes) and the app will search Lazada for related products automatically.

**Pagination Support:**
 Scrapes multiple Lazada pages based on your input. Each page contains around 40 products, allowing you to collect more results (3 pages = ~120 items).
 
**Data Display in Table:**
 After scraping, the data is shown in a user-friendly table (Treeview) within the app. You can scroll, view, and interact with the product list instantly.
 
**Clickable Links:**
 Double-click any product row to open its Lazada page in your default web browser. Helpful for viewing full product details or making purchases.
 
**Sorting Options:**
 Easily sort the displayed data by:
 - Highest Sold
 - Lowest Sold
 - Highest Price
 - Lowest Price
 This makes it easy to analyze the most popular or most affordable items.
 
**CSV Export:**
 You can choose to automatically or manually save the scraped data into a .csv file. This file can be opened in Excel or Google Sheets for further use.
 
**CAPTCHA Detection:**
 If Lazada shows a CAPTCHA, the app will pause and notify you with a popup. You can solve the CAPTCHA manually, and the app will continue scraping afterward.

 ## Requirements to Run the App

 **Python Version:**
Python 3.7 or higher
(Recommended: 3.10+)

Download it from: https://www.python.org/downloads/

## Install Required Python Packages
Open Command Prompt (CMD) and run:

- pip install selenium
- pip install beautifulsoup4
- pip install webdriver-manager

  
## How to Use the App
**Step 1:** Enter Search Keyword
-	Example: laptop, powerbank, shoes

**Step 2:** Set Number of Pages
-	Example: 3 (scrapes 3 pages × 40 items = 120 items approx.)

**Step 3:** Choose Sort Option
-	Highest Sold
-	Lowest Sold
-	Higher Price
-	Lower Price
  
**Step 4:** Check or Uncheck "Save as CSV"
-	If checked, you’ll be asked to save the file after scraping.

**Step 5:** Click “Start Scraping”
-	Chrome will open
- Keyword will be typed automatically into Lazada
-	Products will be scraped page-by-page
-	If CAPTCHA appears, a warning will pop up
**File Menu Options**
-	Save as CSV: Save the currently displayed data.
-	View Recent Data: Load any CSV you previously saved and display it in the table.
**Notes**
-	Each Lazada page contains around 40 products.
-	Double-click any row to open the product link in your browser.
-	Scraping takes ~2–5 seconds per page.
-	CAPTCHA handling is basic. If CAPTCHA shows, the app will wait for you to solve it manually.



