import os
import logging
import sys, getopt
import time
import uuid
import platform
import subprocess
import shutil
import fileinput
import math

logger = logging.getLogger('delete_stack')

LOG_LEVEL = os.getenv('LOG_LEVEL', 'INFO').upper()

class Main():

    prefix = 'demo'
    microk8s = False
    kubectl_string = ''
    delete_all = True

    @staticmethod
    def get_microk8s():
        try:
            subprocess.call(["microk8s", "kubectl", "version"])
            Main.microk8s = True
            Main.kubectl_string = "microk8s kubectl "
        except:
            Main.microk8s = False    
            Main.kubectl_string = "kubectl "    

    @staticmethod
    def log_level(level):
        logging.basicConfig(level=getattr(logging, level))

    @staticmethod
    def stop_jmeter_jobs():
        try:
            if Main.delete_all:
                os.system(Main.kubectl_string + "delete namespace jmeterjobs")
            else:
                os.system(Main.kubectl_string + "-n jmeterjobs delete --ignore-not-found jobs -l jobgroup=" + Main.prefix + "-jmeter")
                os.system(Main.kubectl_string + "-n jmeterjobs delete --ignore-not-found secret jmeterconf")
        except Exception as e:
            logger.error(e)
            exit(1)

    @staticmethod
    def main(argv):
        help_string = 'To delete a job by prefix:\n\nsudo python3 delete_stack.py <-p job_prefix>\n\nWhen running with no prefix specified, all current jmeter jogs will be deleted'
        try:
            opts, args = getopt.getopt(argv,"hp:",["help=","prefix="])
        except getopt.GetoptError:
            print (help_string)
            sys.exit(2)
        for opt, arg in opts:
            if opt in ('-h','--help'):
                print (help_string)
                sys.exit()
            elif opt in ('-p', '--prefix'):
                Main.prefix = arg
                Main.delete_all = False

        Main.log_level(LOG_LEVEL)
        logger.info(Main.prefix)
        Main.get_microk8s()
        Main.stop_jmeter_jobs()

if __name__ == "__main__":
    Main.main(sys.argv[1:])