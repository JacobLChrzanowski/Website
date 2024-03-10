# initializes tables  in a database
# !! Destructive !!
# Pre-loads a site with data
psql --host localhost --port 5432 --username postgres --echo-all -f scripts/postgres/db_init.sql

