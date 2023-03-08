import openai

openai.api_key = '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'

data_profile = '假设你是一个职业数据分析师，现在拿到一张数据表格，表头字段名分别为【date, 商品，门店，销量，销售额，库存，销量预测值】，主键是【date, 商品，门店】。' \
               '请推测这是什么业务下的数据？忽视我们已有的数据，此类业务5个最重要的业务指标是什么？'

response = openai.Completion.create(
    model="text-davinci-003",
    prompt=data_profile,
    temperature=0,
    max_tokens=1000
)

print(response)

response = openai.ChatCompletion.create(
    model="gpt-3.5-turbo",
    temperature=0,
    messages=[
        {"role": "system", "content": "You are a data analyst."},
        {"role": "user", "content": "Given Data with schema table(商品,商品名,属性,价格,开发日期,经理,种类), primary keys are (商品). "
                                    "What kind of business is performed and what are the 5 top important KPI of this type of business. Respond in Chinease"},
        {"role": "assistant", "content": "零售行业或快销行业。主要指标为销售额,有货率,库存周转率,滞销比,服务水平率"},
        {"role": "user", "content": "Given Data with schema table(date, 商品，门店，销量，销售额，库存，销量预测值), primary keys are (date, 商品，门店). "
                                    "What kind of business is performed and what are the 5 top important KPI of this type of business. Respond in Chinease"}
    ]
)
print(response)
