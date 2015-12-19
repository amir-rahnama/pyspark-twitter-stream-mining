import tornado.websocket
import logging


class WebSocketHandler(tornado.websocket.WebSocketHandler):
    waiters = set()
    
    def check_origin(self, origin):
        return True

    def open(self): 
        WebSocketHandler.waiters.add(self)

    def on_message(self, message):
        WebSocketHandler.send_updates(message)
        
    def on_close(self):
        WebSocketHandler.waiters.remove(self)

    @classmethod
    def send_updates(cls, data):
        for waiter in cls.waiters:
            try:
                waiter.write_message(data)
            except:
                logging.error("Error sending message", exc_info=True)

 
class Application(tornado.web.Application):
    def __init__(self):
        handlers = [
            (r"/", WebSocketHandler)
        ]
        tornado.web.Application.__init__(self, handlers)

if __name__ == "__main__":
    app = Application()
    app.listen(8888)
    tornado.ioloop.IOLoop.current().start()
