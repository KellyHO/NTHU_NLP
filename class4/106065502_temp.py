
# coding: utf-8

# In[1]:


import re
from collections import Counter
from pprint import pprint
from math import log

'''Word Probability'''
def words(text): return re.findall(r'\w+', text.lower())
count_word = Counter(words(open('big.txt').read()))
Nw = sum(count_word.values())
Pdist = {word: float(count)/Nw for word, count in count_word.items()}


# In[ ]:


def correction(word):
    MAXBEAM = 500
    total_state = []
    states = [("", word, 0, Pw(word),1)]
    for i in range(len(word)):
#         print(i, states[:3])
        new_s = []
        for s in states:
            new_s += next_states(s)
        states = new_s
        d = {}
        for i in states:
            if i[0]+i[1] in d:
                if d[i[0]+i[1]][2] > i[2]:
                    d[i[0]+i[1]] = i
            else:
                d[i[0]+i[1]] = i
        states = d.values()
        states = sorted(states, key=lambda x: x[2]) 
        states = sorted(states, key=lambda x: P(x[4],x[3],x[2]),reverse=True)[:MAXBEAM] 
#         pprint(states[:3])
#     return max(states[:3])
    return states[:10]


# In[ ]:


def next_states(state):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    L, R, edit, pw, pedit = state
    R0, R1 = R[0], R[1:]
    if edit == 2: return [(L + R0 , R1 , edit ,pw, pedit*0.8 )]
    noedit = [(L + R0 , R1 , edit ,pw, pedit*0.8 )]
    delete  =[(L , R1, edit+1,Pw(L+R1), pedit*Pedit(L[-1]+R0,L[-1]))] if len(L)>0 else [('' , R1, edit+1,Pw(R1), pedit*Pedit(R0,''))]
    replace =[(L +c, R1 , edit+1, Pw(L+c+R1), pedit*Pedit(R0,c) )for c in letters]
    insert = [(L + R0 + c , R1 ,edit+1,Pw(L + R0 + c + R1), pedit*Pedit(R0,R0+c))for c in letters]
    transpose = [( L[:-1] + R0 ,L[-1]+ R1 , edit+1,Pw(L[:-1] + R0 +L[-1]+ R1), pedit+Pedit(L[-1]+R0,R0+L[-1]))] if len(L)>0 else []
#     transpose = [( L + R1[0] ,R0+ R1[1:] , edit+1,Pw(L + R1[0] +R0+ R1[1:]), pedit+Pedit(L + R1,R0+R1[1:]))]

#     delete  =[(L , R1, edit+1,Pw(L+R1), pedit*Pedit(R0,""))]  #if len(L)>0 else []

    return noedit + delete + replace + insert + transpose


# In[ ]:


def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    "The subset of `words` that appear in the dictionary of WORDS."
    return set(w for w in words if w in WORDS)

def edits1(word):
    "All edits that are one edit away from `word`."
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    splits     = [(word[:i], word[i:])    for i in range(len(word) + 1)]
    deletes    = [L + R[1:]               for L, R in splits if R]
    transposes = [L + R[1] + R[0] + R[2:] for L, R in splits if len(R)>1]
    replaces   = [L + c + R[1:]           for L, R in splits if R for c in letters]
    inserts    = [L + c + R               for L, R in splits for c in letters]
    return set(deletes + transposes + replaces + inserts)

def edits2(word):
    "All edits that are two edits away from `word`."
    return (e2 for e1 in edits1(word) for e2 in edits1(e1))


# In[ ]:


count = {}
count_c = {}
for line in open('count_1.txt', 'r'):
#     print(line.split()[0],line.split()[1])
#     print(line.split('\t')[0].split('|')[0],line.split('\t')[0].split('|')[1])
    count[(line.split('\t')[0].split('|')[0],line.split('\t')[0].split('|')[1])] = int(line.split('\t')[1].strip('\n'))
    if line.split('\t')[0].split('|')[1] in count_c:
        count_c[line.split('\t')[0].split('|')[1]] += int(line.split('\t')[1].strip('\n'))
    else:
        count_c[line.split('\t')[0].split('|')[1]] = int(line.split('\t')[1].strip('\n'))


Nall = len(count)
N0 =  26*26*26*26+2*26*26*26+26*26 - Nall
All_N_Count =  Counter(count.values())
# print(All_N_Count)
Nr = [ N0 if r == 0 else All_N_Count[r] for r in range(12) ]
# print(Nr)

def Pw(word, N=sum(count_word.values())): 
#     if word in count_word:
    return count_word[word] / N
#     else:
#         return 0
#         print(10/10**len(word)/Nw)
#         return (1/1000**len(word))/N

def smooth(count, r=10):
#     print(type(count))
    r = int(r)
    if int(count) <= r:
#         if (count+1)*0.7*Nr[count+1]/Nr[count] > 1:
#             print(count,(count+1)*Nr[count+1],Nr[count])
        return (count+1)*Nr[count+1]/Nr[count]
    else:
#         print('smooth',All_N_Count[count])
#         return 0
        return All_N_Count[count]

def Pedit(w, c):
    if c in count_c:
        if count_c[c] > 0:
            if (w,c) not in count:
#                 return log(smooth(0))
#                 print('up',w,c,smooth(0),count_c[c])
                return smooth(0)/count_c[c]

            else:
                try:
#                     if smooth(count[(w,c)])/(count_c[c]) > 1:
#                         print('under',w,c, smooth(count[(w,c)]),count_c[c])
                    return smooth(count[(w,c)])/count_c[c]
                except:
                    print(count_c[c])
    else:
        return 0

# '''Combining channel probability with word probability to score states'''
def P(pedit, pw,edit):
#     return pw
    return pw*pedit/(edit+1)


# In[ ]:


testing_data = open('lab4.test.1.txt')
testing_dict = {}
for i in testing_data.readlines()[:20]:
    testing_dict[i.split('\t')[0].lower().strip()] = i.split('\t')[1].lower().strip()


# In[ ]:


hits = 0
import NetSpeakAPI
SE = NetSpeakAPI.NetSpeak()
for i in testing_dict:
# for i in range(1):
    
#     global hits
    raw_test = i
#     raw_test = 'at brake time'
    
#     raw_test = 'I felt very strang'
    test = raw_test.lower().split()
    
    trigram = {}


    for i in range(len(test) - 2):
        now_tri = ' '.join(test[i:i + 3])
        res = SE.search(' '.join(test[i:i + 3]))
        if res:
            c = '\n'.join(' '.join([str(y) for y in x]) for x in res)
#             print(c)
            trigram[now_tri] = float(c.split(' ')[-1])
#         print('\n'.join('\t'.join([str(y) for y in x]) for x in res))
        else:
            trigram[now_tri] = 0
#             print('not found')
    
#     print(trigram)
    can_tri = min(trigram,key=trigram.get)
    
    candidates = []
    sen_and_err = {}
    for i, t in enumerate(str(can_tri).split(' ')):
        if len(t) < 3:
            pass
        else:
            for i,c in enumerate(correction(t)):
                s = []

                for ot in test:
                    if str(t) == str(ot):
                        s.append(c[0]+c[1])
                    else:
                        s.append(ot)
#                 print(s)
#             candidates[str(t)] = 
#             candidates.append('\t'.join([str(y) for y in s]))
                candidates.append([s,c[0]+c[1],i+1])
                sen_and_err[' '.join([str(y) for y in s])] = (str(t),c[0]+c[1])
        
    score = {}
#     print(candidates)
    for test in candidates:
#         print(test)
        can_trigram = {}
        m_sum = 1
        for i in range(len(test[0]) - 2):
            now_tri = ' '.join(test[0][i:i + 3])
            res = SE.search(' '.join(test[0][i:i + 3]))
            if res:
                c = '\n'.join(' '.join([str(y) for y in x]) for x in res)
                can_trigram[now_tri] = float(c.split(' ')[-1])/test[2]
#                 print('\n'.join(' '.join([str(y) for y in x]) for x in res))
            else:
                if now_tri[0] in Pdist and now_tri[1] in Pdist and now_tri[2] in Pdist:
                    can_trigram[now_tri] = 1/test[2]
                else:
                    can_trigram[now_tri] = 0
#                 print('not found')
    
        for k in can_trigram.values():
            m_sum *= k
        score[' '.join([str(y) for y in test[0]])] = m_sum
    
    error_sen = ' '.join([str(y) for y in test[0]])
    correction_sen = max(score, key=score.get)
    error_text = sen_and_err.get(correction_sen)[0]
    correction_text = sen_and_err.get(correction_sen)[1]
    
    print("Error:",error_text)
    print("Candidates:")
    for i in correction(error_text):
        print(i[0])
    print("Correction:",correction_text)
    correction_sen = " ".join(i for i in correction_sen.split('\t'))
    print(raw_test ,'--->',correction_sen)
    if testing_dict.get(raw_test.lower()) == correction_sen:
        hits += 1
    print("Hits:",hits)
    print('\n')

