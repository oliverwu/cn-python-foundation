import requests
import csv

import bs4
import expanddouban
"""
return a string corresponding to the URL of douban movie lists given category and location.
"""
def getMovieUrl(category, location):
	url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{},{}".format(category,location)
	return url
print(getMovieUrl("剧情","美国"))

# response = requests.get(url)
# html = response.text
# print(expanddouban.getHtml(getMovieUrl("剧情","美国")))

"""
url: the douban page we will get html from
loadmore: whether or not click load more on the bottom
waittime: seconds the broswer will wait after intial load and
"""
def getHtml(url, loadmore = True, waittime = 2):
    browser = webdriver.Chrome('chromedriver')
    browser.get(url)
    time.sleep(waittime)
    if loadmore:
        while True:
            try:
                next_button = browser.find_element_by_class_name("more")
                next_button.click()
                time.sleep(waittime)
            except:
                break
    html = browser.page_source
    browser.quit()
    return html



def getMovies(category, location):
    url = getMovieUrl(category, location)
    html = expanddouban.getHtml(url, True)
    soup = bs4.BeautifulSoup(html, "html.parser")
    content_div = soup.find("div",class_="list-wp")
    movie_name = []
    for element in content_div.find_all("a", recursive=False):
        if element.p.span:
            movie_name.append(element.p.span.get_text())
    return movie_name

# print(getMovies("剧情","美国"))

# def getLocations(category):
#     url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{}".format(category)
#     html = expanddouban.getHtml(url)
#     soup = bs4.BeautifulSoup(html, "html.parser")
# 	locations = []
#     content_ul = soup.find("div",class_="tags").ul.find_next_sibling("ul").find_next_sibling("ul")
#     for child in content_ul.children:
#         print(child.span.get_text())
# 		locations.append(child.span.get_text())
# 		print(locations)
#     # content_ul = soup.find_all("ul",class_="category")
#     # for ul in content_div:
#     # 	if ul.li.span.get_text() == "全部地区":
#     #     	for li in ul:
# 	# 			print(li.span.get_text())
#     #         	print(li.span.get_text())
#     # print(content_div)
#
# print(getLocations("剧情"))

class Movie(object):
	"""docstring forMovie."""
	def __init__(self, name, rate, location, category, info_link, cover_link):
		# superMovie, self).__init__()
		self.name = name
		self.rate = rate
		self.location = location
		self.category = category
		self.info_link = info_link
		self.cover_link = cover_link
m = Movie("肖申克的救赎","9.6","美国","剧情","https://movie.douban.com/subject/1292052/","https://img3.doubanio.com/view/movie_poster_cover/lpst/public/p480747492.jpg")


def getLocations(category):
	url = "https://movie.douban.com/tag/#/?sort=S&range=9,10&tags=电影,{}".format(category)
	html = expanddouban.getHtml(url)
	soup = bs4.BeautifulSoup(html,"html.parser")
	locations = []
	content_ul = soup.find("div",class_="tags").ul.find_next_sibling("ul").find_next_sibling("ul")
	for child in content_ul.children:
		locations.append(child.span.get_text())
		# print(locations)
	return locations[1:]
# print(getLocations("剧情"))

# locations = getLocations("剧情")
my_favorite_categories = ["科幻","动作","青春"]
num_movies = 0


# def getMoviesDetail(category, location):
# 	url = getMovieUrl(category, location)
# 	html = expanddouban.getHtml(url, True)
# 	soup = bs4.BeautifulSoup(html, "html.parser")
# 	content_div = soup.find("div",class_="list-wp")
# 	for element in content_div.find_all("a", recursive=False):
# 		if element.p.span:
# 			name = element.p.span.get_text()
# 			rate = element.p.span.find_next_sibling("span").get_text()
# 			info_link = element.get('href')
# 			cover_link = element.img.get('src')
#
# 			createVar = locals()
# 			createVar['info'+'2'] = Movie(name, rate, location, category, info_link, cover_link)
# 			print(info2.rate)
# 			# num_movies += 1
# 	return






def myFavoriteMovies(categories):
	num_movies = 0
	name_movies = []
	for category in categories:
		for location in getLocations(category):
			url = getMovieUrl(category,location)
			html = expanddouban.getHtml(url, True)
			soup = bs4.BeautifulSoup(html, "html.parser")
			content_div = soup.find("div",class_="list-wp")
			for element in content_div.find_all("a", recursive=False):
				if element.p.span:
					name = element.p.span.get_text()
					rate = element.p.span.find_next_sibling("span").get_text()
					info_link = element.get('href')
					cover_link = element.img.get('src')
					if name not in name_movies:
						name_movies.append(name)
						createVar = locals()
						createVar['movie'+str(num_movies)] = Movie(name, rate, location, category, info_link, cover_link)
						# print(createVar['movie'+'num_movies'].name)
						num_movies += 1
	with open('movies.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, dialect='excel')
		# spamwriter = csv.writer(csvfile, delimiter=' ',quotechar=',', quoting=csv.QUOTE_MINIMAL)
		for num in range(len(name_movies)):
			spamwriter.writerow([createVar['movie'+str(num)].name, createVar['movie'+str(num)].rate, createVar['movie'+str(num)].location, createVar['movie'+str(num)].category, createVar['movie'+str(num)].info_link, createVar['movie'+str(num)].cover_link])
			print(num)


# print(getMoviesDetail("剧情","美国"))
print(myFavoriteMovies(my_favorite_categories))
