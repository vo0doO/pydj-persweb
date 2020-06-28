import os

os.getenv(PGADMIN_DEFAULT_EMAIL, "exenoobe@gmail.com")
os.getenv(PGADMIN_DEFAULT_PASSWORD, "yousupersecretpassword")

get_postgres = [
    "source venv/bin/activate",
    "oc new-project myproject",
    "oc new-app postgresql-ephemeral --name database --param DATABASE_SERVICE_NAME=database --param POSTGRESQL_DATABASE=postgres --param POSTGRESQL_USER=postgres --param POSTGRESQL_PASSWORD=supersecret",
    "oc rollout status dc/database",
    "oc get pods --selector app=database",
    "POD=`oc get pods --selector app=database -o custom-columns=name:.metadata.name --no-headers`; echo $POD",
    "oc rsh $POD",
    "ps x"
    ]
