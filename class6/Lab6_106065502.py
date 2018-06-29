
# coding: utf-8

# In[1]:


from collections import Counter, defaultdict
from pprint import pprint
import fileinput


akl = dict( [ (x+'-n', True) for x in 'focus, ability, absence, account, achievement, act, action, activity, addition, adoption, adult, advance, advantage, advice, age, aim, alternative, amount, analogy, analysis, application, approach, argument, aspect, assertion, assessment, assistance, association, assumption, attempt, attention, attitude, author, awareness, balance, basis, behaviour, behavior, being, belief, benefit, bias, birth, capacity, case, category, cause, centre, challenge, change, character, characteristic, choice, circumstance, class, classification, code, colleague, combination, commitment, committee, communication, community, comparison, complexity, compromise, concentration, concept, conception, concern, conclusion, condition, conduct, conflict, consensus, consequence, consideration, constraint, construction, content, contradiction, contrast, contribution, control, convention, correlation, country, creation, crisis, criterion, criticism, culture, damage, data, debate, decision, decline, defence, defense, definition, degree, demand, description, destruction, determination, development, difference, difficulty, dilemma, dimension, disadvantage, discovery, discrimination, discussion, distinction, diversity, division, doctrine, effect, effectiveness, element, emphasis, environment, error, essence, establishment, evaluation, event, evidence, evolution, examination, example, exception, exclusion, existence, expansion, experience, experiment, explanation, exposure, extent, extreme, fact, factor, failure, feature, female, figure, finding, force, form, formation, function, future, gain, group, growth, guidance, guideline, hypothesis, idea, identity, impact, implication, importance, improvement, increase, indication, individual, influence, information, insight, instance, institution, integration, interaction, interest, interpretation, intervention, introduction, investigation, isolation, issue, kind, knowledge, lack, learning, level, likelihood, limit, limitation, link, list, literature, logic, loss, maintenance, majority, male, manipulation, mankind, material, means, measure, medium, member, method, minority, mode, model, motivation, movement, need, network, norm, notion, number, observation, observer, occurrence, operation, opportunity, option, organisation, organization, outcome, output, paper, parallel, parent, part, participant, past, pattern, percentage, perception, period, person, personality, perspective, phenomenon, point, policy, population, position, possibility, potential, practice, presence, pressure, problem, procedure, process, production, programme, program, progress, property, proportion, proposition, protection, provision, publication, purpose, quality, question, range, rate, reader, reality, reason, reasoning, recognition, reduction, reference, relation, relationship, relevance, report, representative, reproduction, requirement, research, resistance, resolution, resource, respect, restriction, result, review, rise, risk, role, rule, sample, scale, scheme, scope, search, section, selection, sense, separation, series, service, set, sex, shift, significance, similarity, situation, skill, society, solution, source, space, spread, standard, statistics, stimulus, strategy, stress, structure, subject, success, summary, support, survey, system, target, task, team, technique, tendency, tension, term, theme, theory, tolerance, topic, tradition, transition, trend, type, uncertainty, understanding, unit, use, validity, value, variation, variety, version, view, viewpoint, volume, whole, work, world'.split(', ') ]+            [ (x+'-v', True)  for x in 'accept, account, achieve, acquire, act, adapt, adopt, advance, advocate, affect, aid, aim, allocate, allow, alter, analyse, analyze, appear, apply, argue, arise, assert, assess, assign, associate, assist, assume, attain, attempt, attend, attribute, avoid, base, be, become, benefit, can, cause, characterise, characterize, choose, cite, claim, clarify, classify, coincide, combine, compare, compete, comprise, concentrate, concern, conclude, conduct, confine, conform, connect, consider, consist, constitute, construct, contain, contrast, contribute, control, convert, correspond, create, damage, deal, decline, define, demonstrate, depend, derive, describe, design, destroy, determine, develop, differ, differentiate, diminish, direct, discuss, display, distinguish, divide, dominate, effect, eliminate, emerge, emphasize, employ, enable, encounter, encourage, enhance, ensure, establish, evaluate, evolve, examine, exceed, exclude, exemplify, exist, expand, experience, explain, expose, express, extend, facilitate, fail, favour, favor, finance, focus, follow, form, formulate, function, gain, generate, govern, highlight, identify, illustrate, imply, impose, improve, include, incorporate, increase, indicate, induce, influence, initiate, integrate, interpret, introduce, investigate, involve, isolate, label, lack, lead, limit, link, locate, maintain, may, measure, neglect, note, obtain, occur, operate, outline, overcome, participate, perceive, perform, permit, pose, possess, precede, predict, present, preserve, prevent, produce, promote, propose, prove, provide, publish, pursue, quote, receive, record, reduce, refer, reflect, regard, regulate, reinforce, reject, relate, rely, remain, remove, render, replace, report, represent, reproduce, require, resolve, respond, restrict, result, retain, reveal, seek, select, separate, should, show, solve, specify, state, stimulate, strengthen, stress, study, submit, suffer, suggest, summarise, summarize, supply, support, sustain, tackle, tend, term, transform, treat, undermine, undertake, use, vary, view, write, yield'.split(', ') ]+            [ (x+'-adj', True) for x in 'absolute, abstract, acceptable, accessible, active, actual, acute, additional, adequate, alternative, apparent, applicable, appropriate, arbitrary, available, average, basic, central, certain, clear, common, competitive, complete, complex, comprehensive, considerable, consistent, conventional, correct, critical, crucial, dependent, detailed, different, difficult, distinct, dominant, early, effective, equal, equivalent, essential, evident, excessive, experimental, explicit, extensive, extreme, far, favourable, favorable, final, fixed, following, formal, frequent, fundamental, future, general, great, high, human, ideal, identical, immediate, important, inadequate, incomplete, independent, indirect, individual, inferior, influential, inherent, initial, interesting, internal, large, late, leading, likely, limited, local, logical, main, major, male, maximum, mental, minimal, minor, misleading, modern, mutual, natural, necessary, negative, new, normal, obvious, original, other, overall, parallel, partial, particular, passive, past, permanent, physical, positive, possible, potential, practical, present, previous, primary, prime, principal, productive, profound, progressive, prominent, psychological, radical, random, rapid, rational, real, realistic, recent, related, relative, relevant, representative, responsible, restricted, scientific, secondary, selective, separate, severe, sexual, significant, similar, simple, single, so-called, social, special, specific, stable, standard, strict, subsequent, substantial, successful, successive, sufficient, suitable, surprising, symbolic, systematic, theoretical, total, traditional, true, typical, unique, unlike, unlikely, unsuccessful, useful, valid, valuable, varied, various, visual, vital, wide, widespread'.split(', ') ]+            [ (x+'-adv', True) for x in 'above, accordingly, accurately, adequately, also, approximately, at best, basically, clearly, closely, commonly, consequently, considerably, conversely, correctly, directly, effectively, e.g., either, equally, especially, essentially, explicitly, extremely, fairly, far, for example, for instance, frequently, fully, further, generally, greatly, hence, highly, however, increasingly, indeed, independently, indirectly, inevitably, initially, in general, in particular, largely, less, mainly, more, moreover, most, namely, necessarily, normally, notably, often, only, originally, over, partially, particularly, potentially, previously, primarily, purely, readily, recently, relatively, secondly, significantly, similarly, simply, socially, solely somewhat, specifically, strongly, subsequently, successfully, thereby, therefore, thus, traditionally, typically, ultimately, virtually, wholly, widely'.split(', ') ] )





# In[4]:


def read_ngrams():
    skipBigramDistance = defaultdict(lambda: defaultdict(lambda: Counter()))
#     skipBigramDistance = defaultdict(lambda: defaultdict(lambda: []))

    skipBigramExample = defaultdict(lambda: defaultdict(lambda: defaultdict(lambda: Counter())))

#     bigram = open('citeseerx.ngms','r')
    
    for line in fileinput.input():
#     for line in bigram:
        ngram, count = line.split('\t', 1)
        token = ngram.split(' ')
        
        skipBigramDistance[token[0]][token[-1]][len(token)-1] += int(count)
        skipBigramDistance[token[-1]][token[0]][-(len(token)-1)] += int(count)
#         skipBigramDistance[token[-1]][token[0]][-(len(token)-1)].append()

        skipBigramExample[token[0]][token[-1]][len(token)-1][ngram] = int(count)
        skipBigramExample[token[-1]][token[0]][-(len(token)-1)][ngram] = int(count)
        
#         print(line.strip().split(' ')[0])

    return (skipBigramDistance, skipBigramExample)

def grades_sum(my_list): 
    total = 0 
    for grade in my_list:  
        total += grade 
    return total 
    
def grades_average(my_list): 
    sum_of_grades = grades_sum(my_list) 
    average = sum_of_grades / len(my_list) 
    return average 
       
def grades_variance(my_list, average): 
    variance = 0 
    for i in my_list: 
        variance += (average - i) ** 2 
#         variance += (average - my_list[i]) ** 2 
    return variance / len(my_list)


# In[9]:


skipBigramDistance, skipBigramExample = read_ngrams()
# skipBigramExample['focus-n']['paper-n']
# skipBigramDistance['focus-n']['paper-n']
# print(skipBigramDistance)

coll_info = defaultdict(lambda: [])
C1 = []
C2 = []
C3 = defaultdict(lambda: defaultdict())
for i in skipBigramDistance:
    c = {}
    for k in skipBigramDistance[i]:
        c[k] = grades_sum(skipBigramDistance[i][k].values())
    coll_info[i].append(c)
    coll_info[i].append(grades_average(coll_info[i][0].values()))
    coll_info[i].append(grades_variance(list(coll_info[i][0].values()),coll_info[i][1]))

for j in akl.keys():
    try:
        for m in coll_info[j][0]:
#         print(coll_info["focus-n"])
            try:
                if coll_info[j][0][m] - coll_info[j][1]/coll_info[j][2] > 1:
#                 print(coll_info[j][0][m] - coll_info[j][1]/coll_info[j][2] )
                    C1.append([j,m])
            except:
                pass
    except:
        print(j,coll_info[j])
#         if coll_info[j][0][m] - coll_info[j][1]/coll_info[j][2] > 1:
#             C1.append([j,m])
for i,j in C1:
    if coll_info[i][2]>10:
        C2.append([i,j])

for i, j in C2:
    for l in skipBigramDistance[i][j]:
        if skipBigramDistance[i][j][l] > coll_info[i][1]+1*coll_info[i][2]**0.5:
            C3[i][j] = l
        


# In[18]:


# for i, j in C2:
#     for l in skipBigramDistance[i][j]:
#         print(l)
#         if skipBigramDistance[i][j][l] > coll_info[i][1]+1*coll_info[i][2]**0.5:
#             C3[i][j] = l
# print(C3['focus-n']['on-prep'])


# In[20]:


# for i in coll_info:
#     pprint(coll_info[i][0])
# print(C3['focus-n'])
for text in C3.keys():
    print(text)
    for i in C3[text]:
        l = C3[text][i]
#         print(l)
        print(i,skipBigramDistance[text][i][l],             sorted(skipBigramExample[text][i][l].items(),key=lambda x: -x[1])[0])
        
#     pre = sorted(list(skipBigramDistance[text].items()),key=lambda x: -sum(x[1].values()))[:18]
#     for i in pre:
#         max_d = sorted(i[1].items(),key=lambda x: -x[1])[:1][0][0]
# #             print(max_d)
#         max_s = sorted(i[1].items(),key=lambda x: -x[1])[:1][0]
#         print(i[0],end=' ')
#         print(max_s,end=' ')
            
#             pprint(sorted(i[1].items(),key=lambda x: -x[1])[:1][0])
#                   sorted(skipBigramExample[text][i[0]][max_d].items(),key=lambda x: -x[1])[0])
#                    sorted(i[1].items(),key=lambda x: -x[1])[:1],\
#         print(sorted(skipBigramExample[text][i[0]][max_d].items(),key=lambda x: -x[1])[0])
    print('\n')


# In[3]:


# if __name__ == '__main__':

#     skipBigramDistance, skipBigramExample = read_ngrams()
#     for text in C3.keys():
#         print(text,'\t','18')
#         pre = sorted(list(skipBigramDistance[text].items()),key=lambda x: -sum(x[1].values()))[:18]
#         for i in pre:
#             max_d = sorted(i[1].items(),key=lambda x: -x[1])[:1][0][0]
# #             print(max_d)
#             max_s = sorted(i[1].items(),key=lambda x: -x[1])[:1][0]
#             print(i[0],end=' ')
#             print(max_s,end=' ')
            
# #             pprint(sorted(i[1].items(),key=lambda x: -x[1])[:1][0])
# #                   sorted(skipBigramExample[text][i[0]][max_d].items(),key=lambda x: -x[1])[0])
# #                    sorted(i[1].items(),key=lambda x: -x[1])[:1],\
#             print(sorted(skipBigramExample[text][i[0]][max_d].items(),key=lambda x: -x[1])[0])
#         print('\n')

        

