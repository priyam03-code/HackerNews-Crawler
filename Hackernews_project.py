import requests

from bs4 import BeautifulSoup

from pprint import pprint


def sort_stories_by_votes(hn_list):

    hn_list.sort(key=lambda item: item["votes"], reverse=True)        #sort the votes in reverse order
    return hn_list


def create_custom_hackernews(links, subtext):

    hn = []

    for idx, item in enumerate(links):
        title = item.getText()                               #gets the title
        href = item.get("href", None)                        #gets the link
        vote = subtext[idx].select(".score")                 #Check if there is a score attribute

        if len(vote):                                        #check if vote exists

            points = int(vote[0].getText().replace(" points", ""))     #it replaces the string "points" with empty space

            if points > 99:
                hn.append({"title": title, "link": href, "votes": points})

    return hn


def hackernews_page(page_url):

    # Request a web page to scrape
    response = requests.get(page_url)

    # Converting web page to an object
    soup_object = BeautifulSoup(response.text, "html.parser")

    links = soup_object.select(".storylink")                  #gets the class of type storylink or simply gets the link
    subtext = soup_object.select(".subtext")                  #gets the subtext of the above link created

    hn_page = create_custom_hackernews(links, subtext)
    return hn_page


def total_pages(pages_num):                  #this function combines the various pages which is given by the user
    combined_pages = []

    # for 1st news page
    hn_page = hackernews_page("https://news.ycombinator.com/news")
    combined_pages.extend(hn_page)

    # loop over rest of news pages
    for i in range(2, pages_num + 1):
        hn_page = hackernews_page(f"https://news.ycombinator.com/news?p={i}")
        combined_pages.extend(hn_page)

    combined_pages = sort_stories_by_votes(combined_pages)
    return combined_pages

n=int(input("Upto how many pages you want the news?"))

important_hn = total_pages(n)

pprint(important_hn)