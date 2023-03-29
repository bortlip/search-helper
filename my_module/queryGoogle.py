from itertools import islice
from googlesearch import search
import requests
from bs4 import BeautifulSoup

def get_article_text(url, session):
    while True:
        retry_count = 2
        for i in range(0,retry_count):
            try:
                # Make a GET request to fetch the raw HTML content
                print(f"Getting {url}")
                html_content = session.get(url, timeout=5).text

                # Parse the html content
                soup = BeautifulSoup(html_content, "lxml")

                text = soup.get_text()

                text = "\r\n".join([line for line in text.split("\r\n") if line.strip()])
                text = "\n".join([line for line in text.split("\n") if line.strip()])

                return text
            except Exception as e:
                # Retry the function after a delay if the API returns an error
                print(f"API Error: {e}")
                print(f"Retrying...")
                continue
        return "Error getting article.  No info found."
    # # Get all the paragraph tags and heading tags from the HTML
    # paras_and_headings = soup.find_all(['p', 'h1', 'h2', 'h3', 'h4', 'h5', 'h6', 'a', 'code'])

    # # Extract the text and tags from all the paragraph and heading tags
    # article_text = ''
    # for tag in paras_and_headings:  
    #     article_text += str(tag)

    #     # if tag.name == 'p':
    #     #     article_text += tag.text
    #     # else:
    #     #     article_text += '<' + str(tag.name) + '>' + tag.text + '</' + str(tag.name) + '>'

    # return article_text

# TBS:
# Any time: tbs=qdr:a
# Last second: tbs=qdr:s (Read more about this “real time search” on Lifehacker)
# Last minute: tbs=qdr:n (Note! n like in nuts)
# Last 10 minutes: tbs=qdr:n10 (and so on for any number of minutes)
# Last hour: tbs=qdr:h
# Last 12 hours: tbs=qdr:h10 (and so on for any number of hours)
# Last day: tbs=qdr:d
# Last week: tbs=qdr:w
# Last month: tbs=qdr:m
# Last year: tbs=qdr:y
# A specific time range, for example from March 2 1984 to June 5 1987: tbs=cdr:1,cd_min:3/2/1984,cd_max:6/5/1987
# Sort by date: tbs=sbd:1
# Sort by relevance: tbs=sbd:0


def searchGoogle_getUrls(query, num_results):
    # Create an empty set to store unique URLs
    unique_urls = set()

    try:
        # Keep searching until we have enough unique URLs
        start = 0
        while len(unique_urls) < num_results:
            # Search Google and get the next 10 results
            results = search(query, start=start, stop=start + 10)

            # Loop through each result URL and add it to the set
            for url in results:
                # Remove any anchor tags from the URL (i.e., anything after the # character)
                url = url.split('#')[0]
                # Add the URL to the set
                unique_urls.add(url)

            # Increment the start value for the next iteration
            start += 10
    except Exception as e:
        print(f"API Error: {e}")

    # Convert the set back to a list and return it
    return list(unique_urls)[:num_results]

# def searchGoogle_getUrls(query, num_results):
#     # Search Google and get the top 10 results
#     results = search(
#         query,
#         start = 0,
#         stop = num_results)
#     return results

def searchGoogle_getArticles(query, num_results):
    searchResultUrls = searchGoogle_getUrls(query, num_results)
    session = requests.Session()
    searchResultArticles =  [(url, get_article_text(url, session)) for url in searchResultUrls]
    return searchResultArticles


# # The search query
# query = "What is the difference between WebClient and HttpClient in .net, DOTNET, Microsoft.Net, c#? Which should be used?"

# searchResultArticles = searchGoogle_getArticles(query, 2)

# for url, article in searchResultArticles:
#     print("\n\n--- Article URL: " + url + " ---")
#     print("--- Article: ")
#     print(article)





# with open("search_results.txt", "w") as f:
#     for url, article in searchResultArticles:
#       f.write("\n\n--- Article URL: " + url + " ---")
#       f.write("--- Article: ")
#       f.write(article)


# Get the list of URLs from the results
#urls = [result in results]

# Print the URLs
#print(urls)