"""
Chat/Message related database models
Keeping existing SQLAlchemy Core tables for Phase 1 refactoring
"""

import datetime as dt
import sqlalchemy as sa
from .base import meta

# ---- Chat/Message Tables --------------------------------------------------
messages = sa.Table(
    "messages",
    meta,
    sa.Column("id", sa.Integer, primary_key=True),
    sa.Column("role", sa.String(10)),
    sa.Column("content", sa.Text),
    sa.Column("ts", sa.DateTime, default=dt.datetime.utcnow),
)
