# # 使用ORM在models.py中对数据库表的model进行设计。以user表为例：
# # 通过数据库配置文件中的基类来创建模型类。
# # from sqlalchemy import Boolean, Column, Integer, String,VARCHAR, DECIMAL, Double
# from DataBase.database import Base
# from sqlalchemy import Table
# from DataBase.database import md

# # 创建一个实例类继承基类
# class Flylogtest(Base):
#     #第一个参数是数据表名，第二个参数是元数据，第三个参数表示自动加载
#     __table__ = Table("flylogtest",md,autoload=True) # 加载数据




# # class Flylogtest(Base):
# #     __tablename__ = "flylogtest"
# #     order_id = Column(String(18), primary_key=True, index=True)





# Base.metadata.create_all(bind = engine)