import json
import time
import os
import random
from DrissionPage import ChromiumPage
from DrissionPage import ChromiumOptions
from DrissionPage import ChromiumOptions, ChromiumPage

co = ChromiumOptions()
co.incognito()  # 匿名模式
co.headless()  # 无头模式
co.set_argument('--no-sandbox')  # 无沙盒模式
co.no_imgs(True).mute(True)

current_path = "new_folder"
if not os.path.exists(current_path):
    os.makedirs(current_path)

while True:
    try:
        t0 = time.time()
        with open('Data/dep_dis_href_240202.jsonl', 'r') as f:
            lines = f.readlines()
            json_list = [json.loads(line) for line in lines]

        # Load the log file to check hrefs that has been scraped
        if os.path.exists(os.path.join(current_path,'log.txt')):
            with open(os.path.join(current_path,'log.txt'), 'r') as f:
                lines = f.readlines()
                href_list = [line.split(',')[0] for line in lines]
        else:
            href_list = []

        #remove the hrefs that have been scraped
        json_list = [disease for disease in json_list if disease['href'] not in href_list]

        if len(json_list) == 0:
            break
        
        disease_obj = json_list[0]
        href = disease_obj['href'] 
        
        t1 = time.time()
        print('href ready. time cost', t1-t0)
        page = ChromiumPage(co)
        page.get(href)
        # 输入文本

        # Use the refined XPath to locate the elements
        titles_xpath = "/html//div[contains(@class,'health-dict__overview__text health-dict__overview__texts__text')]"
        try:
            overview_texts = page.eles('xpath='+ titles_xpath, timeout=5)
        except Exception as e:
            print(e)
            continue 
        t2 = time.time()
        print('open the page and get tabs element. time cost', t2-t1)
        qobj_list = []
        # Loop over each overview text element
        for overview_text in overview_texts:
            # Extract the title for each level 1 tag
            title_element_xpath = ".//div[@class = 'health-dict__overview__text__level1-tag__title']"

            title_element = overview_text.ele('xpath='+ title_element_xpath, timeout=1)
            
            # Find and print all question titles within this level 1 tag
            questions_xpath = ".//div[@class='health-dict__overview__text__level1-tag__questions__question']"
            question_elements = overview_text.eles('xpath='+ questions_xpath, timeout=1)
            

            if question_elements:
                for question_element in question_elements:
                
                    question_titles_xpath = "./div[@class = 'health-dict__overview__text__level1-tag__questions__question__title']"
                    question_answer_xpath = "./div[@class = 'health-dict__overview__text__level1-tag__questions__question__content']"
                    question_title = question_element.ele('xpath='+ question_titles_xpath, timeout=1)
                    question_answer = question_element.ele('xpath='+ question_answer_xpath, timeout=1)
        
                    q_obj= {
                        "perspective": title_element.text,
                        "question_title": question_title.text,
                        "question_answer": question_answer.text
                            }
                    qobj_list.append(q_obj)

                    print('getting one question and answer. time cost', time.time()-t2)
                    t2 = time.time()
                    

                    
        disease_obj['ques_of_int'] = qobj_list
        time_cost = time.time()-t1
        with open(os.path.join(current_path,'dep_dis_ques_with_q_a.jsonl'),'a') as f:
            json.dump(disease_obj, f,ensure_ascii=False)
            f.write('\n')
        with open(os.path.join(current_path,'log.txt'),'a') as f:
            log = f'{href},{disease_obj["disease"]},{time_cost}\n'
            f.write(log)
    except Exception as e:
        print(e)
        continue
    finally:    
        page.close()
        b = False
        time.sleep(1)

