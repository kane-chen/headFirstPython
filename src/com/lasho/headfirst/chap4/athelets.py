import os ; 

def grade_format(grade):
    if '-' in grade :
        sep = '-' ;
    elif ':' in grade :
        sep = ':' ;
    else :
        return grade ;
    (mins,secs) = grade.split(sep);
    return mins+'.'+secs ;

# try:
#     with open('james2.txt') as jamesFile :
#         jamesData = jamesFile.readline().split(',',2) ;
#         jmap = {} ;
#         jmap['name'] = jamesData.pop(0) ;
#         jmap['birthday'] = jamesData.pop(0) ;
#         grades = jamesData.pop().split(',') ;
#         print(grades);
# #         jmap['grade'] = [grade_format(grade) for grade in grades] ;
#         jmap['grade'] = set([grade_format(grade) for grade in grades]) ;
#         jmap['grade'] = sorted(set([grade_format(grade) for grade in grades]),reverse=True)[0:3] ;
#         print(jmap);
# except :
#     pass ;


class Athlete(list):#extends list
    def __init__(self,name,birth=None,grades=[]):
        list.__init__([]) ;#init
        self.name = name ;
        self.birth = birth ;
#         self.grades = grades ;
        self.extend(grades) ;
    def top(self,topSize = 3,order = False):
#         return sorted(set([grade_format(grade) for grade in self.grades]),reverse=order)[0:topSize] ;
        return sorted(set([grade_format(grade) for grade in self]),reverse=order)[0:topSize] ;

def get_data_in_file(file_name):
    if os.path.exists(file_name):
        with open(file_name) as file :
            content = file.readline().strip() ;
            datas = content.split(',',2);

#             dataInMap = {} ;
#             dataInMap['name'] = datas.pop(0);
#             dataInMap['birth'] = datas.pop(0) ;
#             grades = datas.pop(0).split(',') ;
#             dataInMap['grades'] = sorted(set([grade_format(grade) for grade in grades]))[0:3] ;
#             return dataInMap ;

            return (Athlete(datas.pop(0), datas.pop(0), datas.pop().split(',')));
    else :
        print('file not found');
#james        
# james = 'james2.txt' ; 
# dmap = get_data_in_file(james);
# print(dmap);
#julie        
julie = 'julie2.txt' ; 
athlete = get_data_in_file(julie);
print(athlete.name + " ====== " + str(athlete.top(5,False)));



# list-recursion
def get_data_filelist(files):
    athletes = {} ;
    for filename in files :
        athlete = get_data_in_file(filename) ;
        athletes[athlete.name] = athlete ;
    return athletes ;

import pickle ;

files = ('james2.txt','julie2.txt','mikey2.txt','sarah2.txt');
athelets = get_data_filelist(files);
print(athelets);
try:
    with open('athelets_dump.txt','wb') as atheletfile:
        pickle.dump(athelets, atheletfile);
except IOError as ioerr:
    print(str(ioerr));

try:
    with open('athelets_dump.txt','rb') as atheletrf:
        athleter = pickle.load(atheletrf);
        print(athleter);
except IOError as ioerr:
    print(str(ioerr));
    