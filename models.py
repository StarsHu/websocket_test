import datetime, uuid
from tornado import escape
from sqlalchemy import create_engine, Column
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.dialects.mysql import (INTEGER, DATETIME, VARCHAR, TEXT, BOOLEAN)
from sqlalchemy.orm import sessionmaker

MYSQL_DB = create_engine('mysql+pymysql://root:123456@localhost/erp_message?charset=utf8')
SQLALCHEMY_DATABASE_URI = 'mysql+pymysql://root:123456@localhost/erp_message?charset=utf8'


Session = sessionmaker(bind=MYSQL_DB)

Base = declarative_base()


class Message(Base):
    """
    留言
    """
    __tablename__ = "messages"
    id = Column(INTEGER, primary_key=True)  # 主键
    uuid = Column(VARCHAR(40), unique=True)  # uuid识别码
    created = Column(DATETIME, default=datetime.datetime.utcnow)  # 创建时间
    body = Column(TEXT)  # 留言内容
    receiver = Column(VARCHAR(20))  # 接受者
    flag = Column(BOOLEAN, default=False)  # 是否被标为已读/是否继续推送


class MessageManager(object):
    def __init__(self):
        self.session = Session()

    def add(self, body):
        """
        添加新消息，并返回包含uuid和内容的字典
        """
        body_dict = escape.json_decode(body.request.body)
        new_message = Message(uuid=str(uuid.uuid4()), body=body_dict["body"], receiver=body_dict["receiver"])
        self.session.add(new_message)
        self.session.commit()
        return {'id': new_message.uuid, 'body': new_message.body}

    def remove(self, handler):
        """
        将指定消息设为已读
        """
        message_uuid = handler.get_argument('uuid')
        remove_message = self.session.query(Message).filter_by(uuid=message_uuid).first()
        remove_message.flag = True
        self.session.commit()

    def list(self):
        """
        以字典形式返回目前所有未读消息
        """
        queryset = self.session.query(Message.uuid, Message.body).filter_by(flag=False).all()
        result = []
        for each_query in queryset:
            result.append({"id":each_query.uuid, "body":each_query.body})
        # print(result)
        return result


# class Sending(Base): 已废弃
#     """
#     分发和已读情况
#     """
#     __tablename__ = "sending"
#     id = Column(INTEGER, primary_key=True)  # 主键
#     message_id = Column(INTEGER, ForeignKey('messages.id'))  # 外键关联‘留言’的主键
#     receiver = Column(VARCHAR(20))  # 接受者
#     flag = Column(BOOLEAN, default=False)  # 是否被标为已读
