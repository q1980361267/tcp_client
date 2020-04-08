import socket
import struct
import time
import json
import xlrd
import select
from lib import getToken
from lib import get_excel
from lib import get_color
from lib.get_color import color

# 读取excel表中数据
my_cols = get_excel.getExcel(file='./测试表格.xls', sheet=0, column=1)
ip = my_cols[1]
port = my_cols[2]
productId = my_cols[3]
deviceSecret = my_cols[4]
deviceId = my_cols[5]
# token = getToken.getToken(productId=productId, deviceId=deviceId, deviceSecret=deviceSecret)
token = 'Tk6dv+na9w5OTu5KkObzbHwRkz0='

# 设备连接
tcp_socket = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
tcp_socket.setsockopt(socket.SOL_SOCKET, socket.SO_REUSEADDR, True)
ip_port = (ip, int(port))
tcp_socket.connect(ip_port)
auth = '*{}#{}#{}*'.format(int(productId), int(deviceId), token)
tcp_socket.sendall(auth.encode())
print(color.cyan('设备鉴权信息： ' + auth))
print(color.cyan('接入机地址： ' + str(ip_port)))
# if tcp_socket.recv(1024):
#     print('收到上线回应')
# else:
#     print('上线失败')

# 上报的数据
someString = '{"someString":"ironman"}'
someInteger = '{"someInteger":12}'


#  上行数据
def upload():
    while True:
        # tcp_socket.sendall(struct.pack('!H', len(someString))+someString.encode())
        tcp_socket.sendall(struct.pack('!H', len(someInteger)) + someInteger.encode())
        a = struct.pack('!H', len(someString)) + someString.encode()
        print('上行数据完成')
        print(a)
        time.sleep(10)


# 下行数据（异步IO）
if __name__ == '__main__':
    # upload()
    inputs = [tcp_socket]
    while True:
        rs, ws, es = select.select(inputs, [], [])
        for r in rs:
            if r is tcp_socket:
                recv = tcp_socket.recv(10240)
                try:
                    recv_dic = json.loads(recv)
                except:
                    continue
                print(recv_dic)
                _uuid = recv_dic['uuid']
                _functionType = recv_dic['functionType']
                _identifier = recv_dic['identifier']
                if _functionType == 'propertySet':
                    _data = _uuid + 'success'
                    _len = len(_data)
                    _send = '#'.encode() + struct.pack('!B', _len) + _data.encode()
                    tcp_socket.sendall(_send)
                    print('response: ' + str(_send))
                elif _functionType == 'propertyGet':
                    if _identifier == 'someString':
                        _data = _uuid + 'spiderman'
                        _len = len(_data)
                        _send = '#'.encode() + struct.pack('!B', _len) + _data.encode()
                        tcp_socket.sendall(_send)
                        print('response: ' + str(_send))
                    elif _identifier == 'someInteger':
                        _data = _uuid + '1234'
                        _len = len(_data)
                        _send = '#'.encode() + struct.pack('!B', _len) + _data.encode()
                        tcp_socket.sendall(_send)
                        print('response: ' + str(_send))
                    elif _identifier == 'someFloat':
                        _data = _uuid + '123.123'
                        _len = len(_data)
                        _send = '#'.encode() + struct.pack('!B', _len) + _data.encode()
                        tcp_socket.sendall(_send)
                        print('response: ' + str(_send))
                    elif _identifier == 'someDouble':
                        _data = _uuid + '321.321'
                        _len = len(_data)
                        _send = '#'.encode() + struct.pack('!B', _len) + _data.encode()
                        tcp_socket.sendall(_send)
                        print('response: ' + str(_send))
                    elif _identifier == 'someLong':
                        _data = _uuid + '255000'
                        _len = len(_data)
                        _send = '#'.encode() + struct.pack('!B', _len) + _data.encode()
                        tcp_socket.sendall(_send)
                        print('response: ' + str(_send))
                    elif _identifier == 'someBoolean':
                        _data = _uuid + 'True'
                        _len = len(_data)
                        _send = '#'.encode() + struct.pack('!B', _len) + _data.encode()
                        tcp_socket.sendall(_send)
                        print('response: ' + str(_send))
                    elif _identifier == 'someDate':
                        _data = _uuid + str(int(time.time()) * 1000)
                        _len = len(_data)
                        _send = '#'.encode() + struct.pack('!B', _len) + _data.encode()
                        tcp_socket.sendall(_send)
                        print('response: ' + str(_send))
