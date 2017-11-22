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
	return locations[1:]

my_favorite_categories = ["科幻","动作","青春"]
num_movies = 0


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
						num_movies += 1
	with open('movies.csv', 'w', newline='') as csvfile:
		spamwriter = csv.writer(csvfile, dialect='excel')
		for num in range(len(name_movies)):
			spamwriter.writerow([createVar['movie'+str(num)].name, createVar['movie'+str(num)].rate, createVar['movie'+str(num)].location, createVar['movie'+str(num)].category, createVar['movie'+str(num)].info_link, createVar['movie'+str(num)].cover_link])
			print(num)


with open('movies.csv', 'r') as f:
    reader = csv.reader(f)
    movies = list(reader)


def count_num_of_category(movies,category):
	createVar = locals()
	createVar['num_'+str(category)] = 0

	for movie in movies:
		if movie[3] == category:
			createVar['num_'+str(category)] += 1

	return createVar['num_'+str(category)]


def count_num_of_category_location(movies,category,location):
	createVar = locals()
	createVar['num_'+str(category)+str(location)] = 0

	for movie in movies:
		if movie[3] == category and movie[2] == location:
			createVar['num_'+str(category)+str(location)] += 1

	return createVar['num_'+str(category)+str(location)]


results_for_output = []
def find_topthree_locations(movies,category):
	locations = getLocations(category)
	location_dict = {}
	num_list = []
	num = 0

	for location in locations:
		num = count_num_of_category_location(movies,category,location)
		num_list.append(num)

	num_list = sorted(num_list)

	for location in locations:
		num = count_num_of_category_location(movies,category,location)
		location_dict[location] = num

	return sorted(location_dict,key=lambda x:location_dict[x])[-1], sorted(location_dict,key=lambda x:location_dict[x])[-2], sorted(location_dict,key=lambda x:location_dict[x])[-3]


def find_topthree_locations_in_my_favorite_categories(movies,categories):
	for category in categories:
		createVar = locals()
		createVar["top_three_in_"+str(category)] = find_topthree_locations(movies,category)
		print("在{}类电影中，数量排名前三的地区分别为{}、{}、{}。".format(category,createVar["top_three_in_"+str(category)][0],createVar["top_three_in_"+str(category)][1],createVar["top_three_in_"+str(category)][2]))


def count_percentage(movies,category):
	locations = getLocations(category)
	createVar = locals()
	top_three_locations = []

	createVar["top_three_in_"+str(category)] = find_topthree_locations(movies,category)
	for n in range(3):
		top_three_locations.append(createVar["top_three_in_"+str(category)][n])

	results_for_output.append("在{}类电影中，数量排名前三的地区分别为{}、{}、{}。".format(category,top_three_locations[0],top_three_locations[1],top_three_locations[2]))

	for loca in top_three_locations:
		num_loca = count_num_of_category_location(movies,category,loca)
		num_cate = count_num_of_category(movies,category)
		percentage = float(num_loca/num_cate)
		percentage = round(percentage,2)*100
		results_for_output.append("{}占{}类别的电影的百分比为{}%。".format(loca,category,percentage))


def count_all_percentages(movies,categories):
	for category in categories:
		 count_percentage(movies,category)

count_all_percentages(movies,my_favorite_categories)

f = open("output.txt",'w')
for n in range(len(results_for_output)):
	f.write(results_for_output[n])
	f.write('\n')

f.close()












# print(most_popular_locations(movies))
