'''
    author:kane
    description: my-first-python
'''
# print('welcome');

''' array traversal '''
# teams = ['bullds','lakers','nets','knicks'] ;
# for team in teams :
#     print(team);
# print(teams[2]);

''' mulit-types in array '''
movie = ["The Holy Grail", 1975, "Terry Jones & Terry Gilliam", 91, 
            ["Graham Chapman", 
                ["Michael Palin", "John Cleese","Terry Gilliam", "Eric Idle", "Terry Jones"]
            ]
         ] ;

# for prop in movie :
#     print(prop);
 
''' is-instance '''   
# for prop in movie :
#     if isinstance(prop, list) : 
#         for lprop in prop :
#             print(lprop) ;
#     else :
#         print(prop);
        
''' recursion ''' 
# def print_recursion(param):  
#     if isinstance(param, list):
#         for prop in param:
#             print_recursion(prop) ;
#     else:
#         print(param) ;
# 
# print_recursion('hello world');
# print_recursion(movie);

def print_recursion_blank(param, level=0):
    if isinstance(param, list):
        for prop in param :
            print_recursion_blank(prop,level+1);
    else :
        for tlevel in range(level) :  # @UnusedVariable
            print('\t',end='');
        print(param);
        
print_recursion_blank(movie,1) ;
    
    