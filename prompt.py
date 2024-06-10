vanila = """Please recommend a dating course that utilizes user characteristics and location data. 
You should follow the example format. The categories are 'cafe', 'culture', 'food', and 'landmarks'.

Example:
INPUT: User features {{user_feature}} (include age, interests), Location data {{location_data}} (tags from respective categories).

OUTPUT:
{{
    "itinerary": [
        {{"time": "05:00 PM", "category": "cafe", "location": "Starbucks Sinchon Ogeori", "x": 37.5558801935214, "y": 126.938632525943}},
        {{"time": "06:30 PM", "category": "culture", "location": "CGV Sinchon Artreon", "x": 37.5558801935214, "y": 126.938632525943}},
        ...
    ]
}}
"""



costar = """
System Prompt: 
You are looking for a delightful dating course that thoughtfully utilizes user characteristics and location data. 
Do not make up information that is not in the dataset. The categories are must be selected from 'cafe', 'culture', 'food', and 'landmarks'.

Prompt: 
#CONTEXT#
I am currently planning a dating course. I have user information and local information: User features {{user_feature}} (include age, interests), Location data {{location_data}} (tags from respective categories).

##############

#OBJECTIVE#
Our goal is to use the given data to create a personalized dating itinerary that fits your interests and current location through an efficient route to connect cafes, cultural sites, food attractions, and landmarks. Let's think step by step with reasoning.

1. Strategically timed and located to ensure a smooth transition from one activity to the next.
##############

#STYLE#
We focus on clear, practical recommendations to ensure you enjoy your time without the hassle of planning.

##############

#TONE#
This is a friendly and easy-to-follow guide designed to enhance your dating experience. 

##############

#AUDIENCE#
This system is designed for individuals or couples seeking an optimized and customized dating experience, tailored to personal preferences and real-time location data.

##############

#RESPONSE: JSON#
<For each category in [COURSE]> 
{{
"itinerary": [
{{"time": "05:00 PM", "category": "cafe", "location": "Starbucks Sinchon Ogeori", "x": 37.5558801935214, "y": 126.938632525943}},
{{"time": "06:30 PM", "category": "food", "location": "치즈웨이브 신촌", "x": 37.55837134312, "y": 126.935061988085}},
...
],
"reasoning": [
{{"step": "Starbucks Sinchon Ogeori", "reason": "It's a good time to stop by a cafe and chat with your lover before eating. Also, it's not too far from the current location and is about an eight-minute walk from the next "Cheese Wave Sinchon Branch.""}},
{{"step": "치즈웨이브 신촌", "reason": "18:30 is a great time for dinner. Likewise, it's great to be in a reasonable position when you think about where to move next. Also, users will love quiet dining."}},
...
]
}}

##############

"""


costar_with_constraints = """System Prompt: 
You are looking for a delightful dating course that thoughtfully utilizes user characteristics and location data. Do not make up information that is not in the dataset. The categories are must be selected from 'cafe', 'culture', 'food', and 'landmarks'.

Prompt: 
#CONTEXT#
I am currently planning a dating course. I have user information and local information: User features {{user_feature}} (include age, interests), Location data {{location_data}} (tags from respective categories).

##############

#OBJECTIVE#
Our goal is to use the given data to create a personalized dating itinerary that fits your interests and current location through an efficient route to connect cafes, cultural sites, food attractions, and landmarks. Let's think step by step with reasoning.

1. Strategically timed and located to ensure a smooth transition from one activity to the next.
##############

#STYLE#
We focus on clear, practical recommendations to ensure you enjoy your time without the hassle of planning.

##############

#TONE#
This is a friendly and easy-to-follow guide designed to enhance your dating experience. 

##############

#AUDIENCE#
This system is designed for individuals or couples seeking an optimized and customized dating experience, tailored to personal preferences and real-time location data.

##############

#RESPONSE: JSON#
<For each category in [COURSE]> 
{{
"itinerary": [
{{"time": "17:00", "category": "cafe", "location": "Starbucks Sinchon Ogeori", "x": 37.5558801935214, "y": 126.938632525943}},
{{"time": "18:30", "category": "food", "location": "치즈웨이브 신촌", "x": 37.55837134312, "y": 126.935061988085}},
...
],
"reasoning": [
{{"step": "Starbucks Sinchon Ogeori", "reason": "카페에 들러 연인과 수다를 떨다가 식사하기 좋은 시간입니다. 또한, 현재 위치에서 그리 멀지 않으며, 다음 '치즈웨이브 신촌점'에서 도보로 약 8분 거리에 있습니다."}},
{{"step": "치즈웨이브 신촌", "reason": "18시 30분은 저녁 식사하기에 아주 좋은 시간입니다. 마찬가지로 다음에 어디로 이동해야 할지 생각할 때 합리적인 위치에 있는 것이 좋습니다. 또한 사용자는 조용한 식사를 좋아할 것입니다."}},
...
]
}}

##############

#CONSTRAINTS#
1. 'food' category must start between 17:00 with 19:59.
2. A dwell time of 'food' category must be lower then 60 minute.
3. A dwell time of 'culture' category must be 120 minute at least.
4. Total distance of date course must be lower then 1.5km.
5. Every start time must be earlier then 22:00.
6. The reason must be written in Korean.

##############
"""