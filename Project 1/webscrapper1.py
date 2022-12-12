"""
Author : Kush Jayank Pandya
Date   : 25 September 2022
Summary: A web scrapper project.
"""

import requests
from bs4 import BeautifulSoup
import pandas as pd
import time
import json

def main():
    
    save_bins_size = 100
    base_website = 'https://www.politifact.com'
    
    http_text = requests.get(base_website + '/personalities/')
    
    soup = BeautifulSoup(http_text.text,features="html.parser")
    
    politicians_ref = soup.find_all(class_="m-list__item")
    politicians_ref = politicians_ref[1802:]
    politicians = []

    count = 1800

    df = pd.read_csv('output.csv')
    
    for political_entity in politicians_ref[:]:
          
        count+=1
        time.sleep(3)

        political_entity_info =  political_entity.text.split('\n\n\n')[1:3]
        political_entity_dict = {'Name' : political_entity_info[0], 'Political party' : political_entity_info[1]}
        political_entity_dict['href'] = base_website + political_entity.find_all('a')[0]['href']

        print(count,' - ',political_entity_dict['Name'])
        
        http_text_inner = requests.get(political_entity_dict['href'])
        soup_inner = BeautifulSoup(http_text_inner.text,features="html.parser")
        score_cards = soup_inner.find_all(class_="m-scorecard__item")
        
        assert len(score_cards) == 6
        
        for card in score_cards:
            
            score_title = card.find_all(class_ = "m-scorecard__title")
            score_value = card.find_all(class_ = "m-scorecard__checks")
            
            score_title = score_title[0].text.strip()
            score_value = score_value[0].text.strip()[0]

            assert score_title in ['True', 'Mostly True', 'Half True', 'Mostly False', 'False', 'Pants on Fire']
            assert score_value.isdigit()

            political_entity_dict[score_title] = score_value

        politicians.append(political_entity_dict)

        if count%save_bins_size == 0:
            df = pd.read_csv('output.csv')
            politicians = json.dumps(politicians)
            temp_df = pd.read_json(politicians)
            df = pd.concat([df,temp_df])
            df.to_csv('output.csv',index=False)
            politicians =[]
            print("---- saved progress -----")
    

    if len(politicians) != 0:
        df = pd.read_csv('output.csv')
        politicians = json.dumps(politicians)
        temp_df = pd.read_json(politicians)
        df = pd.concat([df,temp_df])
        df.to_csv('output.csv',index=False)
        print("---- saved progress -----")


if __name__ == '__main__':
    main()
