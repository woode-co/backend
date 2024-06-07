from typing import List
from fastapi import FastAPI, Depends, HTTPException
from pydantic import BaseModel
from sqlalchemy.orm import Session
from database import engine, get_db, User as DBUser, UserCreate as UserSchema
from recsys import recsys
from route_duration import extract_locations_and_durations
app = FastAPI()

sex_type = ['male', 'female']

tastes = [
    ['Calm', 'Noisy'],
    ['Cost-effective', 'Luxury'],
    ['Indoor', 'Outdoor'],
    ['Practical', 'Creative'],
    ['Minimalist', 'Maximalist'],
    ['Traditional', 'Modern'],
    ['Reserved', 'Outgoing']
]

class Course(BaseModel):
    user_id: str
    date: str
    start_t: str
    end_t: str
    curr_x: float
    curr_y: float

class UserInfo(BaseModel):
    user_id: int
    user_sex: bool
    user_birth: str
    user_favor: List[bool]

@app.get("/")
def read_root():
    return {"Hello": "World"}

@app.post("/signup/", response_model=bool)
def create_user(user: UserSchema, db: Session = Depends(get_db)):
    # Convert list of tastes to a comma-separated string
    # tastes_str = ' '.join(user.tastes)
    db_user = db.query(DBUser).filter(DBUser.user_id == user.user_id).first()
    if db_user:
        print("이미 존재하는 user")
        return False

    user_sex = 'male'
    if user.sex == False:
        user_sex = 'female'
    user_tastes = ''
    for i, taste in enumerate(user.tastes):
        if taste == False:
            user_tastes += tastes[i][1]
        else:
            user_tastes += tastes[i][0]
        if i != len(tastes) - 1:
            user_tastes += ' '
    print(user_tastes)
    db_user = DBUser(user_id=user.user_id, birth=user.birth, sex=user_sex, tastes=user_tastes)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return True

def save_user_info(user):
    # db에 저장하는 부분
    return True

def get_user_info(user_id: str, db):
    # 데이터베이스에서 user_id가 일치하는 첫 번째 사용자 정보를 조회
    db_user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    
    # 사용자가 존재하지 않으면 default 값을 반환
    if db_user is None:
        return {"User Number" : "32424","Birth Date": "1991.10.24","Sex" : "Male","Tastes": "Calm Luxury Indoor Practical Minimalist Modern Reserved"}
    
    # 사용자의 정보를 JSON 형식으로 반환
    return {
        "User Number": db_user.user_id,
        "Birth Date": db_user.birth,
        "Sex": db_user.sex,
        "Tastes": db_user.tastes
    }

@app.get("/signin/{user_id}")
def sign_in(user_id: str, db: Session = Depends(get_db)):
    db_user = db.query(DBUser).filter(DBUser.user_id == user_id).first()
    if db_user:
        return {"exists": True}
    else:
        return {"exists": False}

# 데이트 코스 추천
@app.post("/recsys")
def recommend_date_course(course: Course, db: Session = Depends(get_db)):
    user_info = get_user_info(course.user_id, db)
    print(user_info, course.date, course.start_t, course.end_t, course.curr_x, course.curr_y)
    date_course = recsys(user_info = user_info, date = course.date, start_t=course.start_t, end_t=course.end_t, curr_x=course.curr_x, curr_y=course.curr_y)
    print(date_course)
    durations = extract_locations_and_durations(date_course)
    print(durations)
    date_course['durations'] = durations
    return date_course

# To run the server, use the command:
# uvicorn backend:app --host 0.0.0.0 --port 8000 --reload
