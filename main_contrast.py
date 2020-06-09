import re
from nltk.stem import  WordNetLemmatizer, PorterStemmer
import math
import matplotlib.mlab as mlab
import matplotlib.pyplot as plt


# texts about dogs
source_texts = [["dogs1.txt",
                "dogs2.txt",
                "dogs3.txt",
                "dogs4.txt",
                "dogs5.txt",
                "dogs6.txt",
                "dogs7.txt",
                "dogs8.txt",
                "dogs9.txt",
                "dogs10.txt",
                ]]

#texts obout text analysis
source_texts += [["texts1.txt",
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
                ]]
#COHA
source_texts += [[ "fic_1817_8550.txt",
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
                ]]

stop_words = ['the', 'a', 'and', 'of', 'to', 'in', 'i', 'that', 'is', 'it', 'you',
              'he', 'for', 'wa', 'with', 's', 'my', 'his', 'on', 'not', 'this', 'be',
              'from', 'me', 'we', 'text', 'at', 'your', 'him', 'they', 'all', 'or',
              'her', 'what', 'can', 'no', 'one', 'will', 'had', 'so', 'an', 'do',
              'ha', 'their', 'if', 'when', 'she', 'there', 'which', 'would', 'were',
              'more', 'n', 'then', 'like', 'who', 'out', 'count', 'our', 'up', 'now',
              'them', 'these', 'some', 'been', 'about', 'could', 'may', 'how', 'd',
              'into', 'such', 'only', 'make', 'an', 'where', 'yes', 'most', 'must',
              'take', 'very', 'just', 'should', 'any', 'was', 'have', 't', 'isn',
              'by', 'but', 'after' , 'two', 'many', 'are', 'use', 'get', 'other',
              'keep', 'also', 'first'
              ]

texts_count = len(source_texts)

#stemmer = PorterStemmer()
lemmatizer = WordNetLemmatizer()

texts_data = []

for i in range(len(source_texts)):

    corp_data = []

    for j in range(len(source_texts[i])):
    
        text_file = open('corp\\' + source_texts[i][j], "r", encoding="utf8")
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

        corp_data.append(text_dict)
    texts_data.append(corp_data)

#number of texts
texts_count = sum([len(i) for i in source_texts])

# TF IDF

collection_results = []

for corp_data in texts_data:
    
    corp_dict = {}

    for text_data in corp_data:
        for word in text_data['word_counts']:
            TF = text_data['word_counts'][word]/text_data['length']
            #print(TF)
            cnt = 0
            for corp_data_ in texts_data:
                for text_data_ in corp_data:
                    if word in text_data_['word_counts']:
                        cnt += 1
            IDF = math.log10(texts_count/cnt)

            TF_IDF = TF*IDF
            if word in corp_dict:
                corp_dict[word] += TF_IDF
            else:
                corp_dict[word] = TF_IDF
    result = [(word, corp_dict[word]) for word in corp_dict]
    result.sort(key=lambda x: x[1], reverse=True)
    collection_results.append(result)


specific_words = [[word for word, _ in terms[:int(len(terms) * 0.05)]]for terms in collection_results]

# remove non-specific words from specific words
for i, words in enumerate(specific_words):
    print("Specific words ", i, ':', sep = '')
    for j, nonspecific_words in enumerate(collection_results):
        if j != i:
            words = list(filter(lambda word: word not in [word for word, _ in nonspecific_words], words))
    print(*words, sep = ', ')
    print('\n'*3)
