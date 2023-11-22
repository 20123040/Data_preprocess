import numpy as np
import pandas as pd
from tqdm import tqdm

def run(config):
    data_response_1 = pd.read_csv('Assist20-21/aug_to_oct/plogs.csv')
    data_response_2 = pd.read_csv('Assist20-21/feb_to_apr/plogs.csv')
    data_response_3 = pd.read_csv('Assist20-21/may_to_june/plogs.csv')
    data_response_4 = pd.read_csv('Assist20-21/nov_to_jan/plogs.csv')

    q_data_1 = pd.read_csv('Assist20-21/aug_to_oct/pdets.csv')[['problem_id','skills']]
    q_data_2 = pd.read_csv('Assist20-21/feb_to_apr/pdets.csv')[['problem_id','skills']]
    q_data_3 = pd.read_csv('Assist20-21/may_to_june/pdets.csv')[['problem_id','skills']]
    q_data_4 = pd.read_csv('Assist20-21/nov_to_jan/pdets.csv')[['problem_id','skills']]

    data_response = pd.concat([data_response_1,data_response_2, data_response_3, data_response_4])
    # data_response = pd.concat([data_response_1,data_response_2])
    q_data = pd.merge(q_data_1, q_data_2, how = 'outer', on = ['problem_id', 'skills'])
    q_data = pd.merge(q_data, q_data_3, how = 'outer', on = ['problem_id', 'skills'])
    q_data = pd.merge(q_data, q_data_4, how = 'outer', on = ['problem_id', 'skills'])

    data_response = data_response.dropna(subset=['correct'])
    q_data = q_data.dropna(subset=['skills'])
    data_response = data_response.loc[data_response['problem_id'].isin(q_data['problem_id'].unique())]

    response_data = dict()
    stu_response_data = dict() 
    stu_num = np.random.choice(np.arange(len(data_response['student_id'].unique())), size=config['stu_num'], replace=False)
    least_respone_num = config['least_respone_num']
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
    np.savetxt('Assist20-21/Assist20-21_TotalData.csv', TotalData, delimiter=',')
    np.savetxt('Assist20-21/Assist20-21_q.csv', q_matrix, delimiter=',')