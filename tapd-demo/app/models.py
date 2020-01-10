from app import db
from datetime import date

class LoginUser(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    username = db.Column(db.String(64))
    password_hash = db.Column(db.String(128))
    sex = db.Column(db.String(32),nullable=True,comment="性别 1男 2女")
    Position = db.Column(db.String(64),nullable=True,comment="职位")
    email = db.Column(db.String(120),unique=True)

class Menus(db.Model):
    id = db.Column(db.Integer,primary_key=True)
    action = db.Column(db.String(64))
    name= db.Column(db.String(64))
    parentId=db.Column(db.Integer)
    rank = db.Column(db.Integer)
    type = db.Column(db.Integer)
    icon = db.Column(db.String(64))
    menus = []

class Iteration(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128),nullable=False)
    priority = db.Column(db.String(64),nullable=False,comment='优先级')
    status = db.Column(db.String(64),nullable=False)
    handler = db.Column(db.String(64),nullable=False)
    start_time = db.Column(db.String(64),nullable=False,comment='预计开始时间')
    end_time = db.Column(db.String(64),nullable=False,comment='预计结束时间')
    type = db.Column(db.Integer,nullable=False,comment="迭代类型 1当前迭代 2下个迭代 3已完成迭代")

class Report(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    subject = db.Column(db.String(128),nullable=True)
    recipients = db.Column(db.String(128),nullable=True)#收件人
    copier = db.Column(db.String(128),nullable=True)#抄送人
    conclusion = db.Column(db.String(128),nullable=True)
    purposes = db.Column(db.String(128),nullable=True)
    environment = db.Column(db.String(64),nullable=True)
    useCase = db.Column(db.String(64),nullable=True)
    version = db.Column(db.String(64),nullable=True)
    updateContext = db.Column(db.String(64),nullable=True)
    testReport = db.Column(db.String(64),nullable=True)
    attention = db.Column(db.String(64),nullable=True)
    status = db.Column(db.String(64),nullable=True)
    sendTime = db.Column(db.Date, default=date.today())
    creater = db.Column(db.String(64),nullable=True,comment='创建人')
    type = db.Column(db.Integer,nullable=True,comment="报告 1测试报告 2发布报告")
    needs = db.Column(db.String(64),nullable=True)
    bugs = db.Column(db.String(64),nullable=True)


class Need(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128),nullable=False)
    priority = db.Column(db.String(64),nullable=False,comment='优先级')
    iteration= db.Column(db.String(64),nullable=True)
    status = db.Column(db.String(64),nullable=False)
    handler = db.Column(db.String(64),nullable=False)
    start_time = db.Column(db.String(64),nullable=False,comment='预计开始时间')
    end_time = db.Column(db.String(64),nullable=False,comment='预计结束时间')
    type = db.Column(db.Integer,nullable=False,comment="需求类型 1产品 2运营 3设计 4技术")
    report_id = db.Column(db.Integer,db.ForeignKey('report.id'))




class Bugs(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String(128),nullable=False)
    severity = db.Column(db.String(128),nullable=False)
    priority = db.Column(db.String(64),nullable=False,comment='优先级')
    iteration= db.Column(db.String(64),nullable=True)
    status = db.Column(db.String(64),nullable=False)
    handler = db.Column(db.String(64),nullable=False)
    creater = db.Column(db.String(64),nullable=False,comment='创建人')
    createTime = db.Column(db.Date, default=date.today())
    type = db.Column(db.Integer,nullable=False,comment="缺陷 1缺陷列表 2缺陷池")
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))


class Files(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128),nullable=False)
    address = db.Column(db.String(128),nullable=False)
    report_id = db.Column(db.Integer, db.ForeignKey('report.id'))










