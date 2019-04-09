import requests
from urllib.parse import urlencode
from bs4 import BeautifulSoup

def get_page(url, is_binary = False, headers = {'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36'}, session = None):
    print('[Function get_page()]');

    try:
        print('Requesting... URL = {}'.format(url));
        if session != None:
            response = session.get(url, headers = headers, timeout = 10)
        else:
            response = requests.get(url, headers = headers, timeout = 10)
        response.raise_for_status()
        print('Successfully requested!');
        if is_binary:
            print('Content type: binary');
            return response.content
        else:
            print('Content type: text');
            response.encoding = 'utf-8'
            return response.text
    except requests.HTTPError:
        print('[Error] requests.HTTPError: response.status.code = {}'.format(response.status_code))
        return None
    except requests.Timeout:
        print('[Error] requests.Timeout');
        return None
    except requests.exceptions.MissingSchema:
        print('[Error] requests.exception.MissingSchema: Please check the format of the URL.')
        return None
        
def image_download(url, path = 'C:/Users/Editor/Desktop/TempCode/temp/'):
    print('[Function image_download()]')

    name = url.split('/')[-1]
    if (name.split['.'][-1] != 'jpg'): 
        name = name + '.jpg'

    print('Downloading...')
    with open(path + name, 'wb') as f:
        f.write(get_page(url, True))
    print('Successfully downloaded!')

def get_image_url(html):
    s = BeautifulSoup(html, 'html.parser')
    image_pages = s.body.select_one('div#wrapper div#imgContainer div#imgid').select('div.imgpage')
    for page in image_pages:
        image_items = page.ul.select('li.imgitem')
        for item in image_items:
            yield item.attrs['data-objurl']

def build_BaiduImage_url(keyword):
    url = 'https://image.baidu.com/search/index?'
    params = {
        'tn' : 'baiduimage',
        'word' : keyword
    }
    return url + urlencode(params)

def ajax_BaiduImage(keyword, pn = 30, session = None):
    params = {
        'tn' : 'resultjson_com',
        'fp' : 'result',
        'queryWord' : keyword,
        'word' : keyword,
        'pn' : 60,
        'rn' : 30
    }
    headers = {
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        'X-Requested-With' : 'XMLHttpRequest'
    }
    xhr_url = 'https://image.baidu.com/search/acjson?' + urlencode(params)
    return get_page(xhr_url, headers = headers, session = session)

def main():

    headers_standard = {
        'Accept' : 'text/html,application/xhtml+xml,application/xml;q=0.9,image/webp,image/apng,*/*;q=0.8',
        'Accept-Encoding' : 'gzip, deflate, br',
        'Cache-Control' : 'max-age=0',
        'Accept-Language' : 'zh-CN,zh;q=0.9',
        'Connection' : 'keep-alive',
        'Cookie': 'BDqhfp=%E5%9B%BD%E5%AE%B6%E5%9C%B0%E7%90%86%26%260-10-1undefined%26%260%26%261; BIDUPSID=2C7F3C227634DA2D75F699203184C856; PSTM=1546426688; BAIDUID=65CFC98D7AE6C1B01E8FA6E0571901C3:FG=1; Hm_lvt_bfc6c23974fbad0bbfed25f88a973fb0=1549686534,1549688779,1549689168; BDORZ=B490B5EBF6F3CD402E515D22BCDA1598; BDUSS=HR3TTdRWFNsZFpnTXBtaW01MkFjV2VlZ1g0eVBsZGxNbWE0N3FjY0EwNnoxYnBjQVFBQUFBJCQAAAAAAAAAAAEAAAAbpkoJY2NkZGhoaAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAAALNIk1yzSJNcc; H_PS_PSSID=1445_21119_18560_28720_28557_28697_28584_28603_28606; BDRCVFR[X_XKQks0S63]=mk3SLVN4HKm; userFrom=null; BDRCVFR[-pGxjrCMryR]=mk3SLVN4HKm; firstShowTip=1; indexPageSugList=%5B%22%E5%9B%BD%E5%AE%B6%E5%9C%B0%E7%90%86%22%2C%22%E6%88%98%E5%9C%B04%22%2C%22%E4%BD%BF%E5%91%BD%E5%8F%AC%E5%94%A46%22%2C%22%E4%BD%BF%E5%91%BD%E5%8F%AC%E5%94%A42%22%2C%22cheytac%22%2C%22intervention%22%2C%22%E5%AF%B9%E6%95%B0%E5%9B%9E%E5%BD%92%E5%85%AC%E5%BC%8F%22%2C%22permission%22%2C%22%E6%8C%87%E6%95%B0%E5%9B%9E%E5%BD%92%E6%96%B9%E7%A8%8B%E5%85%AC%E5%BC%8F%22%5D; cleanHistoryStatus=0; BDRCVFR[dG2JNJb_ajR]=mk3SLVN4HKm',
        'Host' : 'image.baidu.com',
        'Referer' : 'https://image.baidu.com/',
        'Upgrade-Insecure-Requests' : '1',
        'User-Agent' : 'Mozilla/5.0 (Windows NT 10.0; Win64; x64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/72.0.3626.121 Safari/537.36',
        }

    session_BaiduImage = requests.Session();

    keyword = input('Input the keyword:')

    url = build_BaiduImage_url(keyword)
    html_initial = get_page(url, session = session_BaiduImage)

    times = 3
    for i in range(1, times + 1):
        ajax_BaiduImage(keyword, 30 * i, session_BaiduImage)

    html = get_page(url, session = session_BaiduImage)
    for url_item in get_image_url(html_initial):
        image_download(url_item)

main()
    
    