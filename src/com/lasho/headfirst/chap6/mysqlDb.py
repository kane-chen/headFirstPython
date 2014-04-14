'''
Created on 2014-1-21

@author: Administrator
'''

import mysql.connector ;

try:
    mysql_config = {
                    'host':'127.0.0.1',
                    'user':'root',
                    'password':'',
                    'port':'3306',
                    'database':'test'
                    };
    conn = mysql.connector.connect(**mysql_config);
    print('connect success');
    #insert
    isql = 'insert into code(code,sp_id,pasword,remark) values(%(code)s,%(sp_id)s,%(pasword)s,%(remark)s)' ;
    iparams = {'code':'100007','sp_id':1001,'pasword':'888888','remark':'mmmmmmmm'} ;
    #query
    ssql = 'select code,pasword from code where id = %(id)s'
    sparams = {'id':'5'} 
    #delete
    rsql = 'delete from code where id=%s'
    rparams = (5,)
    try:
        cursor = conn.cursor();
        cursor.execute(rsql,rparams);
#         for (code,pwd) in cursor:
#             print('code=%s,pasword=%s'%(code,pwd));
        print('operate success')
    except mysql.connector.Error as ceer:
        print(ceer)
    finally:
        conn.close();
except mysql.connector.Error as err:
    print(str(err)) ;
    