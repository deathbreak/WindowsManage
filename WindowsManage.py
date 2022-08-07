import subprocess
import os
import sqlite3
import datetime as dtm


def create_table():
    c = conn.cursor()
    c.execute('''CREATE TABLE IF NOT EXISTS  
           KeyUrls(id       INTEGER   primary key AUTOINCREMENT,      -- select last_insert_rowid()
           keywords           CHAR(50)   NOT NULL,  -- 关键词，用于搜索
           tips           CHAR(200),     -- 备注
           urlinfo           CHAR(200),   -- 软件存放路径/打开文件路径/""(资源为备忘录的情况下) 
           signinfo           INT,    -- 对应上面(0/1/2)
           starinfo           INT,    -- 重要星级(0/1/2)
           timeinfo          CHAR(50)   -- 时间信息
           );''')
    conn.commit()


def add_it(str1, str2, str3, int4, int5, str6):
    c = conn.cursor()
    c.execute(
        '''INSERT INTO KeyUrls 
        VALUES (null ,'%s','%s','%s', %d, %d,'%s') ''' % (str1, str2, str3, int4, int5, str6))
    conn.commit()
    print("添加成功!!!")


def run_it():
    c = conn.cursor()
    cursor = c.execute("SELECT id, name  from user")
    print(cursor.fetchall())


def del_it(str1):
    c = conn.cursor()
    c.execute("DELETE from KeyUrls where ID= '%s'" % str1)
    conn.commit()
    print("删除成功!!!")


def set_it():
    c = conn.cursor()
    c.execute("DELETE from user where ID=2;")
    conn.commit()


'''
            KeyUrls   
            id           INTEGER     primary key AUTOINCREMENT
            keywords     CHAR(50)     -- 关键词，用于搜索
            tips         CHAR(200)    -- 备注
            urlinfo      CHAR(200)    -- 软件存放路径/打开文件路径/""(资源为备忘录的情况下) 
            signinfo     INT          -- 对应上面(0/1)
            starinfo     INT          -- 重要星级(0/1/2)
            timeinfo     CHAR(50)     -- 时间信息
            '''


def query_by_keyword(keyword):
    c = conn.cursor()
    cursor = c.execute(
        '''select * from KeyUrls where `keywords` like '%s' ''' % ('%' + keyword + '%'))
    list_info = cursor.fetchall()
    # conn.close()
    return len(list_info), list_info


def check_input_str(str_line):
    if len(str_line) < 5:
        return False
    else:
        if index_plus(str_line, "run ") or index_plus(str_line, "del ") or index_plus(str_line, "set ") or index_plus(
                str_line, "add "):
            return True
        else:
            return False


def index_plus(str1, str2):
    try:
        return True if str1.index(str2) == 0 else False
    except ValueError:
        return False


def print_tips_input():
    print("*******************")
    print("输入命令有误,请重新输入")
    print("run + * : 启动")
    print("add + * : 添加")
    print("set + * : 修改")
    print("del + * : 删除")
    print(dtm.datetime.strftime(dtm.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    print("*******************")


def print_tips_input_index():
    print("*******************")
    print("欢迎使用")
    print("run + * : 启动")
    print("add + * : 添加")
    print("set + * : 修改")
    print("del + * : 删除")
    print(dtm.datetime.strftime(dtm.datetime.now(), '%Y-%m-%d %H:%M:%S'))
    print("*******************")


def list_contains_key(id_temp, listinfo):
    list_temp = []
    list_re = []
    for ii in range(len(listinfo)):
        list_temp.append(str(listinfo[ii][0]))
        # print(str(listinfo[ii][0]), type(str(listinfo[ii][0])))
        if id_temp == str(listinfo[ii][0]):
            list_re = listinfo[ii]
            # print(list_re)
    return True if id_temp in list_temp else False, list_re


if __name__ == "__main__":
    conn = sqlite3.connect('winmanage.db')
    create_table()
    print_tips_input_index()
    while True:
        line = input("请输入命令:")  # run/set/del  run 1
        if check_input_str(line):
            keywords = line[4:].strip()
            command_str = line[0:3]
            print("输入关键词是", keywords)
            '''
            KeyUrls   
            id           INTEGER     primary key AUTOINCREMENT
            keywords     CHAR(50)     -- 关键词，用于搜索
            tips         CHAR(200)    -- 备注
            urlinfo      CHAR(200)    -- 软件存放路径/打开文件路径/""(资源为备忘录的情况下) 
            signinfo     INT          -- 对应上面(0/1)
            starinfo     INT          -- 重要星级(0/1/2)
            timeinfo     CHAR(50)     -- 时间信息
            '''
            if command_str == "add":
                # your_keywords = input("请重新输入需要添加的关键词:")
                your_keywords = keywords
                len_re, re = query_by_keyword(your_keywords)
                if len_re != 0:
                    print("已存在保存的关键词信息%s条,对应详细信息如下:" % len_re)
                    for i in range(len_re):
                        print("------------------------")
                        print("id:    ", re[i][0])
                        print("关键词: ", re[i][1])
                        print("备注:   ", re[i][2])
                        print("存放路径:", re[i][3])
                        print("重要程度:", re[i][5])
                        print("更新时间:", re[i][6])
                        print("------------------------")
                    continue_flag = input("继续添加输入 y ,退出请输入 n :")
                    if continue_flag == "y":
                        your_urlinfo2 = input("请输入软件存放路径/打开文件的路径/__(资源为备忘录的情况下输入0):")
                        your_tips2 = input("请输入备注信息:")
                        signinfo2 = 1 if your_urlinfo2 != "0" else 0
                        try:
                            your_starinfo2 = int(input("请输入url星级:0->不重要,1->一般,2->重要"))
                        except ValueError:
                            print("输入格式错误,添加失败!!!")
                            continue
                        it_timeinfo2 = dtm.datetime.strftime(dtm.datetime.now(), '%Y-%m-%d %H:%M:%S')
                        add_it(your_keywords, your_tips2, your_urlinfo2, signinfo2, your_starinfo2, it_timeinfo2)
                    else:
                        print("退出!!!")
                else:
                    your_urlinfo = input("请输入软件存放路径/打开文件的路径/__(资源为备忘录的情况下输入0):")
                    your_tips = input("请输入备注信息:")
                    signinfo = 1 if your_urlinfo != "0" else 0
                    try:
                        your_starinfo = int(input("请输入url星级:0->不重要,1->一般,2->重要"))
                    except ValueError:
                        print("输入格式错误,添加失败!!!")
                        continue
                    it_timeinfo = dtm.datetime.strftime(dtm.datetime.now(), '%Y-%m-%d %H:%M:%S')
                    add_it(your_keywords, your_tips, your_urlinfo, signinfo, your_starinfo, it_timeinfo)
            if command_str == "run":
                run_keywords = keywords
                len_run, run = query_by_keyword(run_keywords)
                if len_run == 1 and run[0][4] == 1:
                    os.startfile(r'%s' % run[0][3])
                    print("执行成功!!!")
                    # continue
                elif len_run == 1 and run[0][4] == 0:
                    print("备注信息是:", run[0][2])
                elif len_run == 0:
                    print("未找到相关信息!")
                else:
                    print("找到%s条相似信息,对应信息如下:" % len_run)
                    for i in range(len_run):
                        print("------------------------")
                        print("id:    ", run[i][0])
                        print("关键词: ", run[i][1])
                        print("备注:   ", run[i][2])
                        print("存放路径:", run[i][3])
                        print("重要程度:", run[i][5])
                        print("更新时间:", run[i][6])
                        print("------------------------")
                    choose_id = input("请输入需要执行的id:")
                    check_id, re_info = list_contains_key(choose_id, run)
                    # print(check_id, re_info)
                    if check_id and re_info[4] == 1:
                        os.startfile(r'%s' % re_info[3])
                    elif check_id and re_info[4] == 0:
                        print("备注信息是:", re_info[2])
                    else:
                        print("输入id不在命令id内!!!")

            if command_str == "set":
                print("暂时没写这个功能!!!")
            if command_str == "del":
                del_keywords = keywords
                len_re_del, re_del = query_by_keyword(del_keywords)
                if len_re_del == 0:
                    print("不存在关键词对应的信息!!!")
                else:
                    print("数据库中找到的对应信息:")
                    list_range_del = []
                    for i in range(len_re_del):
                        print("------------------------")
                        print("id:    ", re_del[i][0])
                        print("关键词: ", re_del[i][1])
                        print("备注:   ", re_del[i][2])
                        print("存放路径:", re_del[i][3])
                        print("重要程度:", re_del[i][5])
                        print("更新时间:", re_del[i][6])
                        print("------------------------")
                        list_range_del.append(re_del[i][0])
                    try:
                        del_id = int(input("请输入要删除的id:"))
                    except ValueError:
                        print("输入格式错误,删除失败!!!")
                        continue
                    if del_id in list_range_del:
                        del_it(del_id)
                    else:
                        print("输入的id不在可选删除范围内")
        else:
            print_tips_input()
