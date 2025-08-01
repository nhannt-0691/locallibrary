from enum import Enum
MAX_LENGTH_NAME = 200
MAX_LENGTH_AUTHOR_NAME = 100
MAX_LENGTH_ISBN = 13
MAX_LENGTH_SUMMARY = 1000
MAX_LENGTH_UNIQUE_ID = 20

class LoanStatus(Enum):
    MAINTENANCE = 'm'
    ON_LOAN = 'o'
    AVAILABLE = 'a'
    RESERVED = 'r'

DEFAULT_IMPRINT = 'DEFAULT_IMPRINT'

# catalog/constants.py

BOOKS_PER_PAGE = 10

DEFAULT_LOAN_PERIOD_WEEKS = {
    'default': 3,
    'max': 4
}
LOAN_STATUS_ON_LOAN = 'o'  

