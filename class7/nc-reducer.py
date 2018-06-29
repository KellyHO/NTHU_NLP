import sys
from collections import Counter, defaultdict
# ngm_count = defaultdict(Counter)
import fileinput
def tokens(str1): return re.findall('[a-z]+', str1.lower()) 
import re


output = open('test_map_result.txt','r')
HiFreWords = open('HiFreWords','r')
for line in HiFreWords:
    NO_list = line.strip().split('\t')
for n in open('prons.txt','r'):
    NO_list.append(n.strip())

score_dict = defaultdict(lambda:defaultdict(lambda:defaultdict()))


for line in fileinput.input():
# for line in sys.stdin:
    ngm, ex_sen = line.strip().split('\t')
    distance = ngm.split(' ')[1]
    first_word = ngm.split('_')[0]
    sen_token = tokens(ex_sen)
    position = sen_token.index(first_word)
#     print(position,first_word)
    minus = 0
    for t in sen_token:
        if t in NO_list:
            minus += 1
    scores = position - minus
    
    score_dict[(ngm,distance)][ex_sen] = scores

for i in score_dict.keys():
    print(i[0])
    print(sorted(score_dict[i].items(),key=lambda x: -x[1])[0][0])