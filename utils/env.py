import os

# credenciales local
db_host = os.environ.get('MOMOKO_TEST_HOST', 'localhost')
db_port = os.environ.get('MOMOKO_TEST_PORT', 5432)
db_database = os.environ.get('MOMOKO_TEST_DB', 'basedb')
db_user = os.environ.get('MOMOKO_TEST_USER', 'development')
db_password = os.environ.get('MOMOKO_TEST_PASSWORD', '12345678')

# enable_hstore = True if os.environ.get('MOMOKO_TEST_HSTORE', False) == '1' else False

dsn_dev = 'dbname=%s user=%s password=%s host=%s port=%s' % ( \
    db_database, db_user, db_password, db_host, db_port)

# credenciales heroku db
db_host = os.environ.get('MOMOKO_TEST_HOST', 'ec2-54-227-255-240.compute-1.amazonaws.com')
db_port = os.environ.get('MOMOKO_TEST_PORT', 5432)
db_database = os.environ.get('MOMOKO_TEST_DB', 'd3gfgcvud4enli')
db_user = os.environ.get('MOMOKO_TEST_USER', 'hxrysbuozjzdqb')
db_password = os.environ.get('MOMOKO_TEST_PASSWORD', 'hDNih6CmgMuaoUsvaeX8KwBigy')

dsn_prd = 'dbname=%s user=%s password=%s host=%s port=%s' % ( \
    db_database, db_user, db_password, db_host, db_port)

http_port = 8080
