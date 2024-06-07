import utils
from random import sample
from typing import Tuple
from openai import OpenAI
from haversine import haversine


class DataLoader:
    def __init__(self, user_features, place_data):
        self.place_data = place_data
        self.user_position = (user_features['x'], user_features['y'])

    def __call__(self, distance, max_items):
        df = self.place_data
        where = df.apply(
            lambda row: haversine(self.user_position, (row['x'], row['y'])) < distance, 
            axis=1
        )
        df_dict = df[where].to_dict(orient='records')
        return sample(df_dict, min(max_items, len(df_dict)))


class LLM:
    def __init__(self, model: str, prompt: str, openai_api_key: str):
        self.model = model
        self.prompt = prompt
        self.client = OpenAI(api_key=openai_api_key)

    @utils.timer
    def __call__(self, user_features: dict, place_features: dict) -> Tuple[str, int]:
        data = f"INPUT: User features {user_features}, Place features {place_features}"
        response = self.client.chat.completions.create(
            model=self.model,
            messages=[
                {"role": "system", "content": self.prompt},
                {"role": "user", "content": data}
            ]
        )
        content = response.choices[0].message.content
        n_tokens = response.usage.total_tokens
        return (content, n_tokens)
    
