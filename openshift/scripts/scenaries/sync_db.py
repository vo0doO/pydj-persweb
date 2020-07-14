import os
import sys
import time

time = time.asctime().replace(" ", "-")
pod = sys.argv[1]
print(f" {pod}")

os.system(f"cp /home/vo0/projects/blog-osh/pydj-persweb/db.sqlite3 /home/vo0/projects/blog-osh/db.sqlite3[{time}]")
print("backup complete")
time.sleep(1)
os.system(f"oc rsync . {pod}:/opt/app-root/src --exclude=* --include=db.sqlite3 --no-perms")
print("sync complete")