import json
import pandas

with open('dep_dis_ques_240206_with_q.jsonl', 'r') as f:
    lines = f.readlines()
    json_list = [json.loads(line) for line in lines]

# Filter out diseases with no questions of interest
json_list2 = [disease for disease in json_list if disease['ques_of_int'] != []]
labels ="['疾病介绍', '疾病之间的区别', '发病机制', '发病诱因', '症状', '就诊科室', '检验检查', '诊断依据', '治疗方法', '急救方法','治疗的作用机制', '日常护理和注意事项', '自限性', '良恶性', '并发症', '影响生活质量', '影响寿命', '其他预后', '流行病学', '日常习惯预防', '定期体检预防', '早期发现预防']"
example = '**问题**：腋毛癣能自愈吗？**分类**:自限性'
df= pandas.DataFrame(columns=['department', 'disease', 'section','question','href'])
newlist = []
for disease in json_list2:
    for ques in disease['ques_of_int']:
        new_obj = {'department': disease['department'], 
                        'disease': disease['disease'], 
                        'section': ques['perspective'], 
                        'question': ques['question_title'], 
                        "prompt":f"请从以下标签中选取标签{labels}，对问题做分类。\n\n这是一个例子：{example}\n\n **问题**：{ques['question_title']}\n\n**分类**：\n",
                        'href': disease['href']}
        newlist.append(new_obj)
df = pandas.DataFrame(newlist)
df = df.sort_values(by=['department'])
df.to_csv('dep_dis_ques_240206_with_q.csv', index=False, encoding='utf-8-sig')
        
with open('dep_dis_ques_240206_with_q.json', 'w') as f:
    json.dump(newlist, f, ensure_ascii=False, indent=4)


