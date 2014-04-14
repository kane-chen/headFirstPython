''' 
    author:kane
    description: file-operation
'''
from pickle import PickleError

# data = open('sketch.txt', mode='r', encoding=None, errors=None, newline=None, closefd=True, opener=None) ;
# for line in data :
# #     (role,words) = line.split(':') ;
#     if line.find(':') != -1 :#line contains :
#         (role,words) = line.split(':',1) ;
#         print(role,end='');
#         print('------',end='');
#         print(words);
# data.close();


#try except finally
# data = open('sketch.txt') ;
# for line in data :
#     try:
#         (role,words) = line.split(':',1) ;
#         print(role,end='');
#         print('========',end='');
#         print(words);
#     except ValueError:
#         pass ;
# data.close();

'''  os.path.exist '''
# import os ;
# if os.path.exists('sketch.txt') :
#     data = open('sketch.txt') ;
#     try:
#         for line in data :
#             (role,words) = line.split(':',1) ;
#             print(role,end='');
#             print('-------',end='');
# #             print(words);
#             print(words.strip());
#     except:
#         pass ;
#     finally:
#         data.close();
# else:
#     print('file not exist');    
    
    
import os ;
mans = [] ;
others = [] ;
try:
    data = open('sketch.txt') ;
#     data = open('sketch111.txt') ;#test file not found
    try:
        for line in data :
            (role,words) = line.split(':',1);
            if role == 'Man' :
                mans.append(words) ;
            elif role == 'Other Man' :
                others.append(words) ;
         
        data.close() ;
    except:
        pass ;
except IOError as err:
    print("ERROR:"+str(err));

# print(mans);    
# print(others);

''' open file '''
# try:
#     man_data = open('man_data.txt','w');
#     other_man_data = open('other_man.txt','w');
#     print(mans,file=man_data);
#     print(others,file=other_man_data);
# except:
#     print('file io exception');
# finally:
#     man_data.close();
#     other_man_data.close();
    
# try:
#     with open('man.txt','w') as man, open('others.txt','w') as others :
#         print(mans,file=man);
#         print(others,file=others);
# except IOError as err:
#     print('ERROR:'+str(err));

import pickle ;

try:
    with open('manpst.txt','wb') as manpest, open('otherpst.txt','wb') as otherpst:
        pickle.dump(mans, file=manpest);
        pickle.dump(others, file=otherpst);
except IOError as ioerr:
    print("IO-ERROR:"+str(ioerr));
except PickleError as pkerr:
    print("PICKLE-ERROR:"+str(pkerr));