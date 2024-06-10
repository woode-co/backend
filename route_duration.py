import requests
import time

################ API Keys ################
import os
from dotenv import load_dotenv

load_dotenv()
SK_OPEN_API_KEY = os.getenv("SK_OPEN_API_KEY")
##########################################

data = {
  "itinerary": [
    {
      "time": "09:00",
      "category": "cafe",
      "location": "파스쿠찌 충무로역점",
      "x": 37.562608,
      "y": 126.994097
    },
    {
      "time": "10:30",
      "category": "landmark",
      "location": "충무로애견거리",
      "x": 37.562027,
      "y": 126.996754
    },
    {
      "time": "12:00",
      "category": "food",
      "location": "파르투내",
      "x": 37.564611,
      "y": 127.005007
    },
    {
      "time": "13:00",
      "category": "culture",
      "location": "갤러리아람",
      "x": 37.562636,
      "y": 127.002275
    },
    {
      "time": "15:00",
      "category": "landmark",
      "location": "서울도보관광코스 1코스(청계천)",
      "x": 37.568727,
      "y": 126.995504
    }
  ],
  "reasoning": [
    {
      "step": "파스쿠찌 충무로역점",
      "reason": "Starting the day with a coffee at a local café is a great way to energize and relax. This cafe is conveniently located near the current position and sets a calm tone for the day."
    },
    {
      "step": "충무로애견거리",
      "reason": "A brisk walk through the lively Pet Street helps engage with the outdoor taste and provides a delightful, lively experience."
    },
    {
      "step": "파르투내",
      "reason": "The timing is perfect for lunch, and the restaurant offers a quiet dining experience that aligns with reserved and modern tastes."
    },
    {
      "step": "갤러리아람",
      "reason": "The two-hour cultural activity provides the opportunity to immerse in a creative, maximalist atmosphere at the gallery. It also ensures the itinerary remains within the cultural taste and interest."
    },
    {
      "step": "서울도보관광코스 1코스(청계천)",
      "reason": "Ending the day with a scenic walk along the Cheonggyecheon stream meets the taste for outdoor activities. This landmark is close by and offers a serene ambiance to conclude the date."
    }
  ]
}

def extract_locations_and_durations(data: dict):
    itinerary = data['itinerary']
    locations = [[item['y'], item['x'], item['location']] for item in itinerary]
    return get_walk_route_duration(locations)

def get_walk_route_duration(locs: list):
    """
    Tmap api를 사용해 주어진 위치 목록(locs)을 바탕으로 각 위치 간의 도보 소요 시간 계산

    Parameters:
    locs (list): 위치 데이터를 포함하는 2차원 list, 각 원소는 [x좌표, y좌표, 장소명] 형식

    Returns:
    list: 각 위치 쌍 간의 도보 소요 시간(초)을 담은 list. api 응답을 받지 못한 경우 -1 반환
    """

    # Tmap API URL, header
    url = 'https://apis.openapi.sk.com/tmap/routes/pedestrian?version=1'
    headers = {
        'Accept': 'application/json',
        'Content-Type': 'application/json',
        'appKey': SK_OPEN_API_KEY
    }

    # 인접한 위치 쌍에 대한 도보 경로 저장할 리스트 초기화
    durations = [-1 for i in range(len(locs) - 1 )]
    coordinates_list = []
    # 인접한 위치 쌍에 대해 도보 경로 API 요청
    for i in range(len(locs) - 1 ):
        data = {
            "startX": locs[i][0],
            "startY": locs[i][1],
            "startName": locs[i][2],
            "endX": locs[i+1][0],
            "endY": locs[i+1][1],
            "endName": locs[i+1][2]
        }
        response = requests.post(url, headers=headers, json=data, timeout=10)
        response_data = response.json()
        if i == 0:
          print(response_data['features'])
        tmp_coordinates_list = []
        # 응답 데이터에서 도보 소요 시간 추출
        if 'features' in response_data:
            sp_feature = response_data['features'][0]
            if 'properties' in sp_feature and 'totalTime' in sp_feature['properties']:
                durations[i] = sp_feature['properties']['totalTime'] // 60
            for feature in response_data["features"]:
              geometry = feature["geometry"]
              if geometry["type"] == "LineString":
                  for coord in geometry["coordinates"]:
                      tmp_coordinates_list.append(coord)
        coordinates_list.extend(tmp_coordinates_list)


    unique_coordinates = []
    previous_coord = None
    for coord in coordinates_list:
        if coord != previous_coord:
            unique_coordinates.append(coord)
            previous_coord = coord

    return durations, unique_coordinates

if __name__ == '__main__':
    # 테스트 데이터
    l = [
            [126.930562418509,37.5445456700197,"채선당 광흥창점"],
            [126.932433807492,37.5447954313915,"마미"],
            [126.930634805464,37.544581752529,"바드다드 카페"],
            [126.93408804803389,37.544929714208216,"김밥천국 신수사거리점"]
    ]
    start_time = time.time()
    # print(f"도보 소요 시간(초): {get_walk_route_duration(l)}")
    durations, coordinates_list = extract_locations_and_durations(data)
    print(f"도보 소요 시간(초): {durations}")
    print(f"도보 경로 : {coordinates_list}")
    print(f"도보 points 개수 : {len(coordinates_list)}")
    end_time = time.time()
    elapsed_time = end_time - start_time
    # 4개의 location 기준 1.9초정도 걸림
    print(f"Request 처리 시간: {elapsed_time:.2f}초")