def format_data(data):
    if '-' in data:
        sep = '-' ;
    elif ':' in data:
        sep = ':' ;
    else:
        return data ;
    (mins,secs) = data.split(sep) ;
    return mins+'.'+secs ;

try:
    jamesData = [] ;
    with open('james.txt') as james:
        datas = james.readline().split(',') ;
        for data in datas :
            jamesData.append(format_data(data));
        print(jamesData);
        jamesData = sorted(jamesData);#list sort
        print(jamesData);
        jamesData = set(jdata for jdata in jamesData);#remove duplicate
        print(jamesData);
        print(sorted(jamesData)[0:3]);#range
        
        print(sorted(set(jdata for jdata in jamesData))[0:3]) ;
except:
    pass
