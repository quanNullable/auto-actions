import os,traceback,time
from logger import Logger

def test():
    # try:
    #     a = 2/0
    # except Exception as e:
    #     log(e)
    # print('os.environ')
    Logger.v('测试成功!')

def log(e):
    print(isinstance(e, Exception))
    print(time.strftime('%Y-%m-%d %H:%M:%S',time.localtime(time.time())),traceback.format_exc())


if __name__ == '__main__':
    test()


