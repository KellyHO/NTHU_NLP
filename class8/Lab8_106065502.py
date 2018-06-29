
# coding: utf-8

# In[1]:


import fileinput
from collections import Counter, defaultdict


# In[2]:


src = open('All_src.txt','r').read().split('\n\n')
tgt = open('All_tgt.txt','r').read().split('\n\n')
tgt_p = []
src_p = []
Test_src = open('test_src.txt','r').read().split('\n\n')
testing_src = []


# In[3]:


# pattern = defaultdict(lambda:defaultdict(lambda:Counter()))
lan_model = defaultdict(lambda:Counter())
pattern = defaultdict(lambda:Counter())


# In[4]:


for line in src:
    s = []
    try :
        sent, patterns = line.strip().split('\n',1)
        for p in patterns.split('\n'):
            s.append(p)
        src_p.append(s)
    except:
        pass

for line in tgt:
    s = []
    try :
        sent, patterns = line.strip().split('\n',1)
        for p in patterns.split('\n'):
            s.append(p)
        tgt_p.append(s)
    except:
        pass


# In[ ]:




# for line in tgt:
#     s = []
#     sent, patterns = line.strip().split('\n',1)
#     for p in patterns.split('\n'):
#         s.append(p)
#     tgt_p.append(s)

# for line in Test_src:
#     s = []
#     sent, patterns = line.strip().split('\n',1)
#     for p in patterns.split('\n'):
#         s.append(p)
#     testing_src.append(s)



# In[5]:


print(len(tgt),len(src))


# In[ ]:


src_p[0]


# In[ ]:


tgt_p[0]


# In[6]:


for n, pats in enumerate(src_p):
    for p in pats:
        try :
            for t in tgt_p[n]:
                if p.split('\t')[0] == t.split('\t')[0] :
#                     print(p.split('\t')[1],t.split('\t')[1])
                    if p.split('\t')[1] == t.split('\t')[1]:
                        pass
                    else:
                        pattern[p.split('\t')[1]][t.split('\t')[1]] += 1
                    lan_model[p.split('\t')[0]][str(t.split('\t')[1])] += 1
        except:
            pass
#     if pats.split('\t')[0] == tgt[n][]
    
#     pattern[i.split('\t')[1]][tgt_p[n].split('\t')[1]][i.split('\t')[0]] += 1
#     lan_model[i.split('\t')[0]][tgt_p[n].split('\t')[1]] += 1


# In[48]:


print(pattern['V for n'])
print(sum(pattern['V for n'].values()))
print(pattern['V to n'])


# In[43]:


print(lan_model['APPLY'])
print(sum(lan_model['APPLY'].values()))


# In[49]:


23*518/50/697


# In[57]:


nnn = ['discuss','apply','answer','explain']
for line in Test_src:
    sent, patterns = line.strip().split('\n',1)
    score = {}
    for t in patterns.split('\n'):
#         print(t)
#         t = 'BE	V adv	are by far'
        now_p = t.split('\t') 
        if now_p[0].lower() in nnn:
            print(sent)
            for i in pattern[now_p[1]].items():
#                 print(i[0])
#                 print(now_p[0],now_p[1])
#             print(s)
                for l in lan_model[now_p[0]].items():
                    a = sum(pattern[now_p[1]].values())
                    b = sum(lan_model[now_p[0]].values())
#                     print(i[1],l[1],a,b,i[1]*l[1]/a/b)
#                     print(now_p[0],now_p[1],i[0])
                    score[(now_p[0],now_p[1],i[0],l[0])] = i[1]*l[1]/a/b
#                     total_a += i[1]
        

    if score :
#         print(score)
        a = max(score.keys(),key=lambda x: score[x])
#         total = sum(score.values())
        print(a, score[a])
        print('\n')

