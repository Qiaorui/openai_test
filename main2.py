import openai

openai.api_key = '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'

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
        {"role": "system", "content": "你是一个职业数据分析师"},
        {"role": "user", "content": '现在有一张数据表格，表头字段名分别为【date, 商品，门店，销量，销售额，库存，销量预测值】，主键是【date, 商品，门店】。' \
               '请推测这可能是什么业务下的数据？给出3个可能的业务类型以及它们的概率。' \
               '如果你是这个业务领域的专家或者主管，你最关心的5个最重要的业务指标是什么？ 若考虑我们已有的数据，可以在看板上展示哪些重要指标？'\
               '这些看板数据分别通过什么SQL进行构建？它们分别适合用什么类型的图表？' \
               '请按以下格式进行回答：' \
               '【业务】' \
               ' 1. XXX  概率XX%' \
               ' 2. ...' \
               '【业务指标】' \
               ' 1. XXX' \
               ' ...' \
               '【可以展示的指标】' \
               ' 1. XXX' \
               '    SQL CODE: YYY ; 推荐图表类型:ZZZ' \
               ' ...'},
    ]
)

print(response['choices'][0]['message']['content'])
print(response['usage'])
