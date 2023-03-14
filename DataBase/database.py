
# 在database.py中，完成与MySQL的连接
# 在数据库相关的配置文件中，首先创建一个SQLAlchemy的"engine"，然后创建SessionLocal实例进行会话，最后创建模型类的基类。

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.automap import automap_base

SQLALCHEMY_DATABASE_URL = "mysql+pymysql://root:123456@210.30.97.238:3378/uav_cloud?charset=utf8"
# SQLALCHEMY_DATABASE_URL = f'mysql+mysqlconnector://{USER}:{PWD}@localhost:3306/{DB_NAME}?charset=utf8&auth_plugin=mysql_native_password'


# echo=True表示引擎将用repr()函数记录所有语句及其参数列表到日志
# engine = create_engine(
#     SQLALCHEMY_DATABASE_URL, encoding='utf8', echo=True
# )
engine = create_engine(SQLALCHEMY_DATABASE_URL,pool_pre_ping=True)

# SQLAlchemy中，CRUD是通过会话进行管理的，所以需要先创建会话，
# 每一个SessionLocal实例就是一个数据库session
# flush指发送到数据库语句到数据库，但数据库不一定执行写入磁盘
# commit是指提交事务，将变更保存到数据库文件中
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

# 创建基本映射类
Base = automap_base()
Base.prepare(engine, reflect=True)

# 反射得到orm
flylogtest = Base.classes.flylogtest
drone_flylog = Base.classes.drone_flylog
