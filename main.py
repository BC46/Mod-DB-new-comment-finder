# TODO:
# Use sessions https://python.plainenglish.io/send-http-requests-as-fast-as-possible-in-python-304134d46604
# Remove print statements
# Resolve in-code todos
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
        
        print(page_url + "/page/" + str(page_number))
        
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
            
            # TODO: change True to new_comment.is_recent()
            if True and not helpers.has_comment_already_been_saved(comments, new_comment):
                comments.append(new_comment)
            
        page_number += 1

def start():
    comments = []
    previous_comments = []

    urls = [
        "https://www.moddb.com/mods/freelancer-hd-edition/downloads/freelancer-hd-edition-v06",
        "https://www.moddb.com/mods/freelancer-hd-edition/downloads/freelancer-hd-edition-05"
    ]

    try:
        for url in urls:
            find_comments_in_page(comments, url)
    except Exception as e:
        print(f"Could not retrieve comments from {url}: {str(e)}")
    
    for comment in comments:
        if not helpers.has_comment_already_been_saved(previous_comments, comment):
            print(comment)
    
    previous_comments = comments
    


if __name__ == "__main__":
    start()