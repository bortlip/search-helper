from .queryGoogle import searchGoogle_getArticles
from .TextUtilities import split_text_into_sections_by_sentences
from .memory import memory

def get_mem_from_articles(articles, section_size):
    mem = memory()
    for url, article in articles:
        # Split article text into sections by sentences
        sections = split_text_into_sections_by_sentences(article, section_size)
        print(f"Adding {url} to memory in {len(sections)} sections")
        for section in sections:
            if (section != ''):
                section = f"Url: {url} \n{section}"
                mem.add(section)
    return mem

def getSearchInfo_by_word_length(articles, mem_search_query, word_length, section_size):
    mem = get_mem_from_articles(articles, section_size)
    results = mem.search_word_length(mem_search_query, word_length)
    result = "\n---\n".join(results)
    return result

def semantic_search(internet_search_query, num_search_results, mem_search_query, section_size, word_length):
    articles = searchGoogle_getArticles(internet_search_query, num_search_results)
    results = getSearchInfo_by_word_length(articles, mem_search_query, word_length, section_size)
    urls = [url for url, _ in articles]
    return results, urls