import json
import re
import pandas as pd

with open('问题分类.json', 'r') as f:
    json_cls = json.load(f)

def extrat_classification(genetext,json_cls):
    lev1 = json_cls.keys()
    lev2 = [json_cls[key] for key in lev1]
    lev2 = [item for sublist in lev2 for item in sublist]
    # match text with lev2
    matched_cls = re.findall(rf"({'|'.join(lev2)})", genetext)
    if matched_cls:
        if len(matched_cls) == 1:
            return matched_cls
        else:
            # check if in the same lev1
            if any(all(cls in item for cls in matched_cls) for item in json_cls.values()):
                return matched_cls
            else:
                return None
    else:
        return None
    
                

with open('Data/dep_dis_ques_240206_with_q_c.jsonl', 'r') as f:
    lines = f.readlines()
    json_list = [json.loads(line) for line in lines]
for obj in json_list:
    genetext = obj['gpt_gene']
    extracted_text = extrat_classification(genetext,json_cls)
    obj['extracted_text'] = extracted_text
    with open('dep_dis_ques_240206_with_q_c_e.jsonl', 'a') as file:
        file.write(json.dumps(obj, ensure_ascii=False) + '\n')

df = pd.DataFrame(json_list)
df.to_csv('dep_dis_ques_240206_with_q_c_e.csv', index=False, encoding='utf-8-sig')