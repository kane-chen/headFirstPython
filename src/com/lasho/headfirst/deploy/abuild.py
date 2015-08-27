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

# Configuration file name.
config_file='build_config.conf'

# Get configuration from the Config 
def getConfig(section, key):
    config = ConfigParser.ConfigParser()
    path = os.path.split(os.path.realpath(__file__))[0] + '/'+config_file
    config.read(path)
    return config.get(section, key)

# Log path
log_path=getConfig("common", "log_path")
app_name=getConfig("common", "app_name")
antx_prop_path=getConfig("common", "antx_prop_path")
src_target_path=getConfig("common", "src_path")
# [Remote server].
remote_ip=getConfig("remote", "remote_ip")
remote_usr=getConfig("remote", "remote_usr")
remote_pwd=getConfig("remote", "remote_pwd")
remote_target_path=getConfig("remote", "remote_target_path")

# [SVN]
svn_username=getConfig("svn", "svn_username")
svn_password=getConfig("svn", "svn_password")
svn_url=getConfig("svn", "svn_url")


# Main function.
def main(argv):
    try:
        # If no arguments print usage
        if len(argv) == 0:
            usage()
            sys.exit()

        for i in range(len(argv)):
            # Receive the command line arguments. The execute the corresponding function.
            if argv[i] == "-h" or argv[i] == "--help":
                usage()
                sys.exit()
            elif argv[i] == "-c" or argv[i] == "--svn-co":
                svn_co()
            elif argv[i] == "-u" or argv[i] == "--svn-update":
                svn_update()
            elif argv[i] == "-b" or argv[i] == "--mvn build":
                mvn_build()
            elif argv[i] == "-s" or argv[i] == "--upload":
                upload_product()
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
    usage.append("Usage build&upload [-hcubs]\n")
    usage.append("  [-h | --help] Prints this help and usage message\n")
    usage.append("  [-c | --svn-co] Checkout the source-code from svn\n")
    usage.append("  [-u | --svn-update] Update the source-code from svn\n")
    usage.append("  [-b | --build-product-package] build package by maven\n")
    usage.append("  [-s | --upload package] upload package by SCP commond\n")
    message = string.join(usage)
    print message

# Checkout the newarkstg repo via svn function.
def svn_co():

    print ('svn co.')
    print 'Logs output to the '+log_path+'/svn_co.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_co.log")
    
    os.system('mkdir -p '+src_target_path+' 2>/dev/null >/dev/null')

    os.system('svn co --username '+svn_username+' --password '+svn_password+' '+svn_url+' '+src_target_path+' > '+log_path+'/svn_co.log')

    print ('svn_co finished!')

# Update the newarkstg repo via svn function.
def svn_update():

    print ('svn update.')
    print 'Logs output to the '+log_path+'/svn_update.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/svn_update.log")
    os.system('mkdir -p '+src_target_path+' 2>/dev/null >/dev/null')

    os.system('svn update --username '+svn_username+' --password '+svn_password+' '+src_target_path+' > '+log_path+'/svn_update.log')

    print ('svn_update finished!')
    
# mvn build & autoconfig function.
def mvn_build():

    print ('mvn_build.')
    print 'Logs output to the '+log_path+'/mvn_build.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/mvn_build.log")
    os.chdir(src_target_path)
    os.system('mvn clean install -DskipTests autoconf:autoconf -DuserProp='+antx_prop_path +' > ../'+log_path+'/mvn_build.log')

    print ('mvn_build finished!')
    
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

# upload_product function.
def upload_product():

    print ('upload_product')
    print 'Logs output to the '+log_path+'/upload_product.log'

    os.system('mkdir -p '+log_path+' 2>/dev/null >/dev/null')
    os.system("echo '' > "+log_path+"/upload_product.log")
    
    remote_shell = RemoteShell(remote_ip,remote_usr,remote_pwd)
    localfile = src_target_path+'/target/'+app_name+'.tar.gz'
    filename_suffix = datetime.datetime.now().strftime('%y%m%d%H%M%S');
    dest_file = remote_target_path+'/'+app_name+'.tgz.'+filename_suffix
    remote_shell.put(localfile, dest_file)

    print ('upload_product finished!')

# The entrance of program.
if __name__=='__main__':
    main(sys.argv[1:])