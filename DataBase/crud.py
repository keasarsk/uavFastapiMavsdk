from sqlalchemy.orm import Session
from DataBase.database import flylogtest, drone_flylog
from mavsdk import System


def get_test(session: Session):
    print("dataintodb get_test yes")
    print(session.query(flylogtest).first())
    fl = flylogtest(order_id = 7)
    session.add(fl)
    session.commit()
    print("get_test yes")
    print(session.query(flylogtest).first())

def get_drone_flylog(session: Session):
    print("get_drone_flylog yes")
    print(session.query(drone_flylog).first())

