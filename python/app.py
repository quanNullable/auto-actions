# -*- coding: utf-8 -*-
# 主入口

import web

urls = (
    '/wx', 'Handle',
)

if __name__ == '__main__':
    try:
        app = web.application(urls, globals())
        app.run()
    except Exception as e:
        print('控制器启动失败',e)
