# TODO:
# Use sessions https://python.plainenglish.io/send-http-requests-as-fast-as-possible-in-python-304134d46604
# Perform task every 45 minutes

import requests
from bs4 import BeautifulSoup

from comment import Comment
import helpers

def save_comment(comment_element, page_url, page_number):
    author = comment_element.find('a', class_='author').text
    content = helpers.get_content_from_comment(comment_element)
    time_element = comment_element.find('time')
    date_time_obj = helpers.get_date_time_obj(time_element['datetime'])
    
    return Comment(author, content, date_time_obj, time_element.text, page_url, page_number)

def find_comments_in_page(comments, page_url):
    page_number = 1
    
    on_last_page = False
    while not on_last_page:
        page = requests.get(page_url + "/page/" + str(page_number))
        soup = BeautifulSoup(page.content, "html.parser")
        
        current_page_element = soup.find('span', class_='current')
        
        # This page doesn't have a "next" page
        if not current_page_element:
            on_last_page = True
        else:
            # All comments already checked
            if page_number > int(current_page_element.text):
                break

        comments_container = soup.find('div', class_='table tablecomments')
        
        # Page has no comment section
        if not comments_container:
            break

        for comment in comments_container.find_all('div', class_='content'):
            new_comment = save_comment(comment, page_url, page_number)

            if new_comment.is_recent() and not helpers.has_comment_already_been_saved(comments, new_comment):
                comments.append(new_comment)
            
        page_number += 1
        
def reset_lists(comments, previous_comments):
    previous_comments = []
    
    for comment in comments:
        previous_comments.append(comment)
    
    comments = []

def start():
    comments = []
    previous_comments = []

    urls = [
        "https://www.moddb.com/mods/freelancer-hd-edition",
        "https://www.moddb.com/mods/freelancer-hd-edition/downloads/freelancer-hd-edition-v06",
        "https://www.moddb.com/mods/freelancer-hd-edition/downloads/freelancer-hd-edition-05",
        "https://www.moddb.com/mods/freelancer-hd-edition/downloads/freelancer-hd-edition-041",
        "https://www.moddb.com/mods/freelancer-hd-edition/news/freelancer-hd-edition-version-06-released",
        "https://www.moddb.com/mods/freelancer-hd-edition/news/freelancer-hd-edition-05-released",
        "https://www.moddb.com/mods/freelancer-hd-edition/news/freelancer-hd-edition-released",
        "https://www.moddb.com/mods/freelancer-hd-edition/news/freelancer-hd-edition-discord-server",
        
        "https://www.moddb.com/games/freelancer/addons/freelancer-hd-character-models",
        "https://www.moddb.com/games/freelancer/addons/freelancer-hd-icons-and-hud-backgrounds",
        "https://www.moddb.com/games/freelancer/addons/freelancer-hd-base-interiors-and-planetscapes",
        "https://www.moddb.com/games/freelancer/downloads/freelancer-maximized-draw-distances",
        "https://www.moddb.com/games/freelancer/downloads/freelancer-text-strings-revision",
        "https://www.moddb.com/games/freelancer/downloads/freelancer-broken-interior-lighting-fix",
    ]

    try:
        for url in urls:
            find_comments_in_page(comments, url)
    except Exception as e:
        print(f"Could not retrieve comments from {url}: {str(e)}")
    
    for comment in comments:
        # Only print comments that haven't been printed the previous time. This prevents comments from being printed twice.
        if not helpers.has_comment_already_been_saved(previous_comments, comment):
            print(comment)
    
    reset_lists(previous_comments, comments)
    


if __name__ == "__main__":
    start()