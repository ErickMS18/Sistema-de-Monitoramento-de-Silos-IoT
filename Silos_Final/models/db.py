# run this in MySQL to initate the DB:
# DROP SCHEMA IF EXISTS `pjbl3db`;
# CREATE SCHEMA IF NOT EXISTS `pjbl3db`;

from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()

instance = "mysql+pymysql://root:PUC%401234@localhost:3306/pjbl3db"
# an @ symbol needs to be typed as %40

