import re

import openai
import pandas as pd

openai.api_key = ''

import itertools


def search_primary_key_from_df(df, candidates_cols=None, na_threshold=0, max_dim=None):
    # 默认所有列为候选
    if candidates_cols is None:
        candidates_cols = df.columns
    if max_dim is None:
        max_dim = len(candidates_cols) - 1

    # 排除不合法的列，即数据类型不是数值或字符串的列，或na值比例超过na_threshold的列
    valid_cols = []
    for col in candidates_cols:
        if df[col].dtype == float:
            continue
        na_percentage = df[col].isna().sum() / df.shape[0]
        if na_percentage <= na_threshold:
            valid_cols.append(col)

    # primary key搜索
    results = []
    for i in range(1, max_dim + 1):
        for cols in itertools.combinations(valid_cols, i):
            unique_values = df[list(cols)].drop_duplicates().shape[0]
            if unique_values == df.shape[0]:
                results.append((list(cols)))
        if results:
            break

    return results


def get_business_industry_name(cols, pk):
    cols = ",".join(cols)
    pk = ','.join(pk)

    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": "你是一个职业数据分析师"},
            {"role": f"user", "content": f'现在有一张数据表格，表头字段名分别为[{cols}]，主键是[{pk}]。' \
                                         '这是什么行业/业务下的数据？给出3个可能的类型以及它们的概率。按以下格式给予回复：' \
                                         '这张数据表格可能是[xxx]下的数据，其中' \
                                         '1. 业务类型：XXX, 概率:YY%, 原因:blablbla'},
        ]
    )

    msg = response['choices'][0]['message']['content']
    business = re.findall(r'这张数据表格可能是(.*)下的数据', msg)[0]

    return msg, business


def get_general_business_insight(business_name):
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": f"你是一个从事{business_name}的职业数据分析师"},
            {"role": "user", "content": '这个行业都有哪几个业务流程阶段？每个阶段的核心数据指标都有哪些？'},
        ])

    return response['choices'][0]['message']['content']


def get_bi_board_suggestion(business_name, business_insight, data_name, cols, pk):
    cols = ",".join(cols)
    pk = ','.join(pk)
    response = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        temperature=0,
        messages=[
            {"role": "system", "content": f"你是一个从事{business_name}的职业数据分析师"},
            {"role": "user", "content": '这个行业都有哪几个业务流程阶段？每个阶段的核心数据指标都有哪些？'},
            {'role': 'assistant', 'content': business_insight},
            {'role': 'user', 'content': f'现在有一张数据表格，表名：{data_name}, 表头字段名分别为[{cols}]，主键是[{pk}]。' \
                                        '这可能是处于什么业务流程阶段的数据？ 若考虑我们已有的数据，可以在看板上展示哪些重要指标？' \
                                        '这些看板数据分别通过什么SQL进行构建？它们分别适合用什么类型的图表？以及使用这个图表的话，各个参数分别是SQL结果的哪些数据字段？' \
                                        '请按以下格式进行回答：' \
                                        '【业务流程】业务流程名字' \
                                        '【可以展示的指标】' \
                                        ' 1. 指标名， SQL：sql代码 图表类型:图标类型名字 参数: xy各个轴的字段名' \
                                        ' ...'}
        ]
    )

    bi_suggestion = response['choices'][0]['message']['content']
    return bi_suggestion


def looklook(f):
    # f为文件名，需要根据文件对应的后缀将其读取并创建为pd.dataframe。对于不支持的文件类型返回文件类型错误
    data_name, f_type = f.split('.')

    print('开始加载数据')

    if f_type == 'csv':
        df = pd.read_csv(f)

    if 'Col0' in df.columns:
        df.drop('Col0', axis=1, inplace=True)

    if 'Unnamed: 0' in df.columns:
        df.drop('Unnamed: 0', axis=1, inplace=True)

    print(df.describe())
    print('数据加载完毕，开始检测主键')

    pk = search_primary_key_from_df(df)[0]

    print('主键检测出来为:', pk)

    print('让我们来康康这个数据是个啥')

    cols = list(df.columns)
    msg, business = get_business_industry_name(cols, pk)
    print('*' * 40)
    print(msg)
    business_insight = get_general_business_insight(business)
    print('*' * 40)
    print(business_insight)

    bi_suggestion = get_bi_board_suggestion(business, business_insight, data_name, cols, pk)
    print('*' * 40)
    print(bi_suggestion)
    print('*' * 40)
    print('程序结束')
