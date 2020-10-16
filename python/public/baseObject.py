# -*- coding: utf-8 -*-
#基类

class BaseObject:
    def getDescription(self):
        #利用str的format格式化字符串
        #利用生成器推导式去获取key和self中key对应的值的集合
        return ",".join("{}={}".format(key,getattr(self,key)) for key in self.__dict__.keys())
    #重写__str__定义对象的打印内容
    def __str__(self):
        return "{}->({})".format(self.__class__.__name__,self.getDescription())