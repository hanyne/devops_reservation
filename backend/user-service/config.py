class Config:
    DEBUG = False
    SECRET_KEY = 'your-secret-key-here'
    SQLALCHEMY_DATABASE_URI = 'postgresql://postgres:@db:5432/reservation_db'
    SQLALCHEMY_TRACK_MODIFICATIONS = False
    KAFKA_BOOTSTRAP_SERVERS = 'kafka:9092'