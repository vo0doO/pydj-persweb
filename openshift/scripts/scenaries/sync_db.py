import os
import sys

vector = sys.argv[1]
pod = sys.argv[2]
print(f"{vector} {pod}")
if vector == "in":
    os.system(f"oc rsync {pod}:/opt/app-root/src/db.sqlite3 .")
elif vector == "out":
    os.system(f"oc rsync . {pod}:/opt/app-root/src --exclude=* --include=db.sqlite3 --no-perms")
else:
    print("Usage ./sync_db vector pod")
