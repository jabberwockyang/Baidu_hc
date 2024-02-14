import openai
import os
import json
import time
OPENAI_API_KEY = "ghhhkhkghfghvkhf"
openai.api_key = OPENAI_API_KEY
completion = openai.ChatCompletion.create(
      model='gpt-3.5-turbo-16k-0613',
      messages=[
        {"role": "user", "content": 'hello'}])
print(completion.choices[0].message.content)

with open('dep_dis_ques_240206_with_q.json', 'r') as f:
    json_list = json.load(f)
if os.path.exists('dep_dis_ques_240206_with_q_c.jsonl'):
    with open('dep_dis_ques_240206_with_q_c.jsonl','r') as f2:
        done_data = f2.readlines()
        done_data = [json.loads(line) for line in done_data]
        done_request = [obj['question'] for obj in done_data]
else:
    done_request = []


for obj in json_list:
    if obj['question'] in done_request:
        continue
    completion = openai.ChatCompletion.create(
      model='gpt-3.5-turbo-16k-0613',
      messages=[
        {"role": "user", "content": obj['prompt']}])
    obj['gpt_gene'] = completion.choices[0].message.content
    time.sleep(2)
    with open('dep_dis_ques_240206_with_q_c.jsonl', 'a') as file:
        file.write(json.dumps(obj, ensure_ascii=False) + '\n')



