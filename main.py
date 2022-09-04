# TODO:
# Multiple paragraphs inside div.comment
# Store all comments
# Go to all pages
# Paginate to other pages in same page utnil span.current is not equal to current page anymore

import requests
from bs4 import BeautifulSoup
import datetime
import re

class Comment:
    recent_post_regex = re.compile('^\d+ ?(secs?|mins?) ago$')

    def __init__(self, author, content, date_time, date_time_text, page_url, page_number):
        self.author = author
        self.content = content
        self.date_time = date_time
        self.date_time_text = date_time_text
        self.page_url = page_url
        self.page_number = page_number
        
    def is_recent(self):
        return bool(self.recent_post_regex.match(self.date_time_text))
        
    def equals(self, other):
        return self.author == other.author and self.content == other.content and self.date_time == other.date_time and self.page_url == other.page_url
        
    def __str__(self):
        time_diff_min = round((datetime.datetime.utcnow() - self.date_time).total_seconds() / 60.0)
        minute_word = "minute" + ("" if time_diff_min == 1 else "s")
        
        return f"New comment from {self.author} posted {time_diff_min} {minute_word} ago:\n\n" + self.content + f"\n\nReply here: {self.page_url}/page/{self.page_number}#comments"


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
                content = comment.find('p').text.strip()
                
                time_element = comment.find('time')
                
                date_time = time_element['datetime']
                
                if len(date_time) == 10:
                    date_time_obj = datetime.datetime.strptime(date_time, '%Y-%m-%d')
                else:
                    date_time = date_time[:len(date_time) - 6]
                    date_time_obj = datetime.datetime.strptime(date_time, '%Y-%m-%dT%H:%M:%S')
                
                new_comment = Comment(author, content, date_time_obj, time_element.text, url, page_number)
                
                if new_comment.is_recent():
                    comments.append(new_comment)
                
                print(new_comment)
                print(time_element.text)
                print(new_comment.is_recent())
                
            page_number += 1
    except Exception as e:
        print(f"Could not retrieve comments from {url}: {str(e)}")
    


if __name__ == "__main__":
    start()