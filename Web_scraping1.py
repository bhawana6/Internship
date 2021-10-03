#!/usr/bin/env python
# coding: utf-8

# # Importing Librarires

# In[4]:


import pandas as pd
import requests
from bs4 import BeautifulSoup


# # Write a python program to display all the header tags from ‘en.wikipedia.org/wiki/Main_Page’

# In[5]:


def wiki_scrap (url):
    page = requests.get(url)
    print(url)
    soup = BeautifulSoup(page.content)
    title = soup.find_all(['h1','h2','h3','h4','h5'])
    title_h =[]
    for i in title :
        print('Heading',title.index(i))
        print('_____________________________')
        print(i.text)


# In[6]:


url = "http://en.wikipedia.org/wiki/Main_Page"
headings = wiki_scrap(url)
print(headings)


# # Write a python program to display IMDB’s Top rated 100 movies’ data (i.e. Name, IMDB rating, Year of release) and make data frame

# In[8]:


def imdb_hollywood(url):
    html = url
    page = requests.get(html)
    print('Responce received',page)
    soup = BeautifulSoup(page.content)
    mov_lst = soup.find_all('div',class_ ='lister-item mode-detail')
    print('Scrapping Completed')
    movie =[]
    year =[]
    rate = []
    for i in mov_lst :
        movie.append(i.h3.a.text)
        year.append(i.h3.find('span',class_='lister-item-year text-muted unbold').text)
        rate.append(i.find('span',class_ ='ipl-rating-star__rating').text)
    IMDB_hollywood= pd.DataFrame({})
    IMDB_hollywood['Name']=movie
    IMDB_hollywood['IMDB rating']=rate
    IMDB_hollywood['Year of release']=year
    return IMDB_hollywood


# In[35]:


## Calling Function
print('lets find the list of best hollowood movies in IMDB')
url ='https://www.imdb.com/list/ls091520106/'
list_movie = imdb_hollywood(url)
list_movie


# # Write a python program to display IMDB’s Top rated 100 Indian movies’ data (i.e. Name, IMDB rating, Year of release) and make data frame.

# In[10]:


def imdb_bollywood(url):
    html = url
    page = requests.get(html)
    print('Responce received',page)
    soup = BeautifulSoup(page.content)
    mov_lst = soup.find_all('div',class_ ='lister-item mode-detail')
    print('Scrapping Completed')
    movie =[]
    year =[]
    rate = []
    for i in mov_lst :
        movie.append(i.h3.a.text)
        year.append(i.h3.find('span',class_='lister-item-year text-muted unbold').text)
        rate.append(i.find('span',class_ ='ipl-rating-star__rating').text)
    IMDB_bollywood= pd.DataFrame({})
    IMDB_bollywood['Name']=movie
    IMDB_bollywood['IMDB rating']=rate
    IMDB_bollywood['Year of release']=year
    return IMDB_bollywood


# In[ ]:


##FUNCTION CALLING 
print('lets find the list of best Hindi movies in IMDB')
url ="https://www.imdb.com/list/ls009997493/"
html = imdb_bollywood(url)
html


# # Write a python program to scrap book name, author name, genre and book review of any 5 books from

# In[11]:


def book_review(url) :
    page= requests.get(url)
    print (page)
    soup = BeautifulSoup(page.content)
    print ('Web Scrapping completed')
    book_lst = soup.find_all('div',class_ ='row-fluid article-row')
    Book_name= []
    Author_name= []
    Genre= []
    Review = []
    for  b in book_lst :
        Book_name.append(b.h4.a.text.strip())
        Author_name.append(b.p.text.strip())
        Review.append(b.find('p',class_="excerpt").text.strip()) 
        genre_part = b.find('p',class_='genre-links hidden-phone')
        genre_all =genre_part.findChildren("a" , recursive=False)
        k = 'Genre :'
        for i in genre_all:
            k = k + i.text +' '
        Genre.append(k)
        if len(Book_name)>4 :
            break
        
    Book_review =pd.DataFrame({})
    Book_review['Book_name'] =Book_name
    Book_review['Author_name']=Author_name
    Book_review['Genre'] =Genre
    Book_review['Review']=Review
    return Book_review


# In[12]:


print ('**** Books and Review ****')
url = 'https://bookpage.com/reviews'
review = book_review(url)
review


# # Write a python program to scrape cricket rankings from ‘www.icc-cricket.com’. You have to scrape:
# 
# 
# i) Top 10 ODI teams in men’s cricket along with the records for matches, points and rating.
# 
# 

# In[13]:


def men_team_rtgs(url):
    page =requests.get(url)
    print('Response received :',page)
    soup =BeautifulSoup(page.content)
    rank=[]
    country=[]
    matches =[]
    points =[]
    rating=[]
    others =[]
    best_team = soup.find_all('tr',class_="rankings-block__banner")
    for i in best_team :
        rnk =i.find('td',class_='rankings-block__banner--pos')
        rank.append(rnk.text)
        ctry = i.find('span',class_ ='u-hide-phablet')
        country.append(ctry.text.strip())
        mtch = i.find('td',class_ ='rankings-block__banner--matches')
        matches.append(mtch.text.strip())
        pts = i.find('td',class_ ='rankings-block__banner--points')
        points.append(pts.text.strip())
        rate = i.find('td',class_ ='rankings-block__banner--rating u-text-right')
        rating.append(rate.text.strip())
    team_odi = soup.find_all('tr',class_='table-body')
    for i in team_odi :
        rnk =i.find('td',class_='table-body__cell table-body__cell--position u-text-right')
        rank.append(rnk.text)
        ctry = i.find('span',class_ ='u-hide-phablet')
        country.append(ctry.text.strip())
        rate = i.find('td',class_ ='table-body__cell u-text-right rating')
        rating.append(rate.text.strip())
        other = i.find_all('td', class_="table-body__cell u-center-text")
        for j in other :
            others.append(j.text)
        if len(rating) == 10:
            break
    mtch = others[0::2]
    pnts = others[1::2]
    matches =matches.extend(mtch)
    points =points.extend(pnts)
    ODI_MEN_TEAM_RATINGS = pd.DataFrame([])
    ODI_MEN_TEAM_RATINGS["rank"] =rank
    ODI_MEN_TEAM_RATINGS["country"] =country
    ODI_MEN_TEAM_RATINGS["matches"] =matches
    ODI_MEN_TEAM_RATINGS["points"] =points
    ODI_MEN_TEAM_RATINGS["rating"] =rating
    return ODI_MEN_TEAM_RATINGS


# In[14]:


print('****** ICC TEAM RATING MEN ODI ')
url = 'https://www.icc-cricket.com/rankings/mens/team-rankings/odi'
ICC_MEN_ODI_TEAM_RANK= men_team_rtgs(url)
ICC_MEN_ODI_TEAM_RANK


# ii) Top 10 ODI Batsmen in men along with the records of their team and rating.
# 

# In[15]:


def icc_men_bat_odi(url) :
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    w_best_bat =  soup.find_all('tr',class_='rankings-block__banner')
    rank =[]
    name=[]
    country=[]
    points =[]
    for i in w_best_bat :
        rnk = i.find('td',class_ ='rankings-block__position')
        nme = i.find('div',class_ ='rankings-block__banner--name-large')
        ctr = i.find('div',class_ ='rankings-block__banner--nationality')
        pts = i.find('div',class_ ='rankings-block__banner--rating')
        rank.append(rnk.text.strip())
        name.append(nme.text.strip())
        country.append(ctr.text.strip())
        points.append(pts.text.strip())
    w_bat =  soup.find_all('tr',class_='table-body')
    for i in w_bat :
        rnk = i.find('td',class_ ='table-body__cell table-body__cell--position u-text-right')
        nme = i.find('a')
        ctr = i.find('span',class_ ='table-body__logo-text')
        pts = i.find('td',class_ ='table-body__cell rating')
        rank.append(rnk.text.strip())
        name.append(nme.text.strip())
        country.append(ctr.text.strip())
        points.append(pts.text.strip())
        if len(points) == 10:
            break
    ODI_MEN_ODI__BAT_Ratings = pd.DataFrame([])
    ODI_MEN_ODI__BAT_Ratings["Position"] =rank
    ODI_MEN_ODI__BAT_Ratings["Player Name"] =name
    ODI_MEN_ODI__BAT_Ratings["Team"] =country
    ODI_MEN_ODI__BAT_Ratings["Rating"] =points
    return ODI_MEN_ODI__BAT_Ratings


# In[ ]:


print('ODI BATESMEN RATING')
url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/batting"
rank =icc_men_bat_odi(url)
rank


# iii) Top 10 ODI bowlers along with the records of their team and rating.
# 

# In[16]:


def icc_men_bowl_odi(url) :
    
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    best_bowl= soup.find_all('tr',class_='rankings-block__banner')
    rank =[]
    name=[]
    country=[]
    points =[]
    for i in best_bowl :
        rnk = i.find('td',class_ ='rankings-block__position')
        nme = i.find('div',class_ ='rankings-block__banner--name-large')
        ctr = i.find('div',class_ ='rankings-block__banner--nationality')
        pts = i.find('div',class_ ='rankings-block__banner--rating')
        rank.append(rnk.text.strip())
        name.append(nme.text.strip())
        country.append(ctr.text.strip())
        points.append(pts.text.strip())
    bowl_odi = soup.find_all('tr',class_='table-body')
    for i in bowl_odi :
        rnk = i.find('td',class_ ='table-body__cell table-body__cell--position u-text-right')
        nme = i.find('a')
        ctr = i.find('span',class_ ='table-body__logo-text')
        pts = i.find('td',class_ ='table-body__cell rating')
        rank.append(rnk.text.strip())
        name.append(nme.text.strip())
        country.append(ctr.text.strip())
        points.append(pts.text.strip())
        if len(rank) == 10:
            break
    ODI_BOWLING_Ratings = pd.DataFrame([])
    ODI_BOWLING_Ratings["Position"] =rank
    ODI_BOWLING_Ratings["Player Name"] =name
    ODI_BOWLING_Ratings["Team"] =country
    ODI_BOWLING_Ratings["Rating"] =points
    return ODI_BOWLING_Ratings


# In[ ]:


print('ODI Bowler RATING')
url = "https://www.icc-cricket.com/rankings/mens/player-rankings/odi/bowling"
rank =icc_men_bowl_odi(url)
rank


# # Write a python program to scrape cricket rankings from ‘www.icc-cricket.com’. You have to scrape:
# 
# 
# i) Top 10 ODI teams in women’s cricket along with the records for matches, points and rating.
# 
# 

# In[17]:



def women_team_rtgs(url):
    page =requests.get(url)
    print('Response received :',page)
    soup =BeautifulSoup(page.content)
    rank=[]
    country=[]
    matches =[]
    points =[]
    rating=[]
    others =[]
    best_team = soup.find_all('tr',class_="rankings-block__banner")
    for i in best_team :
        rnk =i.find('td',class_='rankings-block__banner--pos')
        rank.append(rnk.text)
        ctry = i.find('span',class_ ='u-hide-phablet')
        country.append(ctry.text.strip())
        mtch = i.find('td',class_ ='rankings-block__banner--matches')
        matches.append(mtch.text.strip())
        pts = i.find('td',class_ ='rankings-block__banner--points')
        points.append(pts.text.strip())
        rate = i.find('td',class_ ='rankings-block__banner--rating u-text-right')
        rating.append(rate.text.strip())
    team_odi = soup.find_all('tr',class_='table-body')
    for i in team_odi :
        rnk =i.find('td',class_='table-body__cell table-body__cell--position u-text-right')
        rank.append(rnk.text)
        ctry = i.find('span',class_ ='u-hide-phablet')
        country.append(ctry.text.strip())
        rate = i.find('td',class_ ='table-body__cell u-text-right rating')
        rating.append(rate.text.strip())
        other = i.find_all('td', class_="table-body__cell u-center-text")
        for j in other :
            others.append(j.text)
        if len(rating) == 10:
            break
    mtch = others[0::2]
    pnts = others[1::2]
    matches =matches.extend(mtch)
    points =points.extend(pnts)
    ODI_WOMEN_TEAM_RATINGS = pd.DataFrame([])
    ODI_WOMEN_TEAM_RATINGS["rank"] =rank
    ODI_WOMEN_TEAM_RATINGS["country"] =country
    ODI_WOMEN_TEAM_RATINGS["matches"] =matches
    ODI_WOMEN_TEAM_RATINGS["points"] =points
    ODI_WOMEN_TEAM_RATINGS["rating"] =rating
    return ODI_WOMEN_TEAM_RATINGS


# In[ ]:


print('****** ICC TEAM RATING WOMEN ODI ')
url = 'https://www.icc-cricket.com/rankings/womens/team-rankings/odi'
ICC_WOMEN_ODI_TEAM_RANK= women_team_rtgs(url)
ICC_WOMEN_ODI_TEAM_RANK


# # ii) Top 10 women’s ODI players along with the records of their team and rating.
# 

# In[ ]:


def w_odi_bat(url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    w_best_bat =  soup.find_all('tr',class_='rankings-block__banner')
    rank =[]
    name=[]
    country=[]
    points =[]
    for i in w_best_bat :
        rnk = i.find('td',class_ ='rankings-block__position')
        nme = i.find('div',class_ ='rankings-block__banner--name-large')
        ctr = i.find('div',class_ ='rankings-block__banner--nationality')
        pts = i.find('div',class_ ='rankings-block__banner--rating')
        rank.append(rnk.text.strip())
        name.append(nme.text.strip())
        country.append(ctr.text.strip())
        points.append(pts.text.strip())
    w_bat =  soup.find_all('tr',class_='table-body')
    for i in w_bat :
        rnk = i.find('td',class_ ='table-body__cell table-body__cell--position u-text-right')
        nme = i.find('a')
        ctr = i.find('span',class_ ='table-body__logo-text')
        pts = i.find('td',class_ ='table-body__cell rating')
        rank.append(rnk.text.strip())
        name.append(nme.text.strip())
        country.append(ctr.text.strip())
        points.append(pts.text.strip())
        if len(points) == 10:
            break
    ODI_Women_ODI__BAT_Ratings = pd.DataFrame([])
    ODI_Women_ODI__BAT_Ratings["Position"] =rank
    ODI_Women_ODI__BAT_Ratings["Player Name"] =name
    ODI_Women_ODI__BAT_Ratings["Team"] =country
    ODI_Women_ODI__BAT_Ratings["Rating"] =points
    return ODI_Women_ODI__BAT_Ratings


# In[18]:


url ="https://www.icc-cricket.com/rankings/womens/player-rankings/odi/batting"
women_odi_bat= w_odi_bat(url)
women_odi_bat


# iii) Top 10 women’s ODI all-rounder along with the records of their team and rating.
# 

# In[19]:


def w_odi_all (url):
    page = requests.get(url)
    soup = BeautifulSoup(page.content)
    w_best_all_odi =  soup.find_all('tr',class_='rankings-block__banner')
    rank =[]
    name=[]
    country=[]
    points =[]
    for i in w_best_all_odi :
        rnk = i.find('td',class_ ='rankings-block__position')
        nme = i.find('div',class_ ='rankings-block__banner--name-large')
        ctr = i.find('div',class_ ='rankings-block__banner--nationality')
        pts = i.find('div',class_ ='rankings-block__banner--rating')
        rank.append(rnk.text.strip())
        name.append(nme.text.strip())
        country.append(ctr.text.strip())
        points.append(pts.text.strip())
    w_all_odi =  soup.find_all('tr',class_='table-body')
    for i in w_all_odi :
        rnk = i.find('td',class_ ='table-body__cell table-body__cell--position u-text-right')
        nme = i.find('a')
        ctr = i.find('span',class_ ='table-body__logo-text')
        pts = i.find('td',class_ ='table-body__cell rating')
        rank.append(rnk.text.strip())
        name.append(nme.text.strip())
        country.append(ctr.text.strip())
        points.append(pts.text.strip())
        if len(points) == 10:
            break
    ODI_Women_ODI_Ratings = pd.DataFrame([])
    ODI_Women_ODI_Ratings["Position"] =rank
    ODI_Women_ODI_Ratings["Player Name"] =name
    ODI_Women_ODI_Ratings["Team"] =country
    ODI_Women_ODI_Ratings["Rating"] =points
    return ODI_Women_ODI_Ratings


# In[20]:


url = "https://www.icc-cricket.com/rankings/womens/player-rankings/odi/all-rounder"
all_rounder_rank= w_odi_all(url)
all_rounder_rank


# # 8. Write a python program to extract information about the local weather from the National Weather Service

# In[23]:


def weather_service(url):
    html = url
    page = requests.get(html)
    print('Website Status',page)
    soup =  BeautifulSoup(page.content)
    period_l=soup.find_all('p',class_ = 'period-name')
    sdesc_l = soup.find_all('p','short-desc')
    t_low =soup.find_all('p','temp temp-low')
    t_high =soup.find_all('p','temp temp-high')
    print('Scrapping Completed')
    period =[]
    for i in period_l:
        period.append(i.text)
    sdesc =[]
    for j in sdesc_l:
        sdesc.append(j.text)
    min_temp = []
    for k in t_low :
        min_temp.append(k.text)
    max_temp = []
    for k in t_high :
        max_temp.append(k.text)
    temp_f = []
    if period[0]=='Today' :
        temp_f =[None]*(len(min_temp)+len(max_temp))
        temp_f[::2]= max_temp
        temp_f[1::2]= min_temp
    else:
        temp_f =[None]*(len(min_temp)+len(max_temp))
        temp_f[::2]= min_temp
        temp_f[1::2]= max_temp
    weather = pd.DataFrame({})
    weather['Period'] =period
    weather['Tempareture'] =temp_f
    #weather['Max_Temp'] =max_temp
    weather['Short_Descriptipn'] =sdesc
    return weather


# In[22]:


print ('**** Weather Forcast ****')
weather_url = "https://forecast.weather.gov/MapClick.php?lat=37.777120000000025&lon=-122.41963999999996#.YM2fa_LivDc" 
report = weather_service(weather_url)
pd.DataFrame(report)


# # 9. Write a python program to scrape fresher job listings from ‘https://internshala.com/’. It should include job title, company name, CTC, and apply date

# In[24]:


def wb_scrap(url):
    page = requests.get(url)
    print(page)
    soup= BeautifulSoup(page.content)
    title_all = soup.find_all('div',class_= "heading_4_5 profile")
    print ('Scrapping Completed')
    job_title = []
    for i in title_all :
        job_title.append(i.text.replace('\n',''))
    comp_all = soup.find_all('a',class_="link_display_like_text")
    company =[]
    for j in comp_all:
        company.append(j.text.strip())
    loc_all = soup.find_all('p',id ='location_names')
    location =[]
    for l in loc_all :
        location.append(l.text.strip())
    job_det =soup.find_all('div',class_ ="item_body")
    j_details=[]
    for i in job_det :
        job_attr=i.text.strip().replace('\xa0' ,' ')
        j_details.append(job_attr)
    start = []
    pkg =[]
    doj = []
    start = j_details[0::3]
    pkg = j_details[1::3]
    doj = j_details[2::3]
    Intern = pd.DataFrame({})
    Intern['Company']= company
    Intern['Job-Title']=job_title
    Intern['Location']=location
    Intern['Starts From ']=start
    Intern['CTC']=pkg
    Intern['Last Date to apply']=doj
    
    
    return Intern


# In[6]:


url_chk = "https://internshala.com/fresher-jobs"
data = wb_scrap(url_chk)
pd.DataFrame(data)


# # 10 .Write a python program to scrape house details from mentioned url. It should include house title, location, area, emi and price

# In[25]:


def no_broker(url):
    page = requests.get(url)
    print(page)
    soup= BeautifulSoup(page.content)
    prop_title = soup.find_all('div',class_ ='nb__2JHKO')
    title = []
    for i in prop_title :
        title.append(i.h2.span.text)
    sqft = soup.find_all('div',class_='nb__3oNyC')
    area = []
    for i in sqft :
        area.append(i.text)
    prop_emi = soup.find_all('div',id ='roomType')
    emi = []
    for i in prop_emi :
        emi.append(i.text)
    prop_loc = soup.find_all('div',class_ ='nb__2CMjv')
    loc = []
    for i in prop_loc :
        loc.append(i.text)
    prop_price =soup.find_all("div", id ="minDeposit")
    price = []
    for i in prop_price :
        j = i.find('div',class_='font-semi-bold heading-6')
        price.append(j.text)
    NO_BROKER_LIST =pd.DataFrame({})
    NO_BROKER_LIST['Availaible'] =title
    NO_BROKER_LIST['Locality'] =loc
    NO_BROKER_LIST['Total_AREA']=area
    NO_BROKER_LIST['Pricre']=price
    NO_BROKER_LIST['Monthly_EMI'] =emi
    return NO_BROKER_LIST


# In[26]:


print ('**** NO BROKER LIST ****')
url = "https://www.nobroker.in/property/sale/bangalore/Electronic%20City?type=BHK4&searchParam=W3sibGF0IjoxMi44NDUyMTQ1LCJsb24iOjc3LjY2MDE2OTUsInBsYWNlSWQiOiJDaElKdy1GUWQ0cHNyanNSSGZkYXpnXzhYRW8iLCJwbGFjZU5hbWUiOiJFbGVjdHJvbmljIENpdHkifV0=&propertyAge=0&radius=2.0"
html_chk  =no_broker(url)
html_chk


# In[ ]:




