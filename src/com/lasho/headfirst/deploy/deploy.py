"""
-----------------------------------------------------------------------------
Svn co&update,mvn build,update package

Use the -h or the --help flag to get a listing of options.

Program: Build application
Author: kane.ch
Date: July 2, 2015
Revision: 1.0
"""
import os
import sys, getopt
import string
import datetime
import errno
import ConfigParser
import commands
# Configuration file name.
config_file='deploy_config.conf'

# Get configuration from the Config 
def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/'+config_file
    config.read(path)
    return config.get(section, key)

#config
log_path=getConfig("common", "log_path")
app_name=getConfig("common", "app_name")
backup_path=getConfig("common", "backup_path")
products_path=getConfig("common", "pro_path")
#deploy
deploy_home=getConfig("deploy", "deploy_home")
bin_path = deploy_home +'/bin/'
deploy_path = deploy_home + '/target/'
dest_file_name = app_name+ '.tgz'
#monitor
monitor_url=getConfig("monitor", "monitor_url")

# Main function.
def main(argv):
    try:
        # If no arguments print usage
        if len(argv) == 0:
            usage()
            sys.exit()
        
        for i in range(len(argv)):
            if argv[i] == "-h" or argv[i] == "--help":
                usage()
                sys.exit()
            elif argv[i] == "-b" or argv[i] == "--backup":
                pro_backup()
            elif argv[i] == "-s" or argv[i] == "--replace(switch)":
                pro_replace()
            elif argv[i] == "-r" or argv[i] == "--restart":
                server_restart()
            elif argv[i] == "-m" or argv[i] == "--monitor":
                server_monitor()
    except getopt.GetoptError:
        # If an error happens print the usage and exit with an error       
        usage()
        sys.exit(errno.EIO)

"""
Prints out the usage for the command line.
"""
# Usage funtion.
def usage():
    usage = [" Deploy:backup,replace,restart,monitor. Write in Python.\n"]
    usage.append("Version 1.0. By kane.ch . Email:qingxiang.cqx@alibaba-inc.com\n")
    usage.append("\n")
    usage.append("Usage backup,replace,restart,monitor [-hbsrm]\n")
    usage.append("  [-h | --help] Prints this help and usage message\n")
    usage.append("  [-b | --backup] backup pre-product\n")
    usage.append("  [-s | --replace] replace with new-product\n")
    usage.append("  [-r | --restart] restart the app-server\n")
    usage.append("  [-m | --monitor] check app-server with monitor\n")
    message = string.join(usage)
    print message

# pro_backup function.
def pro_backup():

    print ('pre-product backup.')
    print 'Logs output to the '+log_path+'/deploy.log'

    os.system('mkdir -p '+backup_path+' 2>/dev/null >/dev/null')
    #deploy-file
    deploy_dest_file = deploy_path + '/' + dest_file_name
    #backup-file
    backup_file = backup_path + '/' + dest_file_name + '.' + datetime.datetime.now().strftime('%y%m%d%H%M%S')
    os.system('cp '+deploy_dest_file+' '+backup_file+' > '+log_path+'/deploy.log')

    print ('backup finished!')

# pro_replace function.
def pro_replace():

    print ('pro_replace.')
    print 'Logs output to the '+log_path+'/deploy.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    #deploy-file
    deploy_dest_file = deploy_path + '/' + dest_file_name
    #new-deploy-file
    new_deploy_dest_file =  products_path + '/' + dest_file_name
    #replace
    os.system('cp '+new_deploy_dest_file+' '+deploy_dest_file+' > '+log_path+'/deploy.log')

    print ('pro_replace finished!')
    
# mvn build & autoconfig function.
def server_restart():

    print ('server_restart.')
    print 'Logs output to the '+log_path+'/deploy.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/deploy.log")
    stop_shell = bin_path + 'killws.sh'
    start_shell = bin_path + 'startws.sh'
    os.system('sh '+ stop_shell +'; sh '+ start_shell +' > ../'+log_path+'/deploy.log')

    print ('server_restart finished!')
    
# server_monitor function.
def server_monitor():

    print ('server_monitor')
    print 'Logs output to the '+log_path+'/deploy.log'
    
    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    resp = commands.getoutput('curl '+monitor_url)
    os.system('echo '+ resp+ ' > '+log_path+"/deploy.log")
    print 'monitor response '+resp
    print ('server_monitor finished!')

# The entrance of program.
if __name__=='__main__':
    main(sys.argv[1:])
