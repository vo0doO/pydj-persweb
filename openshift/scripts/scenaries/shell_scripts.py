import logging
import os
import sys

token = os.getenv("OPENSHIFT_TOKEN")
user = os.getenv("OPENSHIFT_USER")

def sh(command):
    try:
        os.system(f"{command}")
        logger.info(f"Success: {command}.")
        return True
    except Exception as exc:
        logger.error("Error: ", exc.args)
        return False

def run_sh(cmds):
    c = cmds.copy()
    cmds.reverse()
    for cmd in cmds:
        time.sleep(1)
        return logger.info(f"Success {str(sh(cmds.pop())).split(',')}")


if __name__ == "__main__":
    if token or user is None:
        print("NEED EXPORT SECRETS TO ENVIROMENT !!!")
        cmd_run(cmds=[command for command in sys.argv[1:]])
