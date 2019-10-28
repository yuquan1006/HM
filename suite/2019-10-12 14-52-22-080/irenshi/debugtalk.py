# debugtalk.py
import re,os
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

# 获取项目datas下文件路径
def getProjectFile(path):
    '''path -> list'''
    path = eval(path)
    projectPath = "/home/york/HttpRunnerManager/datas"
    for i in range(len(path)):
        projectPath = os.path.join(projectPath,path[i])
    return projectPath

# 数据转化
def get_evelData(data):
    try:
        data = str(data)
        result = eval(data)
    except:
        result = data
    return result
