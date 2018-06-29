
# coding: utf-8

# In[1]:


from collections import defaultdict
import numpy as np


# In[2]:


ch_text = open('UM-Corpus.ch.200k.tagged.txt')
ch_list = []
for line in ch_text:
    ch_list.append(line.strip().split(' '))


# In[70]:


ch_list[0][0]


# In[3]:


match_token = open('align.final.200k','r')
match_list = []
for line in match_token:
    match_list.append(line.strip().split())
#     print(line)


# In[ ]:


ch_list[141]


# In[4]:


all_info = []
for n, line in enumerate(open('all_patterns.txt','r').read().split('\n\n')):
    
    try:
        sent, patterns = line.strip().split('\n',1)
        for p in patterns.split('\n'):
            if n == 141:
                print(p)
                
            start = int(p.split('\t')[3])
            end = int(p.split('\t')[4])
            to_ch_index = []
            
            for index in range(start,end+1):
                if n == 141:
                    print(l.split('-')[1])
                for l in match_list[n]:
                    if l.split('-')[0] == str(index):
                        to_ch_index.append(l.split('-')[1])
            if to_ch_index:
#                 print(p)
                
                to_ch_index = ' '.join(to_ch_index)
#             if to_ch_index == ' ':
#                 print(p)
                
            
            
        
                all_info.append((n,p.split('\t')[1],p.split('\t')[2],to_ch_index))
    
    except:
            continue
    


# In[64]:


all_info[26644]


# In[87]:


all_info_dict = defaultdict(lambda:defaultdict(lambda:[]))
N_V = ['N','V']
vpn = ["V about n","V in n", "V on n","V to n","V for n", "V with n"]
ignore_p = [("asp",""),("sfp",""),("det",""),("cl",""),("de","")]
for n, info in enumerate(all_info):
    
    # tag match to see if is I DONT KNOW~~~
    en_right_tag = info[1].split(' ')[0]
    ch_doubt_tag = info[3].split(' ')[0]
#     print(info[2])
    sent_index = int(info[0])
    ch_trans = []
    ch_tags = []
    
#     print(sent_index,n)
    try:
        flag = False
        temp = sorted([int(i) for i in set(info[3].strip().split(' '))])
        for i in temp:
            i = str(i)
#             print()
            ch_trans.append(ch_list[sent_index][int(i)])
            
            if ch_list[sent_index][int(i)].split('_')[1] in N_V:
#             print(i , ch_doubt_tag,ch_list[sent_index][int(i)].split('_')[1],en_right_tag)

                if i == ch_doubt_tag and ch_list[sent_index][int(i)].split('_')[1] == en_right_tag:
                    flag = True
                    ch_tags.append(ch_list[sent_index][int(i)].split('_')[1])
                else:
                    ch_tags.append(ch_list[sent_index][int(i)].split('_')[1].lower())
                
            else:
                ch_tags.append(ch_list[sent_index][int(i)].split('_')[1].lower())
#             else:
#                 ch_trans.append(ch_list[sent_index][int(i)])
            
        whole_sent = info[2] + '\t' +' '.join(ch_trans)
#         print(ch_tags)
        if flag:
            x = ' '.join(ch_tags)
            for i in ignore_p:
                x = x.replace(i[0],i[1])
            x = ' '.join([xxx.strip() for xxx in x.split()]).replace('nv n', 'n').replace('n n', 'n').replace('adv V', 'V')
            
            if info[1] in vpn:
                all_info_dict['V p n'][x].append(whole_sent)
            else:
                all_info_dict[info[1]][x].append(whole_sent)
    except:
        print(n,sent_index,ch_list[sent_index][int(i)].split('_'))
#     print('-------')


# In[76]:


all_info_dict['V p n'][0]


# In[ ]:


search_word = 'V n'


# In[27]:


total = 0
# for i in all_info_dict['V n']:
#     total += len(all_info_dict['V n'][i])
#     total += len(i)
print(total)
print(len(all_info_dict['V n']['V p n']))
for i in all_info_dict['V n']:
    total += len(all_info_dict['V n'][i])
#     total += 1
#     print(i)

print(total)
print(len(set(all_info_dict['V p n']['P n V'])))
print(all_info_dict['V p n']['p n V'])


# In[91]:


sent_sum = []
total = []
search_word = 'V n'
for i in all_info_dict[search_word]:
    total.append(len(all_info_dict[search_word][i]))
mean = np.mean(total)
std = np.std(total)
door = mean + 2*std


# In[92]:


for i in sorted(all_info_dict[search_word],key=lambda x:-len(all_info_dict[search_word][x]) ):
    if len(all_info_dict[search_word][i]) > door and i != '':
        print(i,len(all_info_dict[search_word][i]))
        for sent in list(set(all_info_dict[search_word][i]))[:3]:
            print(sent)
        print('\n')
#         print(all_info_dict[search_word][i][:3])
#         print(all_info_dict[search_word][i])


# In[ ]:


mean

