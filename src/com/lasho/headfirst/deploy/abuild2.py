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
import errno
import ConfigParser
import datetime

class BuildUtils:
    # Configuration file name.
    def __init__(self, conf_file):
        print '__init__ called.'
        self.config_file = conf_file
        # -------------init--------------
        # Log path
        self.app_name=self.getConfig("common", "app_name")
        self.antx_prop_path=self.getConfig("common", "antx_prop_path")
        self.src_target_path=self.getConfig("common", "src_path")
        # [Remote server].
        self.remote_ip=self.getConfig("remote", "remote_ip")
        self.remote_usr=self.getConfig("remote", "remote_usr")
        self.remote_pwd=self.getConfig("remote", "remote_pwd")
        self.remote_target_path=self.getConfig("remote", "remote_target_path")
        self.log_path=self.getConfig("common", "log_path")
        # [SVN]
        self.svn_username=self.getConfig("svn", "svn_username")
        self.svn_password=self.getConfig("svn", "svn_password")
        self.svn_url=self.getConfig("svn", "svn_url")

    # Get configuration from the Config 
    def getConfig(self,section, key):
        config = ConfigParser.ConfigParser()
        config.read(self.config_file)
        return config.get(section, key)
    
    # Checkout the newarkstg repo via svn function.
    def svn_co(self):
        print ('svn co.')
        print 'Logs output to the '+self.log_path+'/svn_co.log'
        os.system('mkdir -p '+self.log_path+' 2>/dev/null >/dev/null')
        os.system("echo '' > "+self.log_path+"/svn_co.log")
        os.system('mkdir -p '+self.src_target_path+' 2>/dev/null >/dev/null')
        os.system('svn co --username '+self.svn_username+' --password '+self.svn_password+' '+self.svn_url+' '+self.src_target_path+' > '+self.log_path+'/svn_co.log')
        print ('svn_co finished!')
    
    # Update the newarkstg repo via svn function.
    def svn_update(self):
        print ('svn update.')
        print 'Logs output to the '+self.log_path+'/svn_update.log'
        os.system('mkdir -p '+self.log_path+' 2>/dev/null >/dev/null')
        os.system("echo '' > "+self.log_path+"/svn_update.log")
        os.system('mkdir -p '+self.src_target_path+' 2>/dev/null >/dev/null')
        os.system('svn update --username '+self.svn_username+' --password '+self.svn_password+' '+self.src_target_path+' > '+self.log_path+'/svn_update.log')
        print ('svn_update finished!')
        
    # mvn build & autoconfig function.
    def mvn_build(self):
        print ('mvn_build.')
        print 'Logs output to the '+self.log_path+'/mvn_build.log'
        os.system('mkdir -p '+self.log_path+' 2>/dev/null >/dev/null')
        os.system("echo '' > "+self.log_path+"/mvn_build.log")
        os.chdir(self.src_target_path)
        os.system('mvn clean install -DskipTests -Dautoconfig.userProperties='+self.antx_prop_path +' > '+self.log_path+'/mvn_build.log')
        print ('mvn_build finished!')
        
    # upload_product function.
    def upload_product(self):
    
        print ('upload_product')
        print 'Logs output to the '+self.log_path+'/upload_product.log'
    
        os.system('mkdir -p '+self.log_path+' 2>/dev/null >/dev/null')
        os.system("echo '' > "+self.log_path+"/upload_product.log")
        
        remote_shell = RemoteShell(self.remote_ip,self.remote_usr,self.remote_pwd)
        localfile = self.src_target_path+'/target/'+self.app_name+'.tar.gz'
        filename_suffix = datetime.datetime.now().strftime('%y%m%d%H%M%S');
        dest_file = self.remote_target_path+'/'+self.app_name+'.tgz.'+filename_suffix
        remote_shell.put(localfile, dest_file)
    
        print ('upload_product finished!')

# scp shell executor
class RemoteShell:
    def __init__(self, host, user, pwd):
        self.host = host
        self.user  = user
        self.pwd  = pwd

    def put(self, local_path, remote_path):
        scp_put = '''
        spawn scp %s %s@%s:%s
        expect "(yes/no)?" {
        send "yes\r"
        expect "password:"
        send "%s\r"
        } "password:" {send "%s\r"}
        expect eof
        exit'''
        os.system("echo '%s' > scp_put.cmd" % (scp_put % (os.path.expanduser(local_path), self.user, self.host, remote_path, self.pwd, self.pwd)))
        os.system('expect scp_put.cmd')
        os.system('rm scp_put.cmd')
# Main function.
def main(conf_file,argv):
    try:
        # If no arguments print usage
        if len(argv) == 0:
            usage()
            sys.exit()
        build = BuildUtils(conf_file)
        for i in range(len(argv)):
            if 'h' in argv[i] :
                usage()
                sys.exit()
            if 'o' in argv[i] :
                build.svn_co()
            if 'u' in argv[i] :
                build.svn_update()
            if 'b' in argv[i] :
                build.mvn_build()
            if 's' in argv[i]:
                build.upload_product()
    except getopt.GetoptError:
        # If an error happens print the usage and exit with an error       
        usage()
        sys.exit(errno.EIO)

"""
Prints out the usage for the command line.
"""
# Usage funtion.
def usage():
    usage = [" Svn co&update,mvn build,update package. Write in Python.\n"]
    usage.append("Version 1.0. By kane.ch . Email:qingxiang.cqx@alibaba-inc.com\n")
    usage.append("\n")
    usage.append("Format: python abuild2.py [-c aaa.conf] [-h][-o][-u][-b][-s]... \n")
    usage.append("Usage build&upload [-hcubs]\n")
    usage.append("  [-h ] Prints this help and usage message\n")
    usage.append("  [-o ] Checkout the source-code from svn\n")
    usage.append("  [-u ] Update the source-code from svn\n")
    usage.append("  [-b ] build package by maven\n")
    usage.append("  [-s ] upload package by SCP commond\n")
    message = string.join(usage)
    print message

# The entrance of program.
if __name__=='__main__':
    config_file = 'build_config.conf'
    args_index = 1
    if len(sys.argv)>1 and sys.argv[1] == '-c':
        config_file = sys.argv[2]
        args_index = 3
    main(config_file,sys.argv[args_index:])