from app import app
from flask import request
from flask import session
import json
from app.models import LoginUser,Menus,Need,Bugs,Iteration,Report,Files
import hashlib
from app import db
from sqlalchemy import or_,desc
import datetime
from app.email import send_email
import time



@app.route('/')
def index():
    return '欢迎来到首页'

@app.route('/login',methods=['POST','GET'])
def login():

    if request.method == 'GET':
        user = session.get('username')
        if user is None:
            data = {
                'code':-1,
                'msg':'登录失效，请重新登录!',
                'data':[]
            }
            return toString(data)
    else:
        uname = request.form.get('username')
        upass = request.form.get('password')

        h1 = hashlib.md5()
        b = upass.encode(encoding="utf-8")
        h1.update(b)
        upass_hash = h1.hexdigest()
        user = LoginUser.query.filter_by(username=uname).first()
        #判断输入的用户名、加密后的密码是否等于数据库中的用户名、加密后的密码
        if uname==user.username and upass_hash == user.password_hash:
            #登录成功，将数据保存到session
            session['uname'] = uname
            first = getMenus(None)
            data = {
                "code": 200,
                "msg":"成功",
                "data":
                    {
                        "loginName": uname,
                        "firstMenus":None,
                        "menus":toString(first)
                    }
            }
            return toString(data)
        else:
            #登录失败
            return 'error'

def toString(data):
    return json.dumps(data)

@app.route('/getUserInfo',methods=['GET'])
def getUserInfo():
    """
    获取所有登录用户的用户名
    """
    users = LoginUser.query.all()

    user=[]
    for u in users:
        dict = {}
        dict["loginName"] = u.username
        dict['sex']=u.sex
        dict['email']=u.email
        dict['position']=u.Position
        user.append(dict)
    data={
        "code":200,
        "user":user
    }
    return data

def getMenus(parentId):
    """
    菜单
    """
    menus = []
    first = Menus.query.filter(Menus.parentId==parentId).order_by(Menus.rank).all()
    for i in first:
        dict = {}
        dict["menuid"]=str(i.id)
        dict["menuname"] = i.name
        dict["icon"] = i.icon
        dict["url"] = i.action
        dict["parentMenuId"] = i.parentId
        dict.update({"menus": getMenus(i.id)})
        menus.append(dict)
    return menus

@app.route('/need/list',methods=['GET','POST'])
def list():
    """
   需求列表
    """
    page = int(request.args.get('page',default=1))
    page_size = int(request.args.get('size',default=20))

    type = request.args.get('type')

    title = request.args.get('title')
    handler = request.args.get('handler')
    
    query = Need.query
    if type:
        query = query.filter(Need.type==type)

    if title:
        query = query.filter(Need.title.contains(title))

    if handler:
        query = query.filter(Need.handler.contains(handler))

    else:
        query = query

    total = query.count()#需求总条数
    reqult_need = query.order_by(Need.start_time.desc()).paginate(page,page_size,error_out=False)#需求分页


    needList = []
    noIterNeedList = []

    for i in reqult_need.items:
        dict = {}
        dict["id"] = str(i.id)
        dict["title"] = i.title
        dict["priority"] = i.priority
        dict["iteration"] = i.iteration
        dict["status"] = i.status
        dict["handler"] = i.handler
        dict["start_time"] = i.start_time
        dict["end_time"] = i.end_time
        dict["type"] = i.type
        needList.append(dict)

    query = query.filter(Need.iteration == "")
    reqult = query.order_by(Need.start_time).paginate(page, page_size, error_out=False)
    for i in reqult.items:
        dict = {}
        dict["id"] = str(i.id)
        dict["title"] = i.title
        dict["priority"] = i.priority
        dict["iteration"] = i.iteration
        dict["status"] = i.status
        dict["handler"] = i.handler
        dict["start_time"] = i.start_time
        dict["end_time"] = i.end_time
        dict["type"] = i.type
        noIterNeedList.append(dict)

    data = {
        "total": total,
        "needList": needList,
        "noIterTotal":reqult.total,
        "noIterNeedList":noIterNeedList
    }
    return data

@app.route('/need/add',methods=["GET","POST"])
def add():
    """
    新增需求
    """
    title = request.form.get('title')
    priority = request.form.get('priority')
    iteration = request.form.get('iteration')
    status = "规划中"
    handler = request.form.get('handler')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    type = request.form.get('type')

    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    if start_time != '':
        utcTime1 = datetime.datetime.strptime(start_time, UTC_FORMAT)
        start_time = (utcTime1 + datetime.timedelta(hours=8)).date()
    if end_time != '':
        utcTime2 = datetime.datetime.strptime(end_time, UTC_FORMAT)
        end_time = (utcTime2 + datetime.timedelta(hours=8)).date()

    need = Need(title=title,priority=priority,iteration=iteration,status=status,
                handler=handler,start_time=start_time,end_time=end_time,type=type)
    db.session.add(need)
    db.session.commit()


    #将需求归到对应迭代里
    if iteration:
        ition = Iteration(title=title, priority=priority, status=status, handler=handler,
                          start_time=start_time, end_time=end_time, type=iteration)
        db.session.add(ition)
        db.session.commit()

    return 'success'



@app.route('/need/update',methods=["GET","POST"])
def update():
    """
    更新需求
    """
    ids = request.form.get('ids')
    title = request.form.get('title')
    priority = request.form.get('priority')
    iteration = request.form.get('iteration')
    status = request.form.get('status')
    handler = request.form.get('handler')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    type = request.form.get('type')

    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    if start_time:
        if start_time !='' and 'Z' in start_time:
            utcTime1 = datetime.datetime.strptime(start_time, UTC_FORMAT)
            start_time = (utcTime1 + datetime.timedelta(hours=8)).date()
    if end_time:
        if end_time !='' and 'Z' in end_time:
            utcTime2 = datetime.datetime.strptime(end_time, UTC_FORMAT)
            end_time = (utcTime2 + datetime.timedelta(hours=8)).date()

    #更新需求

    # 批量处理
    if ',' in ids:
        need_id = ids.split(',')
        for id in need_id:
            need = Need.query.filter(Need.id == int(id)).first()
            iter = Iteration.query.filter(Iteration.title==need.title).first()
            if iter:
                if status:
                    need.status = status
                    iter.status=status
                if handler:
                    need.handler = handler
                    iter.handler = handler
            db.session.commit()

        # 编辑单条记录或仅编辑状态
    else:
        need = Need.query.filter(Need.id == ids).first()
        #更新迭代
        if need.iteration:  # 之前填了迭代
            if title:
                iter = Iteration.query.filter(Iteration.title == need.title).first()
                # 迭代没变，更新迭代下的需求
                iter.title = title
                iter.priority = priority
                iter.status = status
                iter.handler = handler
                iter.start_time = str(start_time)
                iter.end_time = str(end_time)
                iter.type = iteration
                db.session.commit()

                need.title = title
                need.priority = priority
                need.iteration = iteration
                need.status = status
                need.handler = handler
                need.start_time = start_time
                need.end_time = end_time
                need.type = type
                db.session.commit()
            else:
                #只改状态
                iter = Iteration.query.filter(Iteration.status == need.status).first()
                iter.status = status
                db.session.commit()

                need.status = status
                db.session.commit()

        else:
            iter = Iteration.query.filter(Iteration.title==need.title).first()
            if iter:
                iter.type=iteration
                need.iteration=iteration
                db.session.commit()

            else:
                if title:
                    iter = Iteration(title=title, priority=priority, status=status, handler=handler,
                                     start_time=start_time, end_time=end_time, type=iteration)
                    db.session.add(iter)
                    db.session.commit()

                    need.title = title
                    need.priority = priority
                    need.iteration = iteration
                    need.status = status
                    need.handler = handler
                    need.start_time = start_time
                    need.end_time = end_time
                    need.type = type
                    db.session.commit()

                else:
                    need.status = status
                    db.session.commit()

    return 'success'

@app.route('/need/delete',methods=["GET","POST","DELETE"])
def delete():
    id = request.args.get('id')
    need = Need.query.filter(Need.id==id).first()
    db.session.delete(need)
    db.session.commit()

    iteration = Iteration.query.filter(Iteration.title==need.title).first()
    if iteration:
        db.session.delete(iteration)
        db.session.commit()
    return "success"

@app.route('/need/batchDelete',methods=["GET","POST","DELETE"])
def batchDelete():
    ids = request.args.get('ids')
    need_ids = ids.split(',')

    for need_id in need_ids:
        n = Need.query.get(int(need_id))
        db.session.delete(n)
        db.session.commit()

        iter = Iteration.query.filter(Iteration.title==n.title).first()
        if iter:
            db.session.delete(iter)
            db.session.commit()
    return "success"

@app.route('/bug/listBugs', methods=['GET', 'POST'])
def listBugs():
    """
   缺陷列表
    """
    page = int(request.args.get('page', default=1))
    page_size = int(request.args.get('size', default=20))
    type = request.args.get('type')


    keyword = request.args.get('keyword')
    severity = request.args.get('severity')
    status = request.args.get('status')
    createTime_start = request.args.get('startDate')
    createTime_end = request.args.get('endDate')



    query = Bugs.query
    if type:
        query = query.filter(Bugs.type == type)
    if keyword:
        query = query.filter(or_(Bugs.title.contains(keyword),Bugs.handler.contains(keyword),Bugs.creater.contains(keyword)))
    if severity:
        query = query.filter(Bugs.severity.contains(severity))
    if status:
        query = query.filter(Bugs.status.contains(status))


    if createTime_start:
        query = query.filter(Bugs.createTime>=createTime_start)
    if createTime_end:
        query = query.filter(Bugs.createTime<=createTime_end)

    total = query.count()
    reqult = query.order_by(desc('createTime')).paginate(page, page_size, error_out=False)

    bugList = []

    for i in reqult.items:
        dict = {}
        dict["id"] = str(i.id)
        dict["title"] = i.title
        dict["severity"] = str(i.severity)
        dict["priority"] = i.priority
        dict["iteration"] = i.iteration
        dict["status"] = i.status
        dict["handler"] = str(i.handler)
        dict["creater"] = i.creater
        dict["createTime"] = str(i.createTime)
        dict["type"] = i.type
        bugList.append(dict)
    data = {
        "total": total,
        "bugList": bugList,
    }
    return data


@app.route('/bug/addBugs', methods=["GET", "POST"])
def addBugs():
    """
    新增缺陷
    """
    title = request.form.get('title')
    severity = request.form.get('severity')
    priority = request.form.get('priority')
    iteration = request.form.get('iteration')
    handler = request.form.get('handler')
    creater = session.get('uname')
    createTime = datetime.datetime.now().date()
    type = request.form.get('type')
    status = "新"

    bug = Bugs(title=title, severity=severity,priority=priority, iteration=iteration, status=status,
                handler=handler, creater=creater,createTime=createTime, type=type)
    db.session.add(bug)
    db.session.commit()

    #将bug归到对应迭代中
    if iteration:
        iter = Iteration(title=title,priority=priority,status=status,handler=handler,start_time="",end_time="",type=iteration)
        db.session.add(iter)
        db.session.commit()

    return 'success'


@app.route('/bug/updateBugs', methods=["GET", "POST"])
def updateBugs():
    """
    更新缺陷
    """
    ids = request.form.get('ids')
    title = request.form.get('title')
    severity = request.form.get('severity')
    priority = request.form.get('priority')
    iteration = request.form.get('iteration')
    status = request.form.get('status')
    handler = request.form.get('handler')
    type = request.form.get('type')

    # 批量处理
    if ',' in ids:
        bug_id = ids.split(',')
        for id in bug_id:
            bug = Bugs.query.filter(Bugs.id == int(id)).first()
            iter = Iteration.query.filter(Iteration.title==bug.title).first()
            if iter:
                if status:
                    bug.status = status
                    iter.status = status
                if handler:
                    bug.handler = handler
                    iter.status = status

            db.session.commit()

    # 编辑单条记录或仅编辑状态
    else:
        bug = Bugs.query.filter(Bugs.id == ids).first()
        if bug.iteration:
            if title:
                iter = Iteration.query.filter(Iteration.title == bug.title).first()

                iter.title = title
                iter.severity = severity
                iter.priority = priority
                iter.iteration = iteration
                iter.status = status
                iter.handler = handler
                iter.type = iteration

                bug.title = title
                bug.severity = severity
                bug.priority = priority
                bug.iteration = iteration
                bug.status = status
                bug.handler = handler
                bug.type = type

                db.session.commit()
            else:
                iter = Iteration.query.filter(Iteration.title == bug.title).first()
                iter.status = status
                iter.handler = handler
                db.session.commit()

                bug.status = status
                bug.handler = handler
                db.session.commit()

        else:
            iter = Iteration.query.filter(Iteration.title == bug.title).first()
            if iter:
                iter.type = iteration
                bug.iteration = iteration
                db.session.commit()
            else:
                if title:
                    iter = Iteration(title=title, priority=priority, status=status, handler=handler,
                                     start_time="", end_time="", type=iteration)
                    db.session.add(iter)
                    db.session.commit()

                    bug.title=title
                    bug.severity=severity
                    bug.priority=priority
                    bug.iteration=iteration
                    bug.status = status
                    bug.handler=handler
                    bug.type=type
                    db.session.commit()
                else:
                    bug.status=status
                    db.session.commit()

    return 'success'


@app.route('/bug/deleteBugs', methods=["GET", "POST"])
def deleteBugs():
    id = request.args.get('id')
    bug = Bugs.query.filter(Bugs.id == id).first()
    db.session.delete(bug)
    iter = Iteration.query.filter(Iteration.title==bug.title).first()
    if iter:
        db.session.delete(iter)
    db.session.commit()
    return "success"


@app.route('/bug/batchDeleteBugs', methods=["GET", "POST"])
def batchDeleteBugs():
    ids = request.args.get('ids')
    bug_ids = ids.split(',')

    for bug_id in bug_ids:
        n = Bugs.query.get(int(bug_id))
        iter = Iteration.query.filter(Iteration.title==n.title).first()
        if iter:
            db.session.delete(iter)
        db.session.delete(n)
        db.session.commit()
    return "success"

@app.route('/bug/statistic',methods=["GET","POST"])
def statistic():
    createTime_start = request.args.get('startDate')
    createTime_end = request.args.get('endDate')

    query1 = db.session.query(Bugs.creater, db.func.count('*'))
    query2 = db.session.query(Bugs.handler, db.func.count('*'))
    query3 = db.session.query(Bugs.createTime, db.func.count('*'))
    query4 = db.session.query(Bugs.status, db.func.count('*'))

    if createTime_start:

        query1 = query1.filter(Bugs.createTime >= createTime_start)
        query2 = query2.filter(Bugs.createTime >= createTime_start)
        query3 = query3.filter(Bugs.createTime >= createTime_start)
        query4 = query4.filter(Bugs.createTime >= createTime_start)

    if createTime_end:

        query1 = query1.filter(Bugs.createTime <= createTime_end)
        query2 = query2.filter(Bugs.createTime <= createTime_end)
        query3 = query3.filter(Bugs.createTime <= createTime_end)
        query4 = query4.filter(Bugs.createTime <= createTime_end)

    a = query1.group_by(Bugs.creater).all()#bug创建人及对应创建的Bug数
    b = query2.group_by(Bugs.handler).all()#bug处理人及对应要处理的bug数

    #获取创建人列表及对应提的Bug数
    creater_name = []
    creater_bug = []
    createrList = []
    for i in a:
        creater_name.append(i[0])
        creater_bug.append(i[1])
        dict = {}
        dict["creater_name"] = str(i[0])
        dict["creater_bug"] = str(i[1])
        createrList.append(dict)


    #获取处理人列表和处理人对应的Bug数
    handler_name = []
    handler_bug = []
    handlerList = []

    for i in b:
        name = i[0]
        names = name.split(';')

        for sn in names:
            if sn in handler_name :
                #处理人已存在，找到该处理人的Bug数在bug表中的位置，将其新的bug数加上
                handler_bug[handler_name.index(sn)] = handler_bug[handler_name.index(sn)]+i[1]
            else:
                #处理人不存在，将名字加到名字表，Bug数加到bug表
                handler_name.append(sn)
                handler_bug.append(i[1])


    for i in range(0,len(handler_name)):
        dict = {}
        dict["handler_name"] = str(handler_name[i])
        dict["handler_bug"] = str(handler_bug[i])
        handlerList.append(dict)

    # 创建缺陷总数
    bugs_day = query3.group_by(Bugs.createTime).all()#日期及对应bug总数
    bugs_date = []
    bugs_count = []  # 有bug的日期的Bug总数

    for i in bugs_day:
        bugs_date.append(i[0].strftime("%Y-%m-%d"))
        bugs_count.append(i[1])



    # 获取当前时间所在的年月
    current_date = datetime.datetime.now()
    year = current_date.year
    month = current_date.month
    # 获取当前月份所有日期
    daysList = allDays(year, month)
    if createTime_start:
        daysList = daysList[daysList.index(createTime_start):]
    if createTime_end:
        daysList = daysList[:(daysList.index(createTime_end)+1)]


    # 当月全部日期的bug数，没Bug的数据是0
    everyday_Bug = []

    for day in daysList:
        if day not in bugs_date:
            everyday_Bug.append(0)
        else:
            everyday_Bug.append(bugs_count[bugs_date.index(day)])



    # 日期及对应的修复bug数
    resolved_bugs = query3.filter(or_(Bugs.status == "已解决", Bugs.status == "已验证", Bugs.status == "已关闭")).group_by(
        Bugs.createTime).all()
    resolved_date = []
    resolved_count = []
    for i in resolved_bugs:
        resolved_date.append(i[0].strftime("%Y-%m-%d"))
        resolved_count.append(i[1])

    hasBug_resolved=[]
    for day in bugs_date:
        if day not in resolved_date:
            hasBug_resolved.append(0)
        else:
            hasBug_resolved.append(resolved_count[resolved_date.index(day)])


    everyday_resolved=[]
    for day in daysList:
        if day not in resolved_date:
            everyday_resolved.append(0)
        else:
            everyday_resolved.append(resolved_count[resolved_date.index(day)])


    # 日期及对应的关闭bug数
    colsed_bugs = query3.filter(Bugs.status == "已关闭").group_by(Bugs.createTime).all()
    colsed_date = []
    colsed_count = []
    for i in colsed_bugs:
        colsed_date.append(i[0].strftime("%Y-%m-%d"))
        colsed_count.append(i[1])
    hasBug_closed=[]
    for day in bugs_date:
        if day not in colsed_date:
            hasBug_closed.append(0)
        else:
            hasBug_closed.append(colsed_count[colsed_date.index(day)])

    everyday_closed = []
    for day in daysList:
        if day not in colsed_date:
            everyday_closed.append(0)
        else:
            everyday_closed.append(colsed_count[colsed_date.index(day)])

    bugDayList=[]
    for i in range(len(daysList)):
        dict = {}
        dict["days"] = daysList[i]
        dict["everyday_bug"] = everyday_Bug[i]
        dict["everyday_resolved"] = everyday_resolved[i]
        dict["everyday_closed"] = everyday_closed[i]
        bugDayList.append(dict)


    # 状态及对应bug数
    status_bug = query4.group_by(Bugs.status).all()
    status = []
    status_count = []
    statusList =[]

    for i in status_bug:
        status.append(i[0])
        status_count.append(i[1])
        dict = {}
        dict["status"]= str(i[0])
        dict["status_count"] = str(i[1])
        statusList.append(dict)


    data = {
        "creater_name": creater_name,#创建bug的人名
        "creater_bug": creater_bug,#对应创建人的bug数
        "handler_name": handler_name,#处理Bug的人名
        "handler_bug": handler_bug,#对应处理人的bug数
        "bugs_date": bugs_date,#有bug的日期
        "bugs_count": bugs_count,#对应日期的bug数
        "resolved_date": resolved_date,#有已修复bug的日期
        "hasBug_resolved": hasBug_resolved,#有bug的日期对应修复bug数
        "colsed_date": colsed_date,#有已关闭bug的日期
        "hasBug_closed": hasBug_closed,#有bug的日期对应的关闭bug数
        "status": status,#bug的所有状态
        "status_count": status_count,  #每个状态的bug数
        "statusList": statusList,#状态列表数据
        "handlerList" : handlerList,#处理人列表数据
        "createrList": createrList, #创建人列表数据
        "daysList" : daysList,  #当月全部日期
        "everyday_Bug": everyday_Bug,
        "everyday_resolved":everyday_resolved,
        "everyday_closed":everyday_closed,
        "bugDayList" : bugDayList #当月每天Bug情况（包括日期、创建bug数、修复bug数、关闭bug数）

    }

    return data



from calendar import monthrange

def allDays(y, m):
    return ['{:04d}-{:02d}-{:02d}'.format(y, m, d) for d in range(1, monthrange(y, m)[1] + 1)]


@app.route('/iteration/listIters', methods=['GET', 'POST'])
def listIters():
    """
   迭代列表
    """
    page = int(request.args.get('page', default=1))
    page_size = int(request.args.get('size',default=20))
    type = request.args.get('type')

    keyword = request.args.get('keyword')
    priority = request.args.get('priority')
    status = request.args.get('status')


    query = Iteration.query
    if type:
        query = query.filter(Iteration.type == type)
    if priority:
        query = query.filter(Iteration.priority == priority)
    if status:
        query = query.filter(Iteration.status == status)
    if keyword:
        query = query.filter(or_(Iteration.title.contains(keyword), Iteration.handler.contains(keyword)))

    total = query.count()
    reqult = query.order_by(Iteration.start_time.desc()).paginate(page, page_size, error_out=False)

    iterationList = []

    for i in reqult.items:
        dict = {}
        dict["id"] = str(i.id)
        dict["title"] = i.title
        dict["priority"] = i.priority
        dict["status"] = i.status
        dict["handler"] = str(i.handler)
        dict["start_time"] = str(i.start_time)
        dict["end_time"] = str(i.end_time)
        dict["type"] = i.type
        iterationList.append(dict)
    data = {
         "total": total,
        "iterationList": iterationList,
    }
    return data


@app.route('/iteration/addIters', methods=["GET", "POST"])
def addIters():
    """
    新增迭代
    """
    ids = request.form.get('ids')
    type = request.form.get('type')

    if ',' in ids:
        need_id = ids.split(',')
        for id in need_id:
            need = Need.query.filter(Need.id == id).first()
            iteration = Iteration(title=need.title,priority=need.priority,status=need.status,handler=need.handler,
                                  start_time=need.start_time,end_time=need.end_time,type=type)
            db.session.add(iteration)
            db.session.commit()

            # 更改该需求的迭代
            need.iteration = type
            db.session.commit()
    else:
        need = Need.query.filter(Need.id == int(ids)).first()
        iteration = Iteration(title=need.title, priority=need.priority, status=need.status, handler=need.handler,
                              start_time=need.start_time, end_time=need.end_time, type=type)
        db.session.add(iteration)
        db.session.commit()

        #更改该需求的迭代
        need.iteration = type
        db.session.commit()

    return 'success'


@app.route('/iteration/updateIters', methods=["GET", "POST"])
def updateIters():
    """
    更新迭代
    """
    id = request.form.get('id')
    title = request.form.get('title')
    priority = request.form.get('priority')
    status = request.form.get('status')
    handler = request.form.get('handler')
    start_time = request.form.get('start_time')
    end_time = request.form.get('end_time')
    type = request.form.get('type')

    UTC_FORMAT = "%Y-%m-%dT%H:%M:%S.%fZ"
    if start_time != '' and 'Z' in start_time:
        utcTime1 = datetime.datetime.strptime(start_time, UTC_FORMAT)
        start_time = (utcTime1 + datetime.timedelta(hours=8)).date()
    if end_time != '' and 'Z' in end_time:
        utcTime2 = datetime.datetime.strptime(end_time, UTC_FORMAT)
        end_time = (utcTime2 + datetime.timedelta(hours=8)).date()

    iteration = Iteration.query.filter(Iteration.id == id).first()

    need = Need.query.filter(Need.title == iteration.title).first()
    bug = Bugs.query.filter(Bugs.title==iteration.title).first()
    if need:
        need.title = title
        need.priority = priority
        need.iteration = type
        need.status = status
        need.handler = handler
        need.start_time = start_time
        need.end_time = end_time
        db.session.commit()

    if bug:
        bug.title = title
        bug.priority = priority
        bug.iteration = type
        bug.status = status
        bug.handler = handler

        db.session.commit()

    iteration.title = title
    iteration.priority = priority
    iteration.status = status
    iteration.handler = handler
    iteration.start_time = start_time
    iteration.end_time = end_time
    iteration.type = type

    db.session.commit()

    return 'success'


@app.route('/iteration/deleteIters', methods=["GET", "POST"])
def deleteIters():
    """
    删除迭代
    """
    id = request.args.get('id')
    iteration = Iteration.query.filter(Iteration.id == id).first()
    db.session.delete(iteration)
    db.session.commit()

    need = Need.query.filter(Need.title==iteration.title).first()
    if need:
        need.iteration=""
    bug = Bugs.query.filter(Bugs.title==iteration.title).first()
    if bug:
        bug.iteration=""
    db.session.commit()

    return "success"


@app.route('/iteration/batchDeleteIters', methods=["GET", "POST"])
def batchDeleteIters():
    """
    批量删除迭代
    """
    ids = request.args.get('ids')
    iteration_ids = ids.split(',')

    for iteration_id in iteration_ids:
        n = Iteration.query.get(int(iteration_id))
        db.session.delete(n)
        db.session.commit()

        need = Need.query.filter(Need.title==n.title).first()
        if need:
            need.iteration=""
        bug = Need.query.filter(Bugs.title == n.title).first()
        if bug:
            bug.iteration = ""

        db.session.commit()

    return "success"

@app.route('/reportForms/report',methods=['GET','POST'])
def report():
    type = request.args.get('type')
    keyword = request.args.get('keyword')
    sendTime = request.args.get('sendTime')

    page = int(request.args.get('page', default=1))
    page_size = int(request.args.get('size', default=20))

    query = Report.query

    if type:
        query = query.filter(Report.type == type)
    if keyword:
        query = query.filter(
            or_(Report.subject.contains(keyword),Report.creater.contains(keyword)))
    if sendTime:
        query = query.filter(Report.sendTime == sendTime)

    total = query.count()
    reqult = query.order_by(desc("sendTime")).paginate(page, page_size, error_out=False)

    reportList = []

    for i in reqult.items:
        dict = {}
        dict["id"] = str(i.id)
        dict["subject"] = i.subject
        dict["status"] = i.status
        dict["sendTime"] = str(i.sendTime)
        dict["type"] = i.type
        dict["creater"] = i.creater
        reportList.append(dict)
    data = {
        "total": total,
        "reportList": reportList,
    }
    return data

@app.route('/reportForms/report/addReport',methods=['GET','POST'])
def addReport():
    subject = request.form.get('subject')
    sender = session.get('uname')
    recipients=request.form.get('recipient')
    copier = request.form.get('copier')
    conclusion = request.form.get('conclusion')
    need = request.form.get('need')
    bug = request.form.get('bug')
    purposes = request.form.get('purposes')
    environment = request.form.get('environment')

    files = request.files.getlist('file')

    version = request.form.get('version')
    updateContext = request.form.get('updateContext')
    testReport = request.form.get('testReport')
    attention = request.form.get('attention')
    sendTime = datetime.datetime.now().date()
    creater = session.get('uname')

    type = request.form.get("type")
    isSend = request.form.get("isSend")

    recipients = recipients.split(',')
    copier = copier.split(',')

    needs = ""
    if need:
        needIdArr = need.split(',')
        for needId in needIdArr:
            i = Need.query.filter(Need.id == needId).first()
            need_str = '<div>' + i.title + '  ' + i.priority + '  ' + i.status + '  ' + i.handler + '  ' + i.start_time + '  ' + i.end_time + '</div>'
            needs = needs + need_str

    bugs = ""
    if bug:
        bugIdArr = bug.split(',')
        for bugId in bugIdArr:
            i = Bugs.query.filter(Bugs.id == bugId).first()
            createTime = i.createTime.strftime("%Y-%m-%d")
            bug_str = '<div>' + i.title + '  ' + i.severity + '  ' + i.priority + '  ' + i.iteration + '  ' \
                      + i.status + '  ' + i.handler + '  ' + i.creater + '  ' + createTime + '</div>'
            bugs = bugs + bug_str


    if type=='1':
        if isSend == 'Y':
            text_body = "这是测试报告"
            text_html = "<html><header><h2>" + subject + "测试报告</h2></header>" \
                                "<body><div><b>一、测试结论</b></div>" + conclusion + \
                                "<div><b>二、测试目的</b></div>" + purposes + \
                                "<div><b>三、测试环境</b></div>" + environment + \
                                "<div><b>四、版本需求列表</b></div>" + needs + \
                                "<div><b>五、版本缺陷列表</b></div>" + bugs + "</body></html>"

            send_email(subject, sender, recipients+copier, text_body, text_html)
            status = "已发送"
        else:
            status="草稿"

    if type=='2':
        if isSend == 'Y':
            text_body = "这是发布报告"
            text_html = "<html><header><h2>" + subject + "发布报告</h2></header>" \
                                "<body><div><b>一、版本号</b></div>" + version + \
                                "<div><b>二、更新内容</b></div>" + updateContext + \
                                "<div><b>三、需求列表</b></div>" + needs + \
                                "<div><b>四、测试报告</b></div>" + testReport + \
                                "<div><b>五、注意事项</b></div>" + attention + \
                                "</body></html>"
            send_email(subject, sender, recipients+copier, text_body, text_html)
            status = "已发送"
        else:
            status="草稿"

    report = Report(subject=subject,recipients=";".join(recipients),copier=";".join(copier),conclusion=conclusion, purposes=purposes, environment=environment,
                    version=version, updateContext=updateContext, testReport=testReport,attention=attention, sendTime=sendTime,
                    creater=creater, type=type, status=status,needs=need,bugs=bug)
    db.session.add(report)
    db.session.commit()

    if files:
        for fname in files:
            new_fname = r'F:/tapd-demo/files/'  + fname.filename
            fname.save(new_fname)  # 保存文件到指定路径
            # 文件下载地址
            file_download = "http://localhost:8088/" + fname.filename
            file = Files(name=fname.filename,address=file_download,report_id=report.id)
            db.session.add(file)
            db.session.commit()


    return 'success'

@app.route('/reportForms/report/editReport',methods=['GET','POST'])
def editReport():
    subject = request.form.get('subject')
    sender = "1774454505@qq.com"
    recipients = request.form.get('recipient')
    copier = request.form.get('copier')
    conclusion = request.form.get('conclusion')
    need = request.form.get('need')
    bug = request.form.get('bug')
    purposes = request.form.get('purposes')
    environment = request.form.get('environment')

    files = request.files.getlist('file')

    version = request.form.get('version')
    updateContext = request.form.get('updateContext')
    testReport = request.form.get('testReport')
    attention = request.form.get('attention')
    sendTime = datetime.datetime.now().date()

    type = request.form.get("type")
    isSend = request.form.get("isSend")

    id = request.form.get('id')

    recipients = recipients.split(',')
    copier = copier.split(',')


    report = Report.query.filter(Report.id==id).first()

    needArr = []
    needs = ""
    needIdArr = need.split(',')
    for needId in needIdArr:
        one_need = Need.query.filter(Need.id == needId).first()
        needArr.append(one_need)

    for i in needArr:
        need_str = '<div>' + i.title + '  ' + i.priority + '  ' + i.status + '  ' + i.handler + '  ' + i.start_time + '  ' + i.end_time + '</div>'
        needs = needs + need_str

    bugArr = []
    bugs = ""
    bugIdArr = bug.split(',')
    for bugId in bugIdArr:
        one_bug = Bugs.query.filter(Bugs.id == bugId).first()
        bugArr.append(one_bug)

    for i in bugArr:
        createTime = i.createTime.strftime("%Y-%m-%d")
        bug_str = '<div>' + i.title + '  ' + i.severity + '  ' + i.priority + '  ' + i.iteration + '  ' \
                  + i.status + '  ' + i.handler + '  ' + i.creater + '  ' + createTime + '</div>'
        bugs = bugs + bug_str


    if type == '1':
        if isSend=='Y':
            text_body = "这是测试报告"
            text_html = "<html><header><h2>" + subject + "测试报告</h2></header>" \
                        "<body><div><b>一、测试结论</b></div>" + conclusion +  \
                        "<div><b>二、测试目的</b></div>" + purposes + \
                        "<div><b>三、测试环境</b></div>" + environment + \
                        "<div><b>四、版本需求列表</b></div>" + needs + \
                        "<div><b>五、版本缺陷列表</b></div>" + bugs + \
                        "</body></html>"

            send_email(subject, sender, recipients+copier, text_body, text_html)
            status="已发送"

        else:
            status = "草稿"

        recipients = ';'.join(recipients)
        copier = ';'.join(copier)
        report.subject = subject
        report.recipients = recipients
        report.copier = copier
        report.conclusion = conclusion
        report.purposes = purposes
        report.environment = environment
        report.sendTime = sendTime
        report.status = status
        report.needs = need
        report.bugs = bug

        if files:

            for fname in files:
                new_fname = r'F:/tapd-demo/files/' + fname.filename
                fname.save(new_fname)  # 保存文件到指定路径

                file = Files.query.filter(Files.report_id == id).all()
                for f in file:

                    f.name = fname.filename
                    f.file_download = "http://localhost:8088/" + fname.filename

                db.session.commit()

        db.session.commit()

    if type == '2':
        if isSend=='Y':
            text_body = "这是发布报告"
            text_html = "<html><header><h2>" + subject + "发布报告</h2></header>" \
                        "<body><div><b>一、版本号</b></div>" + version + \
                        "<div><b>二、更新内容</b></div>" + updateContext + \
                        "<div><b>三、需求列表</b></div>" + needs + \
                        "<div><b>四、测试报告</b></div>" + testReport + \
                        "<div><b>五、注意事项</b></div>" + attention + \
                        "</body></html>"
            send_email(subject, sender, recipients+copier, text_body, text_html)
            status = "已发送"

        else:
            status = "草稿"
        recipients = ';'.join(recipients)
        copier = ';'.join(copier)
        report.subject = subject
        report.recipients = recipients
        report.copier = copier
        report.version = version
        report.updateContext = updateContext
        report.purposes = purposes
        report.testReport = testReport
        report.attention = attention
        report.sendTime = sendTime
        report.status = status
        report.needs = need
        report.bugs = bug

        db.session.commit()


    return 'success'

@app.route('/reportForms/report/view',methods=['GET'])
def view():
    """
    获取报告信息
    """
    id = request.args.get('id')
    report = Report.query.filter(Report.id==id).first()
    if report:

        recipientList = report.recipients.split(';')
        recipient=""
        for r in recipientList:
            loginUser = LoginUser.query.filter(LoginUser.email==r).first()
            if recipient=="":
                recipient = loginUser.username
            else:
                recipient = recipient+ ';' + loginUser.username


        copierList = report.copier.split(';')
        copier = ""
        for c in copierList:
            loginUser = LoginUser.query.filter(LoginUser.email == c).first()
            if loginUser:
                if copier=="":
                    copier = loginUser.username
                else:
                    copier = copier+';' + loginUser.username

        result ={}

        dict={}
        dict["id"] = report.id
        dict["subject"] = report.subject
        dict["conclusion"] = report.conclusion
        dict["purposes"] = report.purposes
        dict["environment"] = report.environment
        dict["useCase"] = report.useCase
        dict["version"] = report.version
        dict["updateContext"] = report.updateContext
        dict["testReport"] = report.testReport
        dict["attention"] = report.attention
        dict["type"] = report.type
        dict['recipient'] = recipient
        dict['copier'] = copier #抄送者的姓名
        dict['copiers'] = report.copier #抄送者的邮箱
        dict['recipients'] = report.recipients
        need_list = []
        needIds = report.needs.split(',')
        for needId in needIds:
            need = Need.query.filter(Need.id == needId).first()
            if need:
                need_dict = {}
                need_dict["id"] = str(need.id)
                need_dict["title"] = need.title
                need_dict["priority"] = need.priority
                need_dict["iteration"] = need.iteration
                need_dict["status"] = need.status
                need_dict["handler"] = need.handler
                need_dict["start_time"] = need.start_time
                need_dict["end_time"] = need.end_time
                need_dict["type"] = need.type
                need_list.append(need_dict)

        dict['need']=need_list


        bug_list = []
        bugIds = report.bugs.split(',')
        for bugId in bugIds:
            bug = Bugs.query.filter(Bugs.id == bugId).first()
            if bug:
                createTime = bug.createTime.strftime("%Y-%m-%d")
                bug_dict = {}
                bug_dict['id'] = bug.id
                bug_dict['title'] = bug.title
                bug_dict['severity'] = bug.severity
                bug_dict['priority'] = bug.priority
                bug_dict['iteration'] = bug.iteration
                bug_dict['status'] = bug.status
                bug_dict['handler'] = bug.handler
                bug_dict['creater'] = bug.creater
                bug_dict['createTime'] = createTime
                bug_list.append(bug_dict)

        dict['bug'] = bug_list

        file_list = []
        files = Files.query.filter(Files.report_id == report.id).all()
        if files:
            for file in files:
                file_dict = {}
                file_dict['id'] = file.id
                file_dict['name'] = file.name
                file_dict['url'] = file.address
                file_list.append(file_dict)

        dict['files'] = file_list
        result.update(dict)

    data = {
        "code":"200",
        "result":result,
        "msg":"成功"
    }
    return data





@app.route('/reportForms/report/deleteReport',methods=["GET","POSt"])
def deleteReport():
    """
    删除报告
    """

    id = request.args.get('id')

    report = Report.query.filter(Report.id==id).first()
    files = Files.query.filter(Files.report_id == id).all()

    if files:
        for file in files:
            db.session.delete(file)
    db.session.delete(report)
    db.session.commit()

    return 'success'


@app.route('/reportForms/report/batchDeleteReport', methods=["GET", "POST"])
def batchDeleteReport():
    """
    批量删除报告
    """
    ids = request.args.get('ids')
    ids = ids.split(',')

    for id in ids:
        r = Report.query.get(int(id))
        fs = Files.query.filter(Files.report_id==id).all()
        if fs:
            for f in fs:
                db.session.delete(f)
        db.session.delete(r)
        db.session.commit()
    return "success"


















