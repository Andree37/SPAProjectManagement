"""
 Implements a simple database of users.

"""
from datetime import datetime, timedelta

from flask import Flask
from flask_admin import Admin
from flask_admin.contrib.sqla import ModelView
from flask_login import UserMixin
from datetime import datetime
from flask_sqlalchemy import SQLAlchemy
from sqlalchemy import Integer, String, Column, DateTime, ForeignKey, Boolean
from sqlalchemy.orm import relationship

