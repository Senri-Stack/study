import logging
import os
import datetime

class Main:
    def __init__(self):
        self.path_dir = os.path.realpath(os.path.join(os.getcwd(), os.path.dirname(__file__)))
        self.save_dir = os.path.join(self.path_dir, 'log')
        self.save_log_name = datetime.datetime.now().strftime('%Y-%m-%d') + '.log'
        self.save_log_path = os.path.join(self.save_dir, self.save_log_name)

    def make_save_dir(self):
        if not os.path.exists(self.save_dir):
            os.mkdir(self.save_dir)

    def logging_app(self):
        logger = logging.getLogger('simple_example')
        logger.setLevel(logging.DEBUG)
        ch = logging.StreamHandler()
        ch.setLevel(logging.DEBUG)
        formatter = logging.Formatter('%(asctime)s - %(name)s - %(levelname)s - %(message)s')
        ch.setFormatter(formatter)
        logger.addHandler(ch)


if __name__ == "__main__":
    main = Main()
    main.make_save_dir()
    main.logging_app()