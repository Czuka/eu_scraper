from selenium import webdriver
from selenium.common import NoSuchElementException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import Select


import time
import csv
import random



driver = webdriver.Chrome()
url = 'https://ewybory.eu/sondaze/'
driver.get(url)
combo_index = 0


def czekaj_x(a):
    time.sleep(a)
    print(f"Minęło {a} sekund!")

def przeksztalc_tekst(tekst):
    if not isinstance(tekst, str):
        raise ValueError("Podana wartość nie jest ciągiem znaków")

    # Zamiana przecinków na kropki
    tekst_po_zamianie = tekst.replace(',', '.')

    # Ucina znaki po pierwszym białym znaku
    indeks_bialego_znaku = next((i for i, znak in enumerate(tekst_po_zamianie) if znak.isspace()), len(tekst_po_zamianie))
    tekst_po_ucieciu = tekst_po_zamianie[:indeks_bialego_znaku].strip()

    return tekst_po_ucieciu


def czekaj_losowa_liczba_sekund(min_czas, max_czas):
    losowa_liczba = random.uniform(min_czas, max_czas)
    time.sleep(losowa_liczba)
    print(f"czekano {losowa_liczba}")

czekaj_x(4)

try:
    elements = driver.find_elements(By.XPATH, "//div[contains(@class, 'section_polls')]/div[contains(@class, 'section_polls_row')]")
except NoSuchElementException as e:
        print("Nie znaleziono elementu:", e)

def count_occurrences_and_print(strings_list,driver,i):
    occurrences_dict = {}
    writing_dict = {}
    counter = 0
    holder = []
    for string in strings_list:
        if "section_polls_pollster" not in string:
            if string in occurrences_dict:
                occurrences_dict[string] += 1
            else:
                occurrences_dict[string] = 1

    #for string, count in occurrences_dict.items():
        #print(f"{string}: {count} raz(y)")

    for string in strings_list:
        if "section_polls_pollster" not in string:
            if string in writing_dict:
                if "section_polls_data" != string:
                    temp =(driver.find_element(By.XPATH,
f"(//div[contains(@class, 'section_polls_row')])[{i+1}]/div[contains(@class, '{string}')][{writing_dict[string]+1}]").text)
                    temp = przeksztalc_tekst(temp)
                    print(temp)
                    holder.append(temp)
                else:
                    temp = driver.find_element(By.XPATH,
f"(//div[contains(@class, 'section_polls_row')])[{i + 1}]/div[contains(@class, '{string}')][{counter+1}]").text
                    temp = przeksztalc_tekst(temp)
                    print(temp)
                    holder.append(temp)

                    holder[-1]

                writing_dict[string] += 1
                counter += 1
            else:
                writing_dict[string] = 1
                temp = driver.find_element(By.XPATH,
                    f"(//div[contains(@class, 'section_polls_row')])[{i+1}]/div[contains(concat(' ', normalize-space(@class), ' '), ' {string} ')]").text
                temp = przeksztalc_tekst(temp)
                print(temp)
                holder.append(temp)
                holder[-1]
                counter += 1
    return holder



print(len(elements))
print(elements[1])
def get_next_div_class(driver, i):
    j = 0
    lista_elementow = []
    try:
        # Znajdź wszystkie elementy wewnątrz diva o klasie 'section_polls_row'
        elements_in_row = driver.find_elements(By.XPATH, f"(//div[contains(@class, 'section_polls_row')])[{i+1}]/div")

    except NoSuchElementException as e:
        print("Nie znaleziono elementów:", e)
    for j, next_element in enumerate(elements_in_row):
        try:
            # Sprawdź, czy istnieje element o indeksie j+1
            if j < len(elements_in_row):
                next_element = elements_in_row[j]
                next_element_class = next_element.get_attribute('class')
                if next_element_class:
                    lista_elementow.append(next_element_class)
                else:
                    print(f"Element o indeksie {j} nie ma przypisanej klasy.")
            else:
                print(f"Nie ma elementu o indeksie {j}")
                break
        except NoSuchElementException as e:
            print("Nie znaleziono elementów:", e)
    return lista_elementow

def get_text_from_classes(driver, class_list):
    text_values = []

    for class_name in class_list:
        try:
            # Znajdź wszystkie elementy o danej klasie
            elements = driver.find_element (By.CLASS_NAME, class_name)

            # Pobierz tekst z każdego znalezionego elementu
            for element in elements:
                text_values.append(element.text)
                #print(element.text)
        except NoSuchElementException as e:
            print(f"Nie znaleziono elementów o klasie {class_name}: {e}")

    return text_values
def create_csv(file_path, headers):
    with open(file_path, 'w', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        csv_writer.writerow(headers)

def add_row_to_csv(file_path, csv_headers, values):
    with open(file_path, mode='a', newline='') as csv_file:
        csv_writer = csv.writer(csv_file)
        row_data = [str(value) for value in values]
        csv_writer.writerow(row_data)

file_path = 'sondaze_data.csv'
csv_headers = ['Numer', 'Link', 'Text', 'Zleceniodawca', 'Data', 'Proba','NL','KO','TD','BS','PIS','KONF','P50','PSL']
create_csv(file_path, csv_headers)

try:
    combobox = driver.find_element(By.ID ,("pollcomselector3"))
    opcje_combobox = combobox.find_elements(By.XPATH, '//option')
    select = Select(combobox)
    wszystkie_opcje = select.options
except NoSuchElementException as e:
    print("Nie znaleziono elementu:", e)

def change_combobox():
    global combo_index
    print(f"combobox: {opcje_combobox} ")
    if combo_index+1 < len(wszystkie_opcje) :
        combo_index += 1
        print(f"change_combobox: {combo_index}")
        select.select_by_index(combo_index)
        czekaj_x(12)
    else:
        print("stop")
        czekaj_x(6000)



def scraping_master(elements):

    for i, item in enumerate(elements):
        if i == 0:
            continue
        row_scrap(i,item)



def row_scrap(i, item):
    try:
        link = item.find_element(By.XPATH, f"(//div[contains(@class, 'section_polls_pollster')])[{i}]/a")
        if link.get_attribute("href"):
            link = link.get_attribute('href')
            print("herf ")
        else:
            print("Element nie ma atrybutu href lub jest pusty.")
            link = "nie ma"
        tekscik_element = item.find_element(By.XPATH, f"(//div[contains(@class, 'section_polls_pollster')])[{i}]/a")
        tekscik = tekscik_element.text.strip()
    except NoSuchElementException as e:
        print("Nie znaleziono elementu:", e)
        print("Element nie ma atrybutu a lub jest pusty.")
        link = "nie ma"
        try:
            tekscik = item.find_element(By.XPATH, f"(//div[contains(@class, 'section_polls_pollster')])[{i}]").text
        except NoSuchElementException as e:
            print("Nie znaleziono elementu:", e)
            tekscik = "nie ma"

    try:
        zleceniodawca = item.find_element(By.XPATH,
                                          f"(//div[contains(@class, 'section_polls_pollster')])[{i}]/a/span").text
    except NoSuchElementException as e:
        print("Nie znaleziono elementu:", e)
        zleceniodawca = tekscik

    try:
        proba = item.find_element(By.XPATH,
                                  f"(//div[contains(@class, 'section_polls_pollster')])[{i}]/span[1]").text
        data = item.find_element(By.XPATH,
                                 f"(//div[contains(@class, 'section_polls_pollster')])[{i}]/span[2]").text
    except NoSuchElementException as e:
        print("Nie znaleziono elementu:", e)


    wyniki_list_clas = get_next_div_class(item, i)
    print(wyniki_list_clas)
    wyniki = count_occurrences_and_print(wyniki_list_clas, item, i)

    print(f" \n\n numer:  {i} ")
    print(f"link:  {link}")
    print(f"text:  {tekscik}")
    print(f"zleceniodawca:  {zleceniodawca}")
    print(f"data:  {data}")
    print(f"proba:  {proba} ")
    print(f"wyniki:  {wyniki} \n")
    print(f"wyniki długość:  {len(wyniki)} \n")

    values = []

    if len(wyniki) == 6:
        if wyniki[0] == "" or wyniki[0] is None or wyniki[0] == '':
            change_combobox()
            row_scrap(i,item)
        else:
            if combo_index > 0:
                values.extend(
                    [i, link, tekscik, zleceniodawca, data, proba, wyniki[0], wyniki[1], '-', '-', wyniki[4],
                     wyniki[5], wyniki[2], wyniki[3]])
                add_row_to_csv(file_path, csv_headers, values)
            else:
                values.extend([i, link, tekscik, zleceniodawca, data, proba, wyniki[0], wyniki[1], wyniki[2],
                              wyniki[3], wyniki[4],wyniki[5], '-', '-'])
            add_row_to_csv(file_path,csv_headers, values)
    elif len(wyniki) == 7:
        values.extend([i, link, tekscik, zleceniodawca, data, proba, wyniki[0], wyniki[1], '-', wyniki[4], wyniki[5],
                       wyniki[6], wyniki[2], wyniki[3]])
        add_row_to_csv(file_path, csv_headers, values)
    else:
        print("______")

scraping_master(elements)





czekaj_x(25)




'''
# funkcja pobierająca liste klas z tabeli 
def get_next_div_class(driver, i):
    j = 0
    lista_elementow = []
    try:
        # Znajdź wszystkie elementy wewnątrz diva o klasie 'section_polls_row'
        elements_in_row = driver.find_elements(By.XPATH, f"(//div[contains(@class, 'section_polls_row')])[{i+1}]/div")

        print(f"elements_in_row:  {len(elements_in_row)}")
    except NoSuchElementException as e:
        print("Nie znaleziono elementów:", e)
    for j, next_element in enumerate(elements_in_row):
        try:
            # Sprawdź, czy istnieje element o indeksie j+1
            if j < len(elements_in_row):
                next_element = elements_in_row[j]
                next_element_class = next_element.get_attribute('class')
                if next_element_class:
                    lista_elementow.append(next_element_class)
                    print(f"Klasa elementu o indeksie {j+1}: {next_element_class}")
                else:
                    print(f"Element o indeksie {j} nie ma przypisanej klasy.")
            else:
                print(f"Nie ma elementu o indeksie {j}")
                break
        except NoSuchElementException as e:
            print("Nie znaleziono elementów:", e)
    return lista_elementow

'''

