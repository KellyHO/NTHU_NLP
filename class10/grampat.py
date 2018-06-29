
# coding: utf-8

# In[1]:


import sys
from collections import defaultdict
from pprint import pprint
import numpy
maxDegree = 9


# In[2]:


pgPreps = 'in_favor_of|_|about|after|against|among|as|at|between|behind|by|for|from|in|into|of|on|upon|over|through|to|toward|towarV in favour of	ruled in favour ofV in favour of	ruled in favour ofds|with'.split('|')
otherPreps ='out|down'.split('|')
verbpat = ('V; V n; V ord; V oneself; V adj; V -ing; V to v; V v; V that; V wh; V wh to v; V quote; '+              'V so; V not; V as if; V as though; V someway; V together; V as adj; V as to wh; V by amount; '+              'V amount; V by -ing; V in favour of n; V in favour of ing; V n in favour of n; V n in favour of ing; V n n; V n adj; V n -ing; V n to v; V n v n; V n that; '+              'V n wh; V n wh to v; V n quote; V n v-ed; V n someway; V n with together; '+              'V n as adj; V n into -ing; V adv; V and v').split('; ')
verbpat += ['V %s n' % prep for prep in pgPreps]+['V n %s n' % prep for prep in verbpat]
verbpat += [pat.replace('V ', 'V-ed ') for pat in verbpat]
reservedWords = 'how wh; who wh; what wh; when wh; someway someway; together together; that that'.split('; ')
pronOBJ = ['me', 'us', 'you', 'him', 'them']


# In[3]:


pgNoun = ('N for n to v; N from n that; N from n to v; N from n for n; N in favor of; N in favour of; '+            'N of amount; N of n as n; N of n to n; N of n with n; N on n for n; N on n to v'+            'N that; N to v; N to n that; N to n to v; N with n for n; N with n that; N with n to v').split('; ')
pgNoun += pgNoun + ['N %s -ing' % prep for prep in pgPreps ]
pgNoun += pgNoun + ['ADJ %s n' % prep for prep in pgPreps if prep != 'of']+ ['N %s -ing' % prep for prep in pgPreps]
pgAdj = ('ADJ adj; ADJ and adj; ADJ as to wh; '+        'ADJ enough; ADJ enough for n; ADJ enough for n to v; ADJ enough n; '+        'ADJ enough n for n; ADJ enough n for n to v; ADJ enough n that; ADJ enough to v; '+        'ADJ for n to v; ADJ from n to n; ADJ in color; ADJ -ing; '+        'ADJ in n as n; ADJ in n from n; ADJ in n to n; ADJ in n with n; ADJ in n as n; ADJ n for n'+        'ADJ n to v; ADJ on n for n; ADJ on n to v; ADJ that; ADJ to v; ADJ to n for n; ADJ n for -ing'+        'ADJ wh; ADJ on n for n; ADJ on n to v; ADJ that; ADJ to v; ADJ to n for n; ADJ n for -ing').split('; ')
pgAdj += [ 'ADJ %s n'%prep for prep in pgPreps ]


# In[4]:


pgPatterns = verbpat + pgAdj + pgNoun
# pgPatterns = pgNoun
"""
 'N into -ing',
 'N of -ing',
 'N on -ing',
 'N upon -ing',
 'N over -ing',
 'N through -ing'
"""
mapRW = dict( [ pair.split() for pair in reservedWords ] )


# In[5]:


def isverbpat(pat):
#     return  pat in verbpat
    return pat in pgPatterns

def sentence_to_ngram(words, lemmas, tags, chunks): 
    return [ (k, k+degree) for k in range(1,len(words))             for degree in range(2, min(maxDegree, len(words)-k+1)) ]


# In[6]:


mapRest = dict( [('VBG', 'ing'), ('VBD', 'v-ed'), ('VBN', 'v-ed'), ('VB', 'v'),('NN', 'n'), ('NNS', 'n'), ('JJ', 'adj'), ('RB', 'adv'),('NP', 'n'),('VP','v'),('JP','adj'),('ADJP','adj'),('ADVP','adv'),('SBAR','that')] )
mapHead = dict( [('H-NP', 'N'), ('H-VP', 'V'), ('H-ADJP', 'ADJ'), ('H-ADVP', 'ADV'), ('H-VB', 'V')] )


# In[7]:


def hasTwoObjs(tag, chunk):
    if chunk[-1] != 'H-NP': return False
    return (len(tag) > 1 and tag[0] in pronOBJ) or (len(tag) > 1 and 'DT' in tag[1:])
    
def chunk_to_element(words, lemmas, tags, chunks, i, isHead):
    #print ('***', i, words[i], lemmas[i], tags[i], chunks[i], isHead, tags[i][-1] == 'RP' and tags[i-1][-1][:2] == 'VB')
    if isHead:
#         x = mapHead[chunks[i][-1]] if chunks[i][-1] in mapHead else '*'
#         print(chunks[i][-1],x)
        return mapHead[chunks[i][-1]] if chunks[i][-1] in mapHead else '*'
    if lemmas[i][0] == 'favour' and words[i-1][-1]=='in' and words[i+1][0]=='of': return 'favour'
    if tags[i][-1] == 'RP' and tags[i-1][-1][:2] == 'VB':                return '_'
    if tags[i][0][0]=='W' and lemmas[i][-1] in mapRW:                    return mapRW[lemmas[i][-1]]
    if hasTwoObjs(tags[i], chunks[i]):                                              return 'n n'
    if tags[i][-1] in mapRest:                            return mapRest[tags[i][-1]]
    if tags[i][-1][:2] in mapRest:                        return mapRest[tags[i][-1][:2]]
    if chunks[i][-1] in mapHead:
#         print(mapHead[chunks[i][-1]].lower())
        return mapHead[chunks[i][-1]].lower()
    if lemmas[i][-1] in pgPreps:                                         return lemmas[i][-1]
    return lemmas[i][-1]


# In[8]:


def simplifyPat(pat): return 'V' if pat == 'V ,' else pat.replace(' _', '').replace('_', ' ').replace('  ', ' ')
    
def ngram_to_pat(words, lemmas, tags, chunks, start, end):
    pat, doneHead = [], False
    for i in range(start, end):
#         if tags[i][-1][0] in 'V ADJ N' and not doneHead:
#             isHead = tags[i][-1][0]
#         isHead = tags[i][-1][0] in ['V', 'N','J'] and not doneHead
        isHead = tags[i][-1][0] in ['V', 'N','J'] and not doneHead
        pat.append( chunk_to_element(words, lemmas, tags, chunks, i, isHead) )
        if isHead: doneHead = True
    pat = simplifyPat(' '.join(pat))
    #print ('===', start, end, pat, words[start:end])
    return pat if isverbpat(pat) else ''

def ngram_to_head(words, lemmas, tags, chunks, start, end):
    for i in range(start, end):
        if tags[i][-1][0] in 'V' and tags[i+1][-1]=='RP':  return lemmas[i][-1].upper()+ ('_'+lemmas[i+1][-1].upper())
        if tags[i][-1][0] in ['V', 'N','J']:  return lemmas[i][-1].upper()
#         if tags[i][-1][0] in 'V':  return lemmas[i][-1].upper()
        


# In[9]:


akl = dict( [ (x+'-n', True) for x in 'focus, ability, absence, account, achievement, act, action, activity, addition, adoption, adult, advance, advantage, advice, age, aim, alternative, amount, analogy, analysis, application, approach, argument, aspect, assertion, assessment, assistance, association, assumption, attempt, attention, attitude, author, awareness, balance, basis, behaviour, behavior, being, belief, benefit, bias, birth, capacity, case, category, cause, centre, challenge, change, character, characteristic, choice, circumstance, class, classification, code, colleague, combination, commitment, committee, communication, community, comparison, complexity, compromise, concentration, concept, conception, concern, conclusion, condition, conduct, conflict, consensus, consequence, consideration, constraint, construction, content, contradiction, contrast, contribution, control, convention, correlation, country, creation, crisis, criterion, criticism, culture, damage, data, debate, decision, decline, defence, defense, definition, degree, demand, description, destruction, determination, development, difference, difficulty, dilemma, dimension, disadvantage, discovery, discrimination, discussion, distinction, diversity, division, doctrine, effect, effectiveness, element, emphasis, environment, error, essence, establishment, evaluation, event, evidence, evolution, examination, example, exception, exclusion, existence, expansion, experience, experiment, explanation, exposure, extent, extreme, fact, factor, failure, feature, female, figure, finding, force, form, formation, function, future, gain, group, growth, guidance, guideline, hypothesis, idea, identity, impact, implication, importance, improvement, increase, indication, individual, influence, information, insight, instance, institution, integration, interaction, interest, interpretation, intervention, introduction, investigation, isolation, issue, kind, knowledge, lack, learning, level, likelihood, limit, limitation, link, list, literature, logic, loss, maintenance, majority, male, manipulation, mankind, material, means, measure, medium, member, method, minority, mode, model, motivation, movement, need, network, norm, notion, number, observation, observer, occurrence, operation, opportunity, option, organisation, organization, outcome, output, paper, parallel, parent, part, participant, past, pattern, percentage, perception, period, person, personality, perspective, phenomenon, point, policy, population, position, possibility, potential, practice, presence, pressure, problem, procedure, process, production, programme, program, progress, property, proportion, proposition, protection, provision, publication, purpose, quality, question, range, rate, reader, reality, reason, reasoning, recognition, reduction, reference, relation, relationship, relevance, report, representative, reproduction, requirement, research, resistance, resolution, resource, respect, restriction, result, review, rise, risk, role, rule, sample, scale, scheme, scope, search, section, selection, sense, separation, series, service, set, sex, shift, significance, similarity, situation, skill, society, solution, source, space, spread, standard, statistics, stimulus, strategy, stress, structure, subject, success, summary, support, survey, system, target, task, team, technique, tendency, tension, term, theme, theory, tolerance, topic, tradition, transition, trend, type, uncertainty, understanding, unit, use, validity, value, variation, variety, version, view, viewpoint, volume, whole, work, world'.split(', ') ]+            [ (x+'-v', True)  for x in 'accept, account, achieve, acquire, act, adapt, adopt, advance, advocate, affect, aid, aim, allocate, allow, alter, analyse, analyze, appear, apply, argue, arise, assert, assess, assign, associate, assist, assume, attain, attempt, attend, attribute, avoid, base, be, become, benefit, can, cause, characterise, characterize, choose, cite, claim, clarify, classify, coincide, combine, compare, compete, comprise, concentrate, concern, conclude, conduct, confine, conform, connect, consider, consist, constitute, construct, contain, contrast, contribute, control, convert, correspond, create, damage, deal, decline, define, demonstrate, depend, derive, describe, design, destroy, determine, develop, differ, differentiate, diminish, direct, discuss, display, distinguish, divide, dominate, effect, eliminate, emerge, emphasize, employ, enable, encounter, encourage, enhance, ensure, establish, evaluate, evolve, examine, exceed, exclude, exemplify, exist, expand, experience, explain, expose, express, extend, facilitate, fail, favour, favor, finance, focus, follow, form, formulate, function, gain, generate, govern, highlight, identify, illustrate, imply, impose, improve, include, incorporate, increase, indicate, induce, influence, initiate, integrate, interpret, introduce, investigate, involve, isolate, label, lack, lead, limit, link, locate, maintain, may, measure, neglect, note, obtain, occur, operate, outline, overcome, participate, perceive, perform, permit, pose, possess, precede, predict, present, preserve, prevent, produce, promote, propose, prove, provide, publish, pursue, quote, receive, record, reduce, refer, reflect, regard, regulate, reinforce, reject, relate, rely, remain, remove, render, replace, report, represent, reproduce, require, resolve, respond, restrict, result, retain, reveal, seek, select, separate, should, show, solve, specify, state, stimulate, strengthen, stress, study, submit, suffer, suggest, summarise, summarize, supply, support, sustain, tackle, tend, term, transform, treat, undermine, undertake, use, vary, view, write, yield'.split(', ') ]+            [ (x+'-adj', True) for x in 'absolute, abstract, acceptable, accessible, active, actual, acute, additional, adequate, alternative, apparent, applicable, appropriate, arbitrary, available, average, basic, central, certain, clear, common, competitive, complete, complex, comprehensive, considerable, consistent, conventional, correct, critical, crucial, dependent, detailed, different, difficult, distinct, dominant, early, effective, equal, equivalent, essential, evident, excessive, experimental, explicit, extensive, extreme, far, favourable, favorable, final, fixed, following, formal, frequent, fundamental, future, general, great, high, human, ideal, identical, immediate, important, inadequate, incomplete, independent, indirect, individual, inferior, influential, inherent, initial, interesting, internal, large, late, leading, likely, limited, local, logical, main, major, male, maximum, mental, minimal, minor, misleading, modern, mutual, natural, necessary, negative, new, normal, obvious, original, other, overall, parallel, partial, particular, passive, past, permanent, physical, positive, possible, potential, practical, present, previous, primary, prime, principal, productive, profound, progressive, prominent, psychological, radical, random, rapid, rational, real, realistic, recent, related, relative, relevant, representative, responsible, restricted, scientific, secondary, selective, separate, severe, sexual, significant, similar, simple, single, so-called, social, special, specific, stable, standard, strict, subsequent, substantial, successful, successive, sufficient, suitable, surprising, symbolic, systematic, theoretical, total, traditional, true, typical, unique, unlike, unlikely, unsuccessful, useful, valid, valuable, varied, various, visual, vital, wide, widespread'.split(', ') ]+            [ (x+'-adv', True) for x in 'above, accordingly, accurately, adequately, also, approximately, at best, basically, clearly, closely, commonly, consequently, considerably, conversely, correctly, directly, effectively, e.g., either, equally, especially, essentially, explicitly, extremely, fairly, far, for example, for instance, frequently, fully, further, generally, greatly, hence, highly, however, increasingly, indeed, independently, indirectly, inevitably, initially, in general, in particular, largely, less, mainly, more, moreover, most, namely, necessarily, normally, notably, often, only, originally, over, partially, particularly, potentially, previously, primarily, purely, readily, recently, relatively, secondly, significantly, similarly, simply, socially, solely somewhat, specifically, strongly, subsequently, successfully, thereby, therefore, thus, traditionally, typically, ultimately, virtually, wholly, widely'.split(', ') ] )


# In[40]:


# sss = 'FOCUS-N'
# print(akl[sss.lower()])
# # akl['focus-n']


# In[36]:


# line = [('all the commune members', ',', 'young and old', ',', 'went', 'out', 'to', 'hervest', 'the crops', '.'), ('all the commune member', ',', 'young and old', ',', 'go', 'out', 'to', 'hervest', 'the crop', '.'), ('PDT DT JJ NNS', ',', 'JJ CC JJ', ',', 'VBD', 'RP', 'TO', 'VB', 'DT NNS', '.'), ('I-NP I-NP I-NP H-NP', 'O', 'I-NP I-NP H-NP', 'O', 'H-VP', 'H-PRT', 'H-TO', 'H-VP', 'I-NP H-NP', 'O')]
# line = str(line)

# parse = eval(line.strip())
# parse = [ [y.split() for y in x]  for x in parse ]
# print ('\n'+' '.join([' '.join(x) for x in parse[0] ]))
# to_token = ' '.join([' '.join(x) for x in parse[0] ]).split(' ')
# # print(to_token)

# for start, end in sentence_to_ngram(*parse):

# # for n, start, end in enumerate(sentence_to_ngram(*parse)):
#     pat = ngram_to_pat(*parse, start, end)
#     if pat:
#         word = ngram_to_head(*parse, start, end)
#         temp_token = ' '.join([' '.join(x) for x in parse[0][start:end]]).split(' ')
#         len_token = len(temp_token)
# #         print(len_token)
#         for n, t in enumerate(to_token):
# #             print(temp_token)
# #             print(to_token[n:n+len_token+1])
#             if temp_token == to_token[n:n+len_token]:
#                 token_start = n
#                 token_end = n+len_token-1
# #                 print(n,token_start,token_end)
# #         for i in range(start,end+1):
# #             print(i)
        
#                 print('%s\t%s\t%s\t%d\t%d' %(word,pat,' '.join([' '.join(x) for x in parse[0][start:end]]),token_start,token_end))


# In[ ]:


if __name__ == '__main__':
    for line in open('UM-Corpus.en.200k.tagged.txt'):

#     for line in sys.stdin:
        parse = eval(line.strip())
        parse = [ [y.split() for y in x]  for x in parse ]
        print ('\n'+' '.join([' '.join(x) for x in parse[0] ]))
        
        to_token = ' '.join([' '.join(x) for x in parse[0] ]).split(' ')
# print(to_token)

        for start, end in sentence_to_ngram(*parse):

# for n, start, end in enumerate(sentence_to_ngram(*parse)):
            pat = ngram_to_pat(*parse, start, end)
            if pat:
                word = ngram_to_head(*parse, start, end)
                temp_token = ' '.join([' '.join(x) for x in parse[0][start:end]]).split(' ')
                len_token = len(temp_token)
#         print(len_token)
                for n, t in enumerate(to_token):
#             print(temp_token)
#             print(to_token[n:n+len_token+1])
                    if temp_token == to_token[n:n+len_token]:
                        token_start = n
                        token_end = n+len_token-1
#                 print(n,token_start,token_end)
#         for i in range(start,end+1):
#             print(i)
        
                        print('%s\t%s\t%s\t%d\t%d' %(word,pat,' '.join([' '.join(x) for x in parse[0][start:end]]),token_start,token_end))
                        continue


# In[41]:


# line = [('all that', 'remains', 'for', 'me', 'to', 'do is', 'to', 'say', 'good-bye', '.'), ('all that', 'remain', 'for', 'me', 'to', 'do be', 'to', 'say', 'good-bye', '.'), ('PDT DT', 'VBZ', 'IN', 'PRP', 'TO', 'VB VBZ', 'TO', 'VB', 'NN', '.'), ('I-NP H-NP', 'H-VP', 'H-PP', 'H-NP', 'H-TO', 'I-VP H-VB', 'H-TO', 'H-VP', 'H-NP', 'O')]
# line = str(line)


# In[42]:


# parse = eval(line.strip())
# parse = [ [y.split() for y in x]  for x in parse ]
# print ('\n'+' '.join([' '.join(x) for x in parse[0] ]))



# for start, end in sentence_to_ngram(*parse):

#     pat = ngram_to_pat(*parse, start, end)
#     if pat:
#         word = ngram_to_head(*parse, start, end)
#         tag = pat.split(' ')[0]
#         w_tag = word+'-'+tag
#         if w_tag.lower() in akl:
#             print('%s\t%s\t%s' %(w_tag,pat,'\n'+' '.join([' '.join(x) for x in parse[0] ])))

