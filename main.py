import pandas as pd
import requests
from bs4 import BeautifulSoup


def give_list(attribute, is_rating, is_title):
    text_list = []
    color = []
    if is_rating:
        for element in attribute:
            text_list.append(element.text.split()[0])
    elif is_title:
        for element in attribute:
            title = element.text
            texts = title.split('(')
            name = texts[0]
            color_text = texts[1].split(',')[0]
            text_list.append(name)
            color.append(color_text)
        return text_list, color
    else:
        for element in attribute:
            text_list.append(element.text)
    return text_list

def scrape_flipkart(search_query):
    base_url = "https://www.flipkart.com/search?q="
    search_query = search_query.replace(' ', '%20')
    url = base_url + search_query

    # Send a GET request to the URL
    response = requests.get(url)

    # Check if the request was successful (status code 200)
    if response.status_code == 200:
        # Parse the HTML content of the page

        soup = BeautifulSoup(response.text, 'html.parser')

        # Extracting search Info
        names, color = give_list(soup.find_all('div', {'class': '_4rR01T'}), False, True)
        ratings = give_list(soup.find_all('span', {'class': '_1lRcqv'}), False, False)
        no_ratings = give_list(soup.find_all('span', {'class': '_2_R_DZ'}), True, False)
        features = soup.find_all('ul', {'class': '_1xgFaf'})
        prices = give_list(soup.find_all('div', {'class': '_30jeq3 _1_WHN1'}),False, False)

        ROM = []
        Display = []
        back_camera = []
        front_camera = []
        # feature Extraction
        for feature in features:
            rom = feature.findNext()
            ROM.append(rom.text)
            display = rom.findNext()
            Display.append(display.text)
            camera = display.findNext()
            camera_text_list = camera.text.split('|')
            back_camera.append(camera_text_list[0])
            front_camera.append(camera_text_list[1].split()[0])
        content = {
            'Name' : names,
            'Color' : color,
            'Rating' : ratings,
            'No of Rating' : no_ratings,
            'ROM' : ROM,
            'Display' : Display,
            'Back Camera' : back_camera,
            'Front Camera' : front_camera,
            'Price' : prices
        }

        df = pd.DataFrame(content)
        df.to_csv('phones_data.csv', index=False)
    else:
        print("Failed to retrieve the page. Status code:", response.status_code)



# Example usage
search_query = "iPhone"
scrape_flipkart(search_query)

