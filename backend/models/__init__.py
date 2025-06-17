# Models package - Phase 1 (SQLAlchemy Core)
from .base import get_engine, get_metadata, create_all_tables
from .cv_models import cvs
from .chat_models import messages

__all__ = ["get_engine", "get_metadata", "create_all_tables", "cvs", "messages"]

# TODO: Phase 2 - Add ORM models imports:
# from .cv_models import CVFile, CVPersonalInfo, CVEmployment, etc.
# from .chat_models import Message
