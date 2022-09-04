import re
import datetime

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
        
    def __eq__(self, other):
        return self.author == other.author and self.content == other.content and self.date_time == other.date_time and self.page_url == other.page_url
        
    def __str__(self):
        time_diff_min = round((datetime.datetime.utcnow() - self.date_time).total_seconds() / 60.0)
        minute_word = "minute" + ("" if time_diff_min == 1 else "s")
        
        return f"New comment from {self.author} posted {time_diff_min} {minute_word} ago:\n\n" + self.content + f"Reply here: {self.page_url}/page/{self.page_number}#comments"
