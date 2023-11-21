import numpy as np
import pandas as pd
import json
from tqdm import tqdm

def run(config):
    data_train = pd.read_csv('XES3G5M/XES3G5M/kc_level/train_valid_sequences.csv')
    data_test = pd.read_csv('XES3G5M/XES3G5M/kc_level/test.csv')

    with open(f'XES3G5M/XES3G5M/metadata/questions.json', 'r') as file:
        q_data = json.load(file)
    
    response_data = dict()
    stu_response_data = dict() 
    stu_num = np.random.choice(np.arange(18066), size=config['stu_num'], replace=False)
    least_respone_num = config['least_respone_num']


    for stu in tqdm(stu_num, desc='Filter student'):
        for data in data_train.loc[data_train['uid'] == stu].values:
            uid, questions, responses, selectmasks = data[1], data[2].split(','), data[4].split(','), data[6].split(',')
            for i in range(len(questions)):
                if selectmasks[i] == '-1':
                    break
                tmp_data = (uid, questions[i])
                response_data[tmp_data] = responses[i]
        
        for data in data_test.loc[data_test['uid'] == stu].values:
            uid, questions, responses = data[1], data[2].split(','), data[4].split(',')
            for i in range(len(questions)):
                tmp_data = (uid, questions[i])
                response_data[tmp_data] = responses[i]

    for key, value in response_data.items():
        if key[0] not in stu_response_data:
            stu_response_data[key[0]] = []
        stu_response_data[key[0]].append([int(key[0]), int(key[1]), int(value)])

    stu_map = dict()
    cnt_stu = 0
    question_set = set()
    cnt_question = 0
    question_map = dict()
    concept_set = set()
    cnt_concept = 0
    concept_map = dict()

    for key, value in tqdm(stu_response_data.items(), desc='Remap student_id, question_id and concept_id'):
        if len(value) >= least_respone_num:
            stu_map[key] = cnt_stu
            cnt_stu += 1
            for data in value:
                question_set.add(data[1])
                for concept in q_data[str(data[1])]['kc_routes'][0].split('----'):
                    concept_set.add(concept)

    
    for question in question_set:
        question_map[question] = cnt_question
        cnt_question += 1
    
    for concept in concept_set:
        concept_map[concept] = cnt_concept
        cnt_concept += 1
    
    TotalData = []
    q_matrix = np.zeros((cnt_question, cnt_concept))
    
    for key, value in tqdm(stu_response_data.items(), desc='Construct final data'):
        if len(value) >= least_respone_num:
            for data in value:
                TotalData.append([stu_map[data[0]], question_map[data[1]], data[2]])
                for concept in q_data[str(data[1])]['kc_routes'][0].split('----'):
                    q_matrix[question_map[data[1]]][concept_map[concept]] = 1
    

    print('Final student number: {}, Final question number: {}, Final concept number: {}, Final response number: {}'.format(cnt_stu, cnt_question, cnt_concept, len(TotalData)))
    np.savetxt('XES3G5M/XES3G5M_TotalData.csv', TotalData, delimiter=',')
    np.savetxt('XES3G5M/XES3G5M_q.csv', q_matrix, delimiter=',')