import hmac
import base64


def getToken(productId, deviceId, deviceSecret):
    """获得设备加密后的token值"""
    message = str(deviceId) + '&' + str(productId)
    key = deviceSecret
    digest = hmac.new(key=key.encode(), msg=message.encode(), digestmod='sha1').digest()  # 获取hmac加密后的签名
    token = base64.b64encode(digest).decode()
    return token


if __name__ == '__main__':
    productId = 102501
    deviceId = 11162088
    deviceSecret = 'ZDMxMmEwMzYxNjA0YjRjMmQ0OGU='
    myToken = getToken(productId=productId, deviceId=deviceId, deviceSecret=deviceSecret)
    print(myToken)
