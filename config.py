from filoModules.Models.Config.MongoConfig import MongoConfig
from filoModules.Models.Config.EmailConf import EmailConf
from filoModules.Models.Config.AddrConf import AddrConf
from filoModules.Models.Config.FlaskSessionConf import FlaskSessionConf
from filoModules.Models.Config.FlaskConf import FlaskConf


DEBUG_HOSTNAME = "test.findlock.site"
PROD_HOSTNAME = "findlock.site"
ENV = "DEBUG"
VERSION = "eind1.0"
MONGO_CONFIG = MongoConfig(AddrConf("localhost", "27017"))
EMAIL_CONFIG = EmailConf(AddrConf("smtp.gmail.com", 465), "example@gmail.com", "examplepassword")
SESSION_CONFIG = FlaskSessionConf("mongodb", "filo", "sessions")
SSL_CONTEXT = ('cert/cert.pem', 'cert/key.pem')
LOG_FILE = "filoLogs.log"

FLASK_ADDRESS = AddrConf("0.0.0.0", "4899")

GOOGLE_CLIENT_ID = "xxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxxx.apps.googleusercontent.com"
APP_SECRET_KEY = os.urandom(8)
SECURITY_PASSWORD_SALT = os.urandom(8)

def is_prod() -> bool:
    return ENV == "PROD"
def get_version() -> str:
    return f"{VERSION}.{ENV}"
def get_mongo_config() -> MongoConfig:
    return MONGO_CONFIG
def get_email_config() -> EmailConf:
    return EMAIL_CONFIG
def get_flask_addr() -> AddrConf:
    return FLASK_ADDRESS
def get_gcid() -> str:
    return GOOGLE_CLIENT_ID
def get_app_secret() -> bytes:
    return APP_SECRET_KEY
def get_security_password_salt() -> bytes:
    return SECURITY_PASSWORD_SALT
def get_flask_conf_obj() -> FlaskConf:
    flask_config = FlaskConf()
    flask_config.add_to_config(SESSION_CONFIG)
    return flask_config
def get_ssl_context():
    return SSL_CONTEXT
def get_hostname() -> str:
    if is_prod():
        return PROD_HOSTNAME
    return DEBUG_HOSTNAME
def get_log_file_name() -> str:
    return LOG_FILE