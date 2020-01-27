class FlaskSessionConf(object):
    def __init__(self, session_type, session_mongodb_db, session_mongodb_collect):
        self.SESSION_TYPE = session_type
        self.SESSION_MONGODB_DB = session_mongodb_db
        self.SESSION_MOGNODB_COLLECT = session_mongodb_collect