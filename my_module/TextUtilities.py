import nltk
from nltk.tokenize import sent_tokenize, word_tokenize

def split_text_into_sections_by_sentences(text, max_length):
    # Split the text into sentences
    try:
        sentences = sent_tokenize(text)
    except Exception as e:
        print(e)
        return []
        
    section = "";
    sections = []
    section_word_length = 0

    for sentence in sentences:
        sentence_word_length = len(word_tokenize(sentence))

        if section_word_length + sentence_word_length <= max_length:
            section += sentence + " "
            section_word_length += sentence_word_length
        else:
            sections.append(section.strip())
            section_word_length = 0

            if sentence_word_length > max_length:
                # split into words
                # Split the sentence into chunks of max_length
                words = word_tokenize(sentence)
                section = words[0]
                section_word_length += 1
                for word in words[1:]:
                    if section_word_length + 1 <= max_length:
                        section += " " + word
                        section_word_length += 1
                    else:
                        sections.append(section)
                        section = word
                        section_word_length = 1
                if len(section) > 0:
                    sections.append(section)
                    section = ""
                    section_word_length = 0
            else:
                section = sentence + " "            
                section_word_length = sentence_word_length
        
    sections.append(section.strip())

    return sections

def split_text_into_sections_by_words(text, max_words):
    # Split the text into words
    words = word_tokenize(text)
    section = []
    sections = []

    for word in words:
        if len(section) < max_words:
            section.append(word)
        else:
            sections.append(" ".join(section))
            section = [word]

    sections.append(" ".join(section))

    return sections


# with open('g:\\ChatGPT will replace Programmers Web Developers and Coders.mp4.txt', 'r') as file:
#     text = file.read()


# results = split_into_sentences(text, 3000)


# print(len(results))

# for i, result in enumerate(results):
#     print("----  Group {} Length {} ----".format(i+1, len(result))) 
#     print(i, result)
