import requests
from urllib.parse import urlencode

def get_json_text(next_behot_time):

    behot_str = '_behot_time'
    if next_behot_time == 0:
        behot_str = 'min' + behot_str
    else:
        behot_str = 'max' + behot_str
    
    params = {
        behot_str : next_behot_time,
        'category' : '__all__',
        'utm_source' : 'toutiao',
        'widen' : 1,
        'tadrequire' : 'true',
        }
    
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'x-requested-with' : 'XMLHttpRequest'
        }
    
    url = 'https://www.toutiao.com/api/pc/feed/?' + urlencode(params)
    
    try:
        response = requests.get(url, headers = headers)
        response.raise_for_status();
        return response.json()
    except requests.HTTPError:
        print('Error! Status code: {}'.format(response.status_code))
        return None


def get_info(json):
    if (json.get('data')):
        for item in json.get('data'):
            yield {
               'title' : item.get('abstract'),
               'type' : item.get('article_genre'),
               'comments' : item.get('comments_count')
                }

def main():
    now_behot_time = 0;
    for requests_counter in range(10):
        json = get_json_text(now_behot_time)
        for item in get_info(json):
            print('{}\ntitle: {}\ntype: {}\ncomments: {}\n'.format('=' * 20, item['title'], item['type'], item['comments']))
        now_behot = json.get('next').get('max_behot_time')

if __name__ == '__main__':
    main()