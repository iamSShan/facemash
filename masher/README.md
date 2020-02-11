To run it set some environment variable:
On linux and mac:
export FLASK_APP=mash.py

On Windows:
set FLASK_APP=mash.py


or run using python mash.py

Create a postgres DB of name mash_db and postgres user of name mash_user
Then 
ALTER USER mash_user PASSWORD 'root';

hit url:
/database/frequentare/