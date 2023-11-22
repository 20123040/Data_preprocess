# Data_preprocess

## 数据集

XES3G5M: https://github.com/ai4ed/XES3G5M

EdNet: https://github.com/riiid/ednet

EDM2023-CUP: https://www.kaggle.com/competitions/edm-cup-2023/data

Assist19-20: https://osf.io/q7zc5/

Assist20-21: https://osf.io/7cgav/

将上述数据集下载过后解压至对应文件夹当中

## 运行

1. 使用 `python main.py --dataset <数据集名称> --stu_num <学生数量> --least_respone_num <每个学生最少的做题数目>`

2. 集中运行可以修改 `run.sh` 中命令

## 数据集TIPS
1. XES3G5M: 质量比较高的数据集，主要用到的kc_level文件夹里面的数据，由于是KT的数据集，内部大部分学生都有一个完整的200答题序列，表内每个题目的知识点只给叶子节点，完整的知识点路径可以在metadata文件夹内部的question.json文件中找到

2. EdNet: 只用到了KT1这个文件夹的作答记录，其他三个文件夹内部有更多的拓展信息，content中的question.csv记录了问题和知识点的具体信息,由于该数据集每个学生就是一个csv文件，所以在读取学生时会有大量的文件IO导致读取较慢

3. EDM2023-CUP: 是一个基于Assist的数据集，数据集内部结构与Assist大致相似，主要用到的training_unit_test_scores.csv和problem_details.csv两个文件，由于其中training_unit_test_scores.csv中是以assignment为基本单位的三元组，所以学生必须在problem_details.csv中寻找，该数据集将整体数据划分为训练和测试集两部分，测试集没有回答对错的记录所以无法使用，所以在前期清洗时，需要先将可用的assignment_id筛选出来，同时采集中的一些影响，prolem_details.csv并没有记录到所有的problem信息，所以前期也必须同时筛选出可用的problem_id

4. Assist19-20:数据集主要有完整一学年的数据和分为上半年和下半年的分割数据，这里直接用了完整数据，主要用到的是plogs.csv和pdets.csv两个表格，这个数据集也存在pdets内部没有记录到所有的problem信息同时并不是每个problem都有对应的知识点信息，所以前期也要筛选出可用的problem_id

5. Assist20-21:该数据集直接将一学年的数据分为了四个季度分开打包,所以比Assist19-20多一步合并操作，作答记录作concat，问题信息作merge，后续处理跟Assist19-20类似

