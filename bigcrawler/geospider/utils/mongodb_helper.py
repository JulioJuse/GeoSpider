# -*- encoding: utf-8 -*-
from bson import ObjectId
from pymongo import MongoClient

from geospider.utils.settings_helper import get_attr

'''
    连接mongodb数据库
'''
def connect_mongodb():
    mongo_url = get_attr('MONGO_URI')
    client = MongoClient(mongo_url)
    db = client.news  # 'examples' here is the database name.it will be created if it does not exist.
    # 如果 examples不存在，那么就会新建它
    return db


'''
    爬虫任务实体类数据访问层
'''
class TaskDao(object):
    def __init__(self, db):
        self.db = db

    '''根据taskid查找Task'''
    def find_by_id(self, id):
        return self.db.task.find_one({'_id': ObjectId(id)})

    '''根据状态status查找Task'''
    def find_by_localhost_and_status(self, localhost, status):
        cursor = self.db.task.find({'status': status})
        task_list = []
        for i in cursor:
            if localhost in i['slave']:
                task_list.append(i)
        return task_list

    '''保存一个Task，如果存在则更新，不存在则插入'''
    def save(self, task):
        self.db.task.save(task)

'''
    进程数据访问层
'''
class ProcessDao(object):
    def __init__(self, db):
        self.db = db

    '''查找所有'''
    def find_all(self):
        cursor = self.db.process.find()
        process_list = []
        for i in cursor:
            process_list.append(i)
        return process_list

    '''根据状态status查找'''
    def find_by_status(self, status):
        cursor = self.db.process.find({'status': status})
        process_list = []
        for i in cursor:
            process_list.append(i)
        return process_list

    '''根据本机ip和任务id查找进程'''
    def find_by_localhost_and_taskid(self, localhost, taskid):
        cursor = self.db.process.find({'localhost':localhost, 'taskid': taskid})
        process_list = []
        for i in cursor:
            process_list.append(i)
        return process_list

    def find_by_localhost(self, localhost):
        cursor = self.db.process.find({'localhost': localhost})
        process_list = []
        for i in cursor:
            process_list.append(i)
        return process_list

    '''
        新增一个进程
        pid:进程号
        taskid:任务编号
        status：进程状态
    '''
    def insert_process(self, localhost, pid, taskid, status):
        self.db.process.insert_one({'localhost':localhost, 'pid': pid, 'taskid': taskid, 'status': status})

    '''删除一个进程'''
    def delete_by_localhost_and_taskid(self, localhost, taskid):
        self.db.process.remove({'localhost':localhost, "taskid": taskid})

    '''更新进程状态'''
    def update_status_by_localhost_and_taskid(self, localhost, taskid, status):
        task_list = self.find_by_localhost_and_taskid(localhost, taskid)
        for task in task_list:
            task['status'] = status
            self.db.process.save(task)
            # task['status']=status

            # self.db.process.save(task)

class NewsDao(object):
    def __init__(self, db):
        self.db = db

    def find_urls_by_taksid(self, taskid):
        cursor = self.db.news.find({'taskid': taskid})
        url_list = []
        for i in cursor:
            url_list.append(i['url'])
        return url_list

class URLDao(object):
    def __init__(self, db):
        self.db = db

    def insert_url(self, taskid, url):
        self.db.urls.insert_one({'taskid':taskid, 'url':url})

    def delete_url(self, taskid, url):
        self.db.urls.remove({'taskid':taskid, 'url':url})

if __name__ == '__main__':
    db = connect_mongodb()
    # pro = ProcessDao(db)
    td = TaskDao(db)
    # task = td.find_by_localhost_and_status('127.0.0.1','running')
    # print(task)
    newsdao = NewsDao(db)
    list = newsdao.find_urls_by_taksid('594d0c669c1da962bd4b1457')
    for i in list:
        print i
