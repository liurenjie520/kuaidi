# 1. 导入包
from flask import Flask, request
import test_2
# 2. 实例化一个
app = Flask(__name__)
# 3. 编写一个接口处理方法
@app.route("/add/", methods=["GET", "post"]) # 4. 挂载路由(指定接口的url路径), 声明接口接受的方法
def add():
    # 3.1 从请求中获取参数
    # request.values  {"a": "1", "b": "2"}
    a = request.values.get("a")
    # b = request.values.get("b")
    # 3.2 业务操作
    # sum = int(a) + int(b)
    result = test_2.KuaiDi1002().auto_number(a)
    result = test_2.KuaiDi100().track(result, a, '', '', '')

    # 3.3 组装响应并返回
    return str(result)

# 5. 运行接口
if __name__ == '__main__':
    app.run() # 默认5000端口,可以指定端口app.run(port=50001)
