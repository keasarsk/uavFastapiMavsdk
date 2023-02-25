from pydantic import BaseModel
# # 定义数据模型
# 定义flylog 表数据模型
class CreatFlyLog(BaseModel):
    drone_number: str
    in_air: int
    lat: float
    lng: float
    battery: float
    flight_mode: str
    is_armed: int

class CreatMissionPlan(BaseModel):
    task_number: str
    task_priority: str
    lat: float
    lng: float
    is_execute: int