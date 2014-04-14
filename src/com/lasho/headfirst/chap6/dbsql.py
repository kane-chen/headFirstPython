'''
Created on 2014-1-21
@author: Administrator
'''
import sqlite3 ;
from athelets import Athlete, get_data_in_file

db_name = 'athlete_db' ;

def create_table(db_name):
    conn = sqlite3.connect(db_name) ;
    cursor = conn.cursor();
    
    cursor.execute("create table athletes( id integer  primary key autoincrement not null, name text not null, birthday date )");
    cursor.execute("create table athletes_datas( id integer primary key autoincrement not null , athlete_id integer not null, value text not null,foreign key (athlete_id) references athletes)");
    conn.commit() ;
    conn.close() ;
   
# create_table('athlete_db');


def insert_data(db_name,athlete):
    conn = sqlite3.connect(db_name);
    cursor = conn.cursor() ;
    
    cursor.execute("insert into athletes(name,birthday)values(?,?)",(athlete.name,athlete.birth));
    conn.commit() ;
    conn.close() ;
    
def insert_detail(db_name,athlete,id):  # @ReservedAssignment
    conn = sqlite3.connect(db_name);
    cursor = conn.cursor() ;
    
    cursor.execute("insert into athletes_datas(athlete_id,value)values(?,?)",(id,str(athlete.top)));
    conn.commit() ;
    conn.close() ;

james = 'james2.txt' ;
athlete = get_data_in_file(james) ;
insert_data(db_name,athlete);
insert_detail(db_name,athlete,1);



def select_data(db_name,id):  # @ReservedAssignment
    conn = sqlite3.connect(db_name) ;
    cursor = conn.cursor() ;
    
    results = cursor.execute("select name,birthday,value from athletes ath left join athletes_datas det on ath.id = det.athlete_id where ath.id = ? ",(id,)) ;
    (name,birth,value) = results.fetchone();
#     print(name);
#     print(birth);
#     print(value);
    return Athlete(name,birth,value);
    
athlete = select_data(db_name,1);

def update_data(db_name,id,athlete):  # @ReservedAssignment
    conn = sqlite3.connect(db_name) ;
    cursor = conn.cursor() ;
    cursor.execute("update athletes set name = ? ,birthday= ? where id = ?",(athlete.name,athlete.birth,id));
    conn.commit();
    conn.close();

id = 1 ;  # @ReservedAssignment
athlete = select_data(db_name,id);
print(athlete.name);
athlete.name = 'lebron james' ;
update_data(db_name,id,athlete);    
athlete = select_data(db_name,id);
print(athlete.name);
