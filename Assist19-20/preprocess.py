import numpy as np
import pandas as pd
from tqdm import tqdm

def run(config):
    data_response = pd.read_csv('Assist19-20/2019-2020_school_year/plogs.csv')
    q_data = pd.read_csv('Assist19-20/2019-2020_school_year/pdets.csv')

    data_response = data_response.dropna(subset=['correct'])
    q_data = q_data.dropna(subset=['skills'])
    data_response = data_response.loc[data_response['problem_id'].isin(q_data['problem_id'].unique())]

    response_data = dict()
    stu_response_data = dict() 
    stu_num = np.random.choice(np.arange(163097), size=config["stu_num"], replace=False)
    least_respone_num = config["least_respone_num"]
    original_stu_map = dict()
    original_cnt_stu = 0

    for stu in data_response["student_id"].unique():
        original_stu_map[original_cnt_stu] = stu
        original_cnt_stu += 1
    
    for stu in tqdm(stu_num, desc='Filter student'):
        stu_data = data_response.loc[data_response["student_id"] == original_stu_map[stu]]
        for data in stu_data.values:
            tmp_data = (stu, data[3])
            response_data[tmp_data] = (data[11] == True)

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
                for concept in q_data.loc[q_data["problem_id"] == data[1]]['skills'].iloc[0].split(','):
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
                for concept in q_data.loc[q_data["problem_id"] == data[1]]['skills'].iloc[0].split(','):
                    q_matrix[question_map[data[1]]][concept_map[concept]] = 1

    print('Final student number: {}, Final question number: {}, Final concept number: {}, Final response number: {}'.format(cnt_stu, cnt_question, cnt_concept, len(TotalData)))
    np.savetxt('Assist19-20/Assist19-20_TotalData.csv', TotalData, delimiter=',')
    np.savetxt('Assist19-20/Assist19-20_q.csv', q_matrix, delimiter=',')