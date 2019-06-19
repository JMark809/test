
import requests
import bs4
import re


def open_url(url):
    headers = {'user-agent':'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/74.0.3729.131 Safari/537.36'}
    res = requests.get(url,headers=headers)
    return res


def find_movies(res):
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    #movies'names
    movies = []
    targets = soup.find_all('div', class_='hd')
    for each in targets:
        movies.append(each.a.span.text)

    #ranks
    ranks = []
    targets = soup.find_all('span', class_='rating_num')
    for each in targets:
        ranks.append('the rank is %s' % each.text)

    #informations
    informations = []
    targets = soup.find_all('div', class_='bd')
    for each in targets:
        try:
            informations.append(each.p.text.split('\n')[1].strip()+each.p.text.split('\n')[2].strip())
        except:
            continue

    result = []
    length = len(movies)
    for i in range(length):
        result .append (movies[i]+ranks[i]+informations[i]+'\n')
    return result


def find_depth(res):
    soup = bs4.BeautifulSoup(res.text, 'html.parser')
    depth = soup.find('span', class_='next').previous_sibling.previous_sibling.text
    return int(depth)


def main():
    host = 'https://movie.douban.com/top250'
    res = open_url(host)
    depth = find_depth(res)

    result = []
    for i in range(depth):
        url = host+'/?start='+str(25*i)
        res = open_url(url)
        result.extend(find_movies(res))

    with open('doubanTOP250movies.txt', 'w', encoding='utf-8') as file:
        for each in result:
            file.write(each)


if __name__ == '__main__':
    main()






