import datetime

def has_comment_already_been_saved(saved_comments, comment):
    for saved_comment in saved_comments:
        if saved_comment == comment:
            return True
    return False


def get_content_from_comment(comment):
    content = ''
    for paragraph in comment.find_all('p'):
        content += paragraph.text.strip() + '\n\n'
        
    return content


def get_date_time_obj(datetime_element):
    if len(datetime_element) == 10:
        date_time_obj = datetime.datetime.strptime(datetime_element, '%Y-%m-%d')
    else:
        datetime_element = datetime_element[:len(datetime_element) - 6]
        date_time_obj = datetime.datetime.strptime(datetime_element, '%Y-%m-%dT%H:%M:%S')
        
    return date_time_obj
