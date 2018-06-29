
# coding: utf-8

# In[11]:


import re
from collections import Counter
from pprint import pprint
from math import log

'''Word Probability'''
def words(text): return re.findall(r'\w+', text.lower())
count_word = Counter(words(open('big.txt').read()))
Nw = sum(count_word.values())
Pdist = {word: float(count)/Nw for word, count in count_word.items()}


# def P(word, N=sum(WORDS.values())): 
#     "Probability of `word`."
#     return WORDS[word] / N


def correction(word):
    MAXBEAM = 500
    total_state = []
    states = [("", word, 0, Pw(word),1)]
    for i in range(len(word)):
        print(i, states[:3])
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
        states = sorted(states, key=lambda x: P(x[4],x[3]),reverse=True)[:MAXBEAM] 
        # pprint(states[:3])
    # return max(states[:3])
    return states[:3]

def next_states(state):
    letters    = 'abcdefghijklmnopqrstuvwxyz'
    L, R, edit, pw, pedit = state
    R0, R1 = R[0], R[1:]
    if edit == 2: return [(L + R0 , R1 , edit ,pw, pedit*0.8 )]
    noedit = [(L + R0 , R1 , edit ,pw, pedit*0.8 )]
    delete  =[(L , R1, edit+1,Pw(L+R1), pedit*Pedit(L[-1]+R0,L[-1]))] if len(L)>0 else []
    replace =[(L +c, R1 , edit+1, Pw(L+c+R1), pedit*Pedit(R0,c) )for c in letters]
    insert = [(L + R0 + c , R1 ,edit+1,Pw(L + R0 + c + R1), pedit*Pedit(R0,R0+c))for c in letters]
    transpose = [( L[:-1] + R0 ,L[-1]+ R1 , edit+1,Pw(L[:-1] + R0 +L[-1]+ R1), pedit+Pedit(L[-1]+R0,R0+L[-1]))] if len(L)>0 else []
#     transpose = [( L + R1[0] ,R0+ R1[1:] , edit+1,Pw(L + R1[0] +R0+ R1[1:]), pedit+Pedit(L + R1,R0+R1[1:]))]

#     delete  =[(L , R1, edit+1,Pw(L+R1), pedit*Pedit(R0,""))]  #if len(L)>0 else []

    return noedit + delete + replace + insert + transpose

# def next_states(state):
#     letters    = 'abcdefghijklmnopqrstuvwxyz'
#     L, R, edit, pw, pedit = state
#     R0, R1 = R[0], R[1:]
#     if edit == 2: return [(L + R0 , R1 , edit ,Pw(L+R),1)]
#     noedit = [(L + R0 , R1 , edit ,Pw(L+R),1)]
#     delete  =[(L , R1, edit+1, Pw(L+R1),1)]
#     replace =[(L +c, R1 , edit+1, Pw(L+c+R1),1)for c in letters]
#     insert = [(L + R0 + c , R1 ,edit+1,Pw(L + R0 + c+R1),1 )for c in letters]

#     return noedit + delete + replace + insert

def candidates(word): 
    "Generate possible spelling corrections for word."
    return (known([word]) or known(edits1(word)) or known(edits2(word)) or [word])

def known(words): 
    # "The subset of `words` that appear in the dictionary of WORDS."
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




# In[12]:


# count = dict( [((x.split()[0],x.split()[1]),x.split()[2]) for x in open('count_1.txt', 'r') ] )
count = {}
count_c = {}
for line in open('count_1.txt', 'r'):
#     print(line.split()[0],line.split()[1])
#     print(line.split('\t')[0].split('|')[0],line.split('\t')[0].split('|')[1])
    count[(line.split('\t')[0].split('|')[0],line.split('\t')[0].split('|')[1])] = int(line.split('\t')[1].strip('\n'))
    if line.split('\t')[0].split('|')[1] in count_c:
        count_c[line.split('\t')[0].split('|')[1]] += 1
    else:
        count_c[line.split('\t')[0].split('|')[1]] = 1


Nall = len(count)
N0 =  26*26*26*26+2*26*26*26+26*26 - Nall
All_N_Count =  Counter(count.values())
print(All_N_Count)
Nr = [ N0 if r == 0 else All_N_Count[r] for r in range(12) ]
print(Nr)


# In[13]:


# def Pw(word): 
# #     if word in Pdist:
# #         print(word,log(Pdist[word]))
# #     return log(Pdist[word]) if word in Pdist else log(10/10**len(word)/Nw)
#     return count_word[word]/Nw if word in count_word else 10/10**len(word)/Nw

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
        return (count+1)*Nr[count+1]/Nr[count]
    else:
        return All_N_Count[count]

def Pedit(w, c):
    if c in count_c:
        if count_c[c] > 0:
            if (w,c) not in count:
#                 return log(smooth(0))
#                 print(smooth(0),count_c[c])
                return smooth(0)/count_c[c]

            else:
                try:
#                     return log(smooth(count[(w,c)])/(count_c[c]))
                    return smooth(count[(w,c)])/count_c[c]
                except:
                    print(count_c[c])
    else:
        return 0

# '''Combining channel probability with word probability to score states'''
def P(pedit, pw):
    return pw*pedit


# In[14]:


c = 0
# print(count['a','a-'])
# Counter(count.values())
# for i in range(3):
#     print(Counter(count.values())[str(i)])

# pprint(correction('thenks'))
pprint(correction('gost'))
# pprint(correction('appearant'))
# pprint(next_states(('', "apperent", 0, 0) ))


# In[10]:


# print(Nr)

