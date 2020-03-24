import threading


def sender():
    print(threading.current_thread())


class TimerManager:
    main_timer = threading.Timer(1.0, sender)

    @classmethod
    def start(cls):
        threading.Thread(target=sender).start()
        cls.main_timer = threading.Timer(1.0, cls.start)
        cls.main_timer.start()

    @classmethod
    def stop(cls):
        cls.main_timer.cancel()




