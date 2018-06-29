
# coding: utf-8

# In[1]:


import fileinput
from collections import Counter, defaultdict
import numpy as np


# In[2]:


all_pat = open('all_patterns.txt','r').read().split('\n\n')
# all_pat = ["Seiji Uchida , 48 , who lost the ability to walk in a car accident 27 years ago , said he has long dreamed of visiting the picturesque abbey of Mont Saint - Michel , set on a rocky islet in Normandy .\n\
# LOSE	V n	lost the ability\n\
# LOSE	V n to v	lost the ability to walk\n\
# LOSE	V n to v	asdfghjkl;\n\
# ABILITY	N to v	the ability to walk\n\
# WALK	V in n	walk in a car accident 27 years\n\
# SAY	V n	said he\n\
# SAY	V n v-ed	said he has long dreamed\n\
# VISIT	V n	visiting the picturesque abbey\n\
# SET	V on n	set on a rocky islet"]
pat = []


# In[3]:


NO_list = []
Yes_list = []
HiFreWords = open('../class7/HiFreWords','r')
for line in HiFreWords:
    YES_list = line.strip().split('\t')
for n in open('../class7/prons.txt','r'):
    NO_list.append(n.strip())


# In[5]:


YES_list[0]


# In[4]:


def score_sent(sent):
    score = 0
    for w in sent.split(' '):
        if w in YES_list:
            score += 1
        if w in NO_list:
            score -= 1
    return score


# In[5]:


pattern = defaultdict(lambda:defaultdict(lambda: []))
for line in all_pat:
#     print(line)
    try :
        sent, patterns = line.strip().split('\n',1)
#         print(patterns)
        for p in patterns.split('\n'):
#             print(p)
            word_tag,tags, exam = p.split('\t')
#             print(exam)
#             word_tag, tags , exam = p.split('\t')
#             print(p.split('\t'))
            pattern[word_tag][tags].append(exam)
#             print(pattern)
#             print(p)
#             pat.append(p)
#             s.append(p)
#         pat.append(s)
    except:
        pass


# In[6]:


pattern['REMAIN-V']


# In[ ]:


# for line in pat:
#     for p in line:
#         word_tag, tags , exam = p.split('\t')
# #         print(word,tags,exam)
# #         word_tag = word+'-'+tags.split(' ')[0]
# #         print(word_tag)
#         pattern[word_tag][tags].append(exam)
    
# #             if p.split('\t')[0] == t.split('\t')[0] :
# # #                     print(p.split('\t')[1],t.split('\t')[1])
# #                     if p.split('\t')[1] == t.split('\t')[1]:
# #                         pass
# #                     else:
# #                         pattern[p.split('\t')[1]][t.split('\t')[1]] += 1
# #                     lan_model[p.split('\t')[0]][str(t.split('\t')[1])] += 1
# #     except:
# #         pass


# In[26]:


search_word = 'VALUE-N'


# In[27]:


print(search_word)
sent_sum = []
for i in pattern[search_word]:
    tag_len = len(i.split(' '))
    sent_sum.append(len(pattern[search_word][i])*tag_len**1.5)
# print(sent_sum[:10])
mean = np.mean(sent_sum)
std = np.std(sent_sum)
door = mean+std
# print(door)
for t in pattern[search_word].keys():
    sen_score = {}
    
    sen_len = len(pattern[search_word][t])
    new_sent_len = sen_len * len(t.split(' ')) ** 1.5
#     print(new_sent_len)
    if new_sent_len > door:
        print(new_sent_len)
        print(t,end = '\t')
        print('(',len(pattern[search_word][t]),')',end = '\t')
        
        for sent in pattern[search_word][t]:
#             print(sent)
            if len(sent.split(' ')) > 10 and len(sent.split(' '))< 25:
                sen_score[sent] = score_sent(sent)
        good_sen = max(sen_score.items(), key = lambda x:x[1])[0]
        print(good_sen)

