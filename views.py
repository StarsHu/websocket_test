import logging
import tornado.web
import tornado.websocket
import tornado.escape
from models import MessageManager, Session

session = Session()


class MainHandler(tornado.web.RequestHandler):
    def get(self):
        self.render("index.html", messages=MessageManager().list())


class ChatSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    # cache = MessageManager().list()   已废弃，更新方式转为从数据库拉取

    def get_compression_options(self):
        # Non-None enables compression with default options.
        return {}

    def open(self):
        """
        当ws链接上时，将此链接加入收听者列表
        """
        ChatSocketHandler.waiters.add(self)

    def on_close(self):
        """
        断开ws连接时，将此连接移除收听者列表
        :return:
        """
        ChatSocketHandler.waiters.remove(self)

    # @classmethod 已废弃，更新方式转为重新从数据库拉取
    # def update_cache(cls, chat):
    #     cls.cache.append(chat)

    @classmethod
    def send_updates(cls, chat):
        """
        向所有收听者广播新内容
        """
        logging.info("sending message to %d waiters", len(cls.waiters))
        for waiter in cls.waiters:
            try:
                waiter.write_message(chat)
            except:
                logging.error("Error sending message", exc_info=True)

    def on_message(self, message):
        """
        当有新消息到达时启动
        """
        logging.info("got message %r", message)
        parsed = tornado.escape.json_decode(message)
        chat = MessageManager().add(parsed)  # 将新消息存到数据库，并获得一个有关于新消息的字典

        chat["html"] = tornado.escape.to_basestring(
            self.render_string("message.html", message=chat))

        # ChatSocketHandler.update_cache(chat)
        ChatSocketHandler.send_updates(chat)
