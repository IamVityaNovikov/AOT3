import re
from nltk.stem import  WordNetLemmatizer, PorterStemmer
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


SELECTED_TEXT = 6


# texts about dogs
source_texts = ["dogs1.txt",
                "dogs2.txt",
                "dogs3.txt",
                "dogs4.txt",
                "dogs5.txt",
                "dogs6.txt",
                "dogs7.txt",
                "dogs8.txt",
                "dogs9.txt",
                "dogs10.txt",
                ]

#texts obout text analysis
source_texts += ["texts1.txt",
                "texts2.txt",
                "texts3.txt",
                "texts4.txt",
                "texts5.txt",
                "texts6.txt",
                "texts7.txt",
                "texts8.txt",
                "texts9.txt",
                "texts10.txt",
                "texts11.txt",
                "texts12.txt",
                ]
#COHA
source_texts += [ "fic_1817_8550.txt",
                "fic_1827_8950.txt",
                "fic_1830_8750.txt",
                "fic_1831_8850.txt",
                "fic_1836_8650.txt",
                "fic_1847_7650.txt",
                "fic_1868_9550.txt",
                "fic_1874_9050.txt",
                "fic_1884_9250.txt",
                "fic_1992_40350.txt",
                "fic_1993_53750.txt",
                "fic_1994_53950.txt",
                "fic_1995_52950.txt",
                "fic_1996_54250.txt",
                "fic_1998_30150.txt",
                ]

stop_words = ['the', 'a', 'and', 'of', 'to', 'in', 'i', 'that', 'is', 'it', 'you',
              'he', 'for', 'wa', 'with', 's', 'my', 'his', 'on', 'not', 'this', 'be',
              'from', 'me', 'we', 'text', 'at', 'your', 'him', 'they', 'all', 'or',
              'her', 'what', 'can', 'no', 'one', 'will', 'had', 'so', 'an', 'do',
              'ha', 'their', 'if', 'when', 'she', 'there', 'which', 'would', 'were',
              'more', 'n', 'then', 'like', 'who', 'out', 'count', 'our', 'up', 'now',
              'them', 'these', 'some', 'been', 'about', 'could', 'may', 'how', 'd',
              'into', 'such', 'only', 'make', 'an', 'where', 'yes', 'most', 'must',
              'take', 'very', 'just', 'should', 'any', 'was', 'have', 't', 'isn'
              ]

texts_count = len(source_texts)

stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

texts_data = []

for i in range(texts_count):

    if i == SELECTED_TEXT:
        print(source_texts[i])
    
    text_file = open(source_texts[i], "r", encoding="utf8")
    words = text_file.read()
    words = re.findall(r"[a-zA-Z]+", words)
    words = [word.lower() for  word in words]
    words = [lemmatizer.lemmatize(word) for word in words]
    words = list(filter(lambda word: word not in stop_words, words))

    
    length = len(words)
    
    word_counts = {}
    for word in words:
        if word in word_counts:
            word_counts[word] += 1
        else:
            word_counts[word] = 1
            
    text_dict = {}
    text_dict['length'] = length
    text_dict['word_counts'] =  word_counts

    texts_data.append(text_dict)

#the TF IDF

results = []

for word in texts_data[SELECTED_TEXT]['word_counts'].keys():

    TF = texts_data[SELECTED_TEXT]['word_counts'][word]/texts_data[SELECTED_TEXT]['length']

    cnt = 0

    for text in texts_data:
        if word in text['word_counts'].keys():
            cnt += 1
            
    IDF = math.log10(texts_count/cnt)

    results.append((word, TF * IDF))


results.sort(key=lambda x: x[1], reverse=True)

for i in range(len(results)):
    if results[i][0] == 'dog':
        print(i)
        print(len(results))
        print(texts_data[SELECTED_TEXT]['word_counts']['dog'],'/',texts_data[SELECTED_TEXT]['length'])

result_lenth = 1000

width = 0.75
plt.bar([pair[0] for pair in results[:result_lenth]], [pair[1] for pair in results[:result_lenth]], width, align='center', )
plt.xticks(rotation='vertical')
plt.show()

