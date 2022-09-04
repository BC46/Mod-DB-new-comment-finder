# TODO:
# Use sessions https://python.plainenglish.io/send-http-requests-as-fast-as-possible-in-python-304134d46604
# Cleanup
# Remove print statements
# Go to all pages
# Perform task every 45 minutes

import requests
from bs4 import BeautifulSoup

from comment import Comment
import helpers

def start():
    comments = []

    #url = "https://www.moddb.com/mods/freelancer-hd-edition/downloads/freelancer-hd-edition-v06"

    try:
        url = "https://www.moddb.com/mods/freelancer-hd-edition"

        page_number = 1
        
        while True:
            page = requests.get(url + "/page/" + str(page_number))

            soup = BeautifulSoup(page.content, "html.parser")
            
            print(page_number)
            actual_page_number = int(soup.find('span', class_='current').text)
            
            if page_number > actual_page_number:
                break

            comments_container = soup.find('div', class_='table tablecomments')

            for comment in comments_container.find_all('div', class_='content'):
                author = comment.find('a', class_='author').text
                content = helpers.get_content_from_comment(comment)
                time_element = comment.find('time')
                date_time_obj = helpers.get_date_time_obj(time_element['datetime'])
                
                new_comment = Comment(author, content, date_time_obj, time_element.text, url, page_number)
                
                if True and not helpers.has_comment_already_been_saved(comments, new_comment):
                    comments.append(new_comment)
                
                print(new_comment.is_recent())
                
            page_number += 1
    except Exception as e:
        print(f"Could not retrieve comments from {url}: {str(e)}")
        
    print(len(comments))
    


if __name__ == "__main__":
    start()