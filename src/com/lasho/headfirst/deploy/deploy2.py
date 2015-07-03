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
class DeployUtils:
    def __init__(self, conf_file):
        print '__init__ called.'
        self.conf_file = conf_file
        #config
        self.log_path=self.getConfig("common", "log_path")
        self.app_name=self.getConfig("common", "app_name")
        self.backup_path=self.getConfig("common", "backup_path")
        self.products_path=self.getConfig("common", "pro_path")
        #deploy
        self.deploy_home=self.getConfig("deploy", "deploy_home")
        self.bin_path = self.deploy_home +'/bin/'
        self.deploy_path = self.deploy_home + '/target/'
        self.dest_file_name = self.app_name+ '.tgz'
        #monitor
        self.monitor_url=self.getConfig("monitor", "monitor_url")
    # Get configuration from the Config 
    def getConfig(self,section, key):
        config = ConfigParser.ConfigParser()
        path = os.path.split(os.path.realpath(__file__))[0] + '/'+self.conf_file
        config.read(path)
        return config.get(section, key)
    
    # pro_backup function.
    def pro_backup(self):
    
        print ('pre-product backup.')
        print 'Logs output to the '+self.log_path+'/deploy.log'
    
        os.system('mkdir -p '+self.backup_path+' 2>/dev/null >/dev/null')
        #deploy-file
        deploy_dest_file = self.deploy_path + '/' + self.dest_file_name
        #backup-file
        backup_file = self.backup_path + '/' + self.dest_file_name + '.' + datetime.datetime.now().strftime('%y%m%d%H%M%S')
        os.system('cp '+deploy_dest_file+' '+backup_file+' > '+self.log_path+'/deploy.log')
    
        print ('backup finished!')
    
    # pro_replace function.
    def pro_replace(self):
    
        print ('pro_replace.')
        print 'Logs output to the '+self.log_path+'/deploy.log'
    
        os.system('mkdir -p '+self.log_path+' 2>/dev/null >/dev/null')
        #deploy-file
        deploy_dest_file = self.deploy_path + '/' + self.dest_file_name
        #new-deploy-file
        new_deploy_dest_file =  self.products_path + '/' + self.dest_file_name
        #replace
        os.system('cp '+new_deploy_dest_file+' '+deploy_dest_file+' > '+self.log_path+'/deploy.log')
    
        print ('pro_replace finished!')
        
    # mvn build & autoconfig function.
    def server_restart(self):
    
        print ('server_restart.')
        print 'Logs output to the '+self.log_path+'/deploy.log'
    
        os.system('mkdir -p '+self.log_path+' 2>/dev/null >/dev/null')
        os.system("echo '' > "+self.log_path+"/deploy.log")
        stop_shell = self.bin_path + 'killws.sh'
        start_shell = self.bin_path + 'startws.sh'
        os.system('sh '+ stop_shell +'; sh '+ start_shell +' > '+self.log_path+'/deploy.log')
    
        print ('server_restart finished!')
        
    # server_monitor function.
    def server_monitor(self):
    
        print ('server_monitor')
        print 'Logs output to the '+self.log_path+'/deploy.log'
        
        os.system('mkdir -p '+self.log_path+' 2>/dev/null >/dev/null')
        resp = commands.getoutput('curl '+self.monitor_url)
        os.system('echo '+ resp+ ' > '+self.log_path+"/deploy.log")
        print 'monitor response '+resp
        print ('server_monitor finished!')

        

# Main function.
def main(conf_file,argv):
    try:
        # If no arguments print usage
        if len(argv) == 0:
            usage()
            sys.exit()
        deploy = DeployUtils(conf_file)
        for i in range(len(argv)):
            if 'h' in argv[i] :
                usage()
                sys.exit()
            if 'b' in argv[i] :
                deploy.pro_backup()
            if 's' in argv[i] :
                deploy.pro_replace()
            if 'r' in argv[i] :
                deploy.server_restart()
            if 'm' in argv[i]:
                deploy.server_monitor()
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
    usage.append("Format: python deploy2.py [-c aaa.conf] [-h][-b][-s][-r][-m]... \n")
    usage.append("Usage backup,replace,restart,monitor [-hbsrm]\n")
    usage.append("  [-h ] Prints this help and usage message\n")
    usage.append("  [-b ] backup pre-product\n")
    usage.append("  [-s ] replace with new-product\n")
    usage.append("  [-r ] restart the app-server\n")
    usage.append("  [-m ] check app-server with monitor\n")
    message = string.join(usage)
    print message

# The entrance of program.
if __name__=='__main__':
    config_file = 'deploy_config.conf'
    args_index = 1
    if len(sys.argv)>1 and sys.argv[1] == '-c':
        config_file = sys.argv[2]
        args_index = 3
    main(config_file,sys.argv[args_index:])
