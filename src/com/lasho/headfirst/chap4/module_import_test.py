'''
Created on 2014-1-21
@author: Administrator
'''
#import class/method
from athelets import get_data_filelist, get_data_in_file

james = get_data_in_file('james2.txt')
print(james.name);
print(get_data_filelist(['james2.txt']));
