# 내장 라이브러리
import os
import random
from pprint import pprint
import json

# 외부 설치 필요
import pandas as pd
from openai import OpenAI
from dotenv import load_dotenv

# 커스텀 라이브러리
import utils
from prompt import costar_with_constraints
from model import DataLoader, LLM


load_dotenv()
openai_api_key = os.getenv('OPENAI_API_KEY')


def select_random_user(user_data):
    random_user = random.choice(user_data.index)
    user_features = user_data.iloc[random_user].to_dict()
    return user_features


def recsys(user_info = None, date='2024-06-06', start_t='17:00', end_t='22:00', curr_x=37.555198169366435, curr_y=126.93698075993808):
    # User data
    user_data = pd.read_csv('./data/user_data.csv')
    if user_info == None:
        user_features = select_random_user(user_data)
    else:
        user_features = user_info
    user_features['date for the Date'] = date
    user_features['Date Start Time'] = start_t
    user_features['Date End Time'] = end_t
    user_features['x'] = curr_x
    user_features['y'] = curr_y

    # Place data
    food_data = pd.read_csv('./data/food.csv')
    cafe_data = pd.read_csv('./data/cafe.csv')
    culture_data = pd.read_csv('./data/culture.csv')
    landmark_data = pd.read_csv('./data/landmark.csv')

    food_loader = DataLoader(user_features, food_data)
    cafe_loader = DataLoader(user_features, cafe_data)
    culture_loader = DataLoader(user_features, culture_data)
    landmark_loader = DataLoader(user_features, landmark_data)

    # LLM model
    distance = 0.8  # (km)
    max_items = 20
    history = []
    recommender = LLM(model="gpt-4o", prompt=costar_with_constraints, openai_api_key=openai_api_key)

    place_features = {
        'food': food_loader(distance, max_items),   
        'cafe': cafe_loader(distance, max_items),   
        'culture': culture_loader(distance, max_items),   
        'landmark': landmark_loader(distance, max_items)
    }
    content, n_tokens = recommender(user_features, place_features)
    start_index = content.find('{')
    end_index = content.rfind('}') + 1
    history.append((content, n_tokens))

    if start_index != -1 and end_index != -1:
        json_str = content[start_index:end_index]
        content = json.loads(json_str)
    else:
        return None
    print(f'# {n_tokens} tokens used.\n')

    # Save history as cache file.
    file_path = utils.create_file(prefix='./cache/', extension='cache')
    utils.save_pickle(history, file_path)
    print(f'[Done] saved as {file_path}\n')
    return content


if __name__=='__main__':
    main()
    