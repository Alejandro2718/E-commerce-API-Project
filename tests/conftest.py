import sqlite3
import sys
from pathlib import Path

import pytest

sys.path.insert(0, str(Path(__file__).resolve().parent.parent))

from database import create_schema


@pytest.fixture
def db():
	conn = sqlite3.connect(":memory:")
	conn.row_factory = sqlite3.Row
	create_schema(conn)
	try:
		yield conn
	finally:
		conn.close()
