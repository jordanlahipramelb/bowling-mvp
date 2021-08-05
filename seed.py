"""Seed file to create tables."""

from models import db
from app import app

db.drop_all()
db.create_all()
