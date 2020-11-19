Metadata Repository (mdrepo)

A collection of tables that contain the metadata used for managing our process flows for data pipelines.

The package offers the Python class models of the tables and their corresponding operators used for accessing
data in the tables and inserting/updating the data.

The package requires at least two environment variables for the location of the encrypted password file and
the host for the database. The username for the database connection can also be set via an environment variable.
The name of the encrypted password file *must* be ".repo" without the double quotes.  It can be managed using the
pwutil.py CLI application.

Environment Variables
    * MDREPO_DB_PFILE = Required - the location of the encrypted password file
    * MDREPO_DB_HOST  = Required - host name or ip address for database
    * MDREPO_DB_USER  = Optional - name of the database user - defaults to "mdrepo"

Future Development
    + Utils module for creating a new, empty repository and updating to the latest version.
