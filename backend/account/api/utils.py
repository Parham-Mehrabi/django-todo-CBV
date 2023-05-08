import threading
# import time

class EmailThread(threading.Thread):
    def __init__(self, email_object):
        threading.Thread.__init__(self)
        self.email_obj = email_object

    def run(self) -> None:
        # time.sleep(5)
        self.email_obj.send()
