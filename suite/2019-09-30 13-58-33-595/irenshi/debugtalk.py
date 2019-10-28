# debugtalk.py
import re
import requests
# 获取请求头部中token
def getHeadersToken(req_headers):
    try:
        # TODO: write code...
        result = re.findall("XSRF-TOKEN=(.{36})", req_headers)[0]
        return result
    except Exception as e:
        print("获取请求头部中token失败，请检查问题。可能原因:{}".format(e))
        raise e


def getCookiesToken(req_cookies):
    result = requests.utils.dict_from_cookiejar(req_cookies)
    return result


def getStrLen(strs,len=9):
    if isinstance(strs,int):
        strs = str(strs)
    return strs[:len]
