import csv
import os
import re
import webbrowser
import time
from tkinter import *
from tkinter import filedialog, messagebox, ttk
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.common.keys import Keys
from selenium.webdriver.chrome.service import Service
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from webdriver_manager.chrome import ChromeDriverManager
from bs4 import BeautifulSoup

original_data = []
recent_data = []

def sold_to_number(sold_str):
    try:
        if 'k' in sold_str.lower():
            return float(sold_str.lower().replace('k', '').replace('sold', '').strip()) * 1000
        return float(re.sub(r'[^\d.]', '', sold_str))
    except:
        return 0

def check_captcha(driver):
    try:
        if "captcha" in driver.current_url.lower() or "Please verify" in driver.page_source:
            messagebox.showwarning("CAPTCHA Detected", "Please solve the CAPTCHA manually and click OK.")
            while "captcha" in driver.current_url.lower() or "Please verify" in driver.page_source:
                driver.implicitly_wait(5)
    except:
        pass

def scrape_lazada(keyword, max_pages, sort_choice):
    global recent_data, original_data
    options = webdriver.ChromeOptions()
    driver = webdriver.Chrome(service=Service(ChromeDriverManager().install()), options=options)
    wait = WebDriverWait(driver, 10)

    driver.get("https://www.lazada.com.ph/")

    try:
        search_box = wait.until(EC.presence_of_element_located((By.ID, 'q')))
        search_box.clear()
        search_box.send_keys(keyword)
        search_box.send_keys(Keys.RETURN)
        wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-qa-locator="product-item"]')))
    except:
        driver.quit()
        return []

    sort_param = ''
    if sort_choice == "Top Sale":
        sort_param = 'pop'
    elif sort_choice == "Newest":
        sort_param = 'new'

    if sort_param:
        current_url = driver.current_url
        if 'sort=' in current_url:
            current_url = re.sub(r'sort=[^&]*', f'sort={sort_param}', current_url)
        else:
            current_url += f"&sort={sort_param}"

        try:
            old_element = driver.find_element(By.CSS_SELECTOR, 'div[data-qa-locator="product-item"]')
        except:
            old_element = None

        driver.get(current_url)

        if old_element:
            try:
                wait.until(EC.staleness_of(old_element))
                wait.until(EC.presence_of_all_elements_located((By.CSS_SELECTOR, 'div[data-qa-locator="product-item"]')))
            except:
                pass

    result_list = []
    seen_links = set()

    for page in range(1, max_pages + 1):
        time.sleep(2)
        soup = BeautifulSoup(driver.page_source, 'html.parser')
        products = soup.find_all('div', {'data-qa-locator': 'product-item'})

        for product in products:
            link_tag = product.find('a', href=True)
            link = 'https:' + link_tag['href'] if link_tag else 'N/A'
            if link in seen_links:
                continue
            seen_links.add(link)

            name = product.find('div', class_='RfADt')
            price = product.find('span', class_='ooOxS')
            name_text = name.text.strip() if name else 'N/A'
            price_text = price.text.strip() if price else '0'
            try:
                price_val = float(re.sub(r'[^\d.]', '', price_text))
            except:
                price_val = 0.0

            sold = '0 sold'
            for span in product.find_all('span'):
                if span.text and 'sold' in span.text.lower():
                    sold = span.text.strip()
                    break

            result_list.append([name_text, price_val, sold, link])

        try:
            pagination_links = driver.find_elements(By.CSS_SELECTOR, 'li.ant-pagination-item')
            for page_link in pagination_links:
                if page_link.text == str(page + 1):
                    driver.execute_script("arguments[0].click();", page_link)
                    wait.until(EC.presence_of_element_located((By.CSS_SELECTOR, 'div[data-qa-locator="product-item"]')))
                    break
            else:
                break  # if no matching page number is found
        except:
            break

    driver.quit()
    original_data = result_list.copy()
    recent_data = result_list.copy()
    return result_list



def save_as_csv():
    if not recent_data:
        return
    file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
    if file_path:
        with open(file_path, 'w', newline='', encoding='utf-8') as file:
            writer = csv.writer(file)
            writer.writerow(['Name', 'Price', 'Sold', 'Link'])
            writer.writerows(recent_data)

def view_recent_data():
    global original_data, recent_data
    try:
        file_path = filedialog.askopenfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")])
        if file_path:
            with open(file_path, 'r', encoding='utf-8') as file:
                reader = csv.reader(file)
                next(reader)
                loaded_data = [row for row in reader]

            original_data = loaded_data.copy()
            recent_data = loaded_data.copy()

            for item in tree.get_children():
                tree.delete(item)
            for index, row in enumerate(recent_data):
                tag = 'evenrow' if index % 2 == 0 else 'oddrow'
                tree.insert("", "end", values=row, tags=(tag,))
    except Exception as e:
        messagebox.showerror("Error", f"Failed to load CSV file.\n{e}")

def refresh_data_by_sold(order):
    global recent_data
    if not recent_data:
        return

    recent_data = sorted(recent_data, key=lambda x: sold_to_number(x[2]), reverse=(order == 'desc'))

    for item in tree.get_children():
        tree.delete(item)
    for index, row in enumerate(recent_data):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert("", "end", values=row, tags=(tag,))

def sort_by_price(order):
    global recent_data
    if not recent_data:
        return
    if order == 'asc':
        recent_data = sorted(recent_data, key=lambda x: float(x[1]))
    elif order == 'desc':
        recent_data = sorted(recent_data, key=lambda x: float(x[1]), reverse=True)

    for item in tree.get_children():
        tree.delete(item)
    for index, row in enumerate(recent_data):
        tag = 'evenrow' if index % 2 == 0 else 'oddrow'
        tree.insert("", "end", values=row, tags=(tag,))

def start_scraping():
    keyword = entry.get().strip()
    pages = pages_entry.get().strip()

    if not keyword:
        messagebox.showwarning("Input Error", "Please enter a keyword.")
        return
    if not pages or not pages.isdigit() or int(pages) <= 0:
        messagebox.showwarning("Input Error", "Please enter a valid number of pages (positive integer).")
        return

    max_pages = int(pages)
    sort_choice = "Top Sale"  # Default backend sorting only
    data = scrape_lazada(keyword, max_pages, sort_choice)
    data = sorted(data, key=lambda x: sold_to_number(x[2]), reverse=True)

    if save_csv_var.get():
        file_path = filedialog.asksaveasfilename(defaultextension=".csv", filetypes=[("CSV files", "*.csv")], initialfile=f"{keyword.replace(' ', '_')}_lazada.csv")
        if file_path:
            with open(file_path, 'w', newline='', encoding='utf-8') as file:
                writer = csv.writer(file)
                writer.writerow(['Name', 'Price', 'Sold', 'Link'])
                writer.writerows(data)

    global recent_data, original_data
    recent_data = data.copy()
    original_data = data.copy()
    refresh_data_by_sold('desc')

def on_link_click(event):
    selected = tree.focus()
    if selected:
        link = tree.item(selected, 'values')[3]
        if link.startswith('http'):
            webbrowser.open(link)

root = Tk()
root.title("Lazada Scraper")
root.geometry("1280x720")
root.configure(bg='white')

save_csv_var = BooleanVar(value=True)

frame_top_right = Frame(root, bg='white')
frame_top_right.pack(anchor='ne', pady=5, padx=5)

menu_bar = Menu(root, fg='blue', font=('Arial', 14))
file_menu = Menu(menu_bar, tearoff=0)
file_menu.add_command(label="Save as CSV", command=save_as_csv)
file_menu.add_command(label="View Recent Data", command=view_recent_data)
menu_bar.add_cascade(label="File", menu=file_menu)
root.config(menu=menu_bar)

frame_top = Frame(root, bg='white')
frame_top.pack(pady=10)

Label(frame_top, text="Keyword:", bg='white', fg='black', font=('Arial', 12)).grid(row=0, column=0, padx=5)
entry = Entry(frame_top, font=('Arial', 12), width=30)
entry.grid(row=0, column=1, padx=5)

Label(frame_top, text="Pages:", bg='white', fg='black', font=('Arial', 12)).grid(row=0, column=2, padx=5)
pages_entry = Entry(frame_top, font=('Arial', 12), width=5)
pages_entry.grid(row=0, column=3, padx=5)

Label(frame_top, text="Sort by:", bg='white', fg='black', font=('Arial', 12)).grid(row=0, column=4, padx=5)
combined_sort_menu = ttk.Combobox(frame_top, values=[
    "Highest Sold",
    "Lowest Sold",
    "Higher Price",
    "Lower Price"
], state="readonly", font=('Arial', 12), width=25)
combined_sort_menu.current(0)
combined_sort_menu.grid(row=0, column=5, padx=5)

def handle_combined_sort(event):
    selection = combined_sort_menu.get()
    if selection == "Highest Sold":
        refresh_data_by_sold('desc')
    elif selection == "Lowest Sold":
        refresh_data_by_sold('asc')
    elif selection == "Higher Price":
        sort_by_price('desc')
    elif selection == "Lower Price":
        sort_by_price('asc')

combined_sort_menu.bind("<<ComboboxSelected>>", handle_combined_sort)

frame_buttons = Frame(root, bg='white')
frame_buttons.pack(pady=5)

Button(frame_buttons, text="Start Scraping", command=start_scraping, bg='#333333', fg='white',
       font=('Arial', 14), width=20).pack(pady=10)

Checkbutton(frame_buttons, text="Save as CSV after scraping", variable=save_csv_var,
            bg='white', font=('Arial', 11)).pack()

style = ttk.Style()
style.configure("Treeview.Heading", font=('Arial', 12, 'bold'))
style.configure("Treeview", font=('Arial', 11), rowheight=25, background='white', fieldbackground='white', foreground='black')
style.map('TCombobox', fieldbackground=[('readonly', '#333333')], foreground=[('readonly', 'white')])

columns = ('Name', 'Price', 'Sold', 'Link')
tree = ttk.Treeview(root, columns=columns, show='headings')

for col in columns:
    tree.heading(col, text=col)
    if col == 'Price':
        tree.column(col, width=100, anchor='center')
    elif col == 'Sold':
        tree.column(col, width=100, anchor='center')
    elif col == 'Link':
        tree.column(col, width=250, anchor='center')
    else:
        tree.column(col, width=300, anchor='center')

tree.pack(expand=True, fill=BOTH, padx=10, pady=10)
tree.tag_configure('oddrow', background="#ffffff")
tree.tag_configure('evenrow', background="#f2f2f2")
tree.bind("<Double-1>", on_link_click)

root.mainloop()
