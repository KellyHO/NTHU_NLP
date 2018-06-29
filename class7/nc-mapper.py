from collections import Counter, defaultdict
import fileinput
import re

def tokens(str1): return re.findall('[a-z]+', str1.lower()) 
def ngrams(sent, n):
    return [ ' '.join(x) for x in zip(*[sent[i:] for i in range(n) if i <= len(sent) ] ) ]


def get_collocation_dict():
    
    coll_dict = defaultdict(lambda:Counter())
    collocation = open('bnc.coll.small.txt','r')
    
    for line in collocation:
        content = line.strip().split('\t')
        coll_dict[(content[0],content[1],int(content[2]))] = int(content[3])
    
    return coll_dict

coll_dict = get_collocation_dict()
# sentences = open('test_sen.txt','r')
skipBigramExample = defaultdict(lambda:defaultdict(lambda:defaultdict(lambda:[])))
for line in fileinput.input():
# for line in sentences:
# for line in sys.stdin:
    sent = tokens(line)
    if len(sent) > 9 and len(sent) < 26:
        # for n in range(2, 6):
        for n in range(1, 6):

            for ngram in ngrams(sent, n):
#             print ('%s\t%s' % (ngram, 1))
                
                token = ngram.split(' ')
#             print(token)
        
                if (token[0],token[-1],len(token)-1) in coll_dict:
                    output = token[0]+'_'+token[-1]+' '+str(len(token)-1)+'\t'+line.strip()
                    print(output)
#                     print(token[0],token[-1],line)
#                     skipBigramExample[token[0]][token[-1]][len(token)-1].append(line)
        
                if (token[-1],token[0],-(len(token)-1)) in coll_dict:
                    output = token[-1]+'_'+token[0]+' '+str(-(len(token)-1))+'\t'+line.strip()
                    print(output)