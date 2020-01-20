# debugtalk.py
# 审批时获取任务taskId
def getTaskId_1(aname_1,tid_1,aname_2,tid_2,sname):
    mydict={}
    mydict[aname_1]=tid_1
    mydict[aname_2]=tid_2
    for key in mydict.keys():
        if key == sname:
            return mydict[key]


def getTaskId_2(aname_1,tid_1,aname_2,tid_2,sname):
    if str(aname_1) == str(sname):
        return tid_1
    else:
        return tid_2

def getTaskId(aname,sname,tid_1,tid_2):
    if aname==sname:
        return tid_1
    else:
        return tid_2
