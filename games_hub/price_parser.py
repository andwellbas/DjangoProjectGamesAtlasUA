from bs4 import BeautifulSoup
from lxml import html
import requests


game_not_found = "Ціну не знайдено"


def get_steam_price(game_name: str):
    try:
        response = requests.get(f"https://store.steampowered.com/search/?term={game_name}&category1=998")
        soup = BeautifulSoup(response.content, 'html.parser')
        game_url = soup.find("a", {"class": "search_result_row"})["href"]
        response = requests.get(game_url)
        tree = html.fromstring(response.content)

        game_price = tree.xpath('//div[@class="game_area_purchase_game_wrapper"]//div[@class="game_purchase_price '
                                'price"]//text()')
        discount_price = tree.xpath('//div[@class="game_area_purchase_game_wrapper"]//div['
                                    '@class="discount_final_price"]//text()')

        if game_price and not discount_price:
            return game_price[0].strip(), game_url
        elif discount_price:
            return discount_price[0].strip(), game_url
        else:
            return game_not_found, "https://store.steampowered.com/"

    except TypeError:
        return game_not_found, "https://store.steampowered.com/"

    except Exception as e:
        # Error handling if the query fails or no data is available
        return "", ""


def get_games_planet_price(game_name: str):
    try:
        url = f"https://us.gamesplanet.com/search?query={game_name.replace(' ', '+')}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        try:
            game_link = soup.find("a", class_="d-block text-decoration-none stretched-link")["href"]
        except TypeError:
            pass

        try:
            return soup.find("span", class_="price_current").text.split("$")[1]+"$", game_link

        except TypeError:
            return game_not_found, ""

    except Exception as e:
        # Error handling if the query fails or no data is available
        return "", ""


def get_games_yu_play_price(game_name):
    try:
        url = f"https://www.yuplay.com/products/?search={game_name.replace(' ', '+')}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        try:
            game = soup.find("span", class_="catalog-item-sale-price").text
            game_link = soup.find("a", class_="catalog-image-ratio-container")["href"]
            print(game_link)

            return game, game_link
        except AttributeError:
            return game_not_found, ""

    except Exception as e:
        # Error handling if the query fails or no data is available
        return "", ""


def get_win_game_store_price(game_name: str):
    try:
        url = f"https://www.wingamestore.com/search/?SearchWord={game_name.replace(' ', '+')}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        game = soup.find("span", class_="price").text.replace("$", "") + "$"
        try:
            game_link = soup.find("a", class_="overclick nocolor")["href"]
        except TypeError or UnboundLocalError:
            game_link = "https://www.wingamestore.com/"
        if len(game) < 10:
            return game, game_link
        else:
            return game_not_found, game_link

    except Exception as e:
        # Error handling if the query fails or no data is available
        return "", ""


def get_noctre_price(game_name: str):
    try:
        url = f"https://www.noctre.com/search?s={game_name.replace(' ', '+')}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        game = soup.find("div", class_="font-weight-medium-bold text-white").text
        game_link = soup.find("a", class_="h-100")["href"]

        return game.replace("$", "") + "$", game_link

    except AttributeError:
        return game_not_found, ""

    except Exception as e:
        # Error handling if the query fails or no data is available
        return "", ""


def get_all_key_shop_price(game_name: str):
    try:
        url = f"https://www.allkeyshop.com/blog/en-us/catalogue/search-{game_name.replace(' ', '+')}"
        r = requests.get(url)
        soup = BeautifulSoup(r.text, "lxml")
        game = soup.find("div", class_="search-results-row-price").text\
                   .replace(" ", "").replace("$", "").replace("\n", '') + "$"
        game_link = soup.find("a", class_="search-results-row-link")["href"]

        return game, game_link

    except AttributeError:
        return game_not_found, "https://www.allkeyshop.com/blog/"

    except Exception as e:
        # Error handling if the query fails or no data is available
        return "", ""
