import numpy as np
import pandas as pd
import os
from tqdm import tqdm

def run(config):
    dir_route = "Ednet/KT1"
    dirs = os.listdir(dir_route)
    response_data = dict()
    stu_response_data = dict() 
    stu_num = np.random.choice(np.arange(784309), size=config['stu_num'], replace=False)
    least_respone_num = config['least_respone_num']
    q_data = pd.read_csv("Ednet/content/questions.csv")
    original_stu_map = dict()
    original_cnt_stu = 0

    for dir in dirs:
        original_stu_map[original_cnt_stu] = dir
        original_cnt_stu += 1

    for stu in tqdm(stu_num, desc='Filter student'):
        stu_data = pd.read_csv(os.path.join(dir_route, original_stu_map[stu]))
        for data in stu_data.values:
            tmp_data = (stu, data[2])
            response_data[tmp_data] = (q_data.loc[q_data["question_id"] == data[2]]["correct_answer"].iloc[0] == data[3])

    for key, value in response_data.items():
        if key[0] not in stu_response_data:
            stu_response_data[key[0]] = []
        stu_response_data[key[0]].append([int(key[0]), key[1], int(value)])
    
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
                for concept in q_data.loc[q_data["question_id"] == data[1]]['tags'].iloc[0].split(';'):
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
                for concept in q_data.loc[q_data["question_id"] == data[1]]['tags'].iloc[0].split(';'):
                    q_matrix[question_map[data[1]]][concept_map[concept]] = 1


    print('Final student number: {}, Final question number: {}, Final concept number: {}, Final response number: {}'.format(cnt_stu, cnt_question, cnt_concept, len(TotalData)))
    np.savetxt('EdNet/EdNet_TotalData.csv', TotalData, delimiter=',')
    np.savetxt('EdNet/EdNet_q.csv', q_matrix, delimiter=',')