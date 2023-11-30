"""
Provide simple tools to help building SQL queries.
"""

from .filter import *
from .query import *

# short aliases to classes Filter and Query which are the only ones
# that will be needed to build SQL queries
f = Filter
q = Query
