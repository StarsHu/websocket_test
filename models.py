import datetime, uuid
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import (INTEGER, DATETIME, VARCHAR, TEXT, BOOLEAN)

MYSQL_DB = create_engine('mysql+pymysql://root:123456@localhost/erp_message?charset=utf8')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/erp_message?charset=utf8'

Base = declarative_base()


class Message(Base):
    """
    留言
    """
    __tablename__ = "messages"
    id = Column(INTEGER, primary_key=True)  # 主键
    uuid = Column(VARCHAR(32), default=str(uuid.uuid4()), unique=True)  # uuid识别码
    created = Column(DATETIME, default=datetime.datetime.utcnow)  # 创建时间
    body = Column(TEXT)  # 留言内容
    receiver = Column(VARCHAR(20))  # 接受者
    flag = Column(BOOLEAN, default=False)  # 是否被标为已读/是否继续推送

#
# class Sending(Base):
#     """
#     分发和已读情况
#     """
#     __tablename__ = "sending"
#     id = Column(INTEGER, primary_key=True)  # 主键
#     message_id = Column(INTEGER, ForeignKey('messages.id'))  # 外键关联‘留言’的主键
#     receiver = Column(VARCHAR(20))  # 接受者
#     flag = Column(BOOLEAN, default=False)  # 是否被标为已读
