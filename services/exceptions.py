class BankingError(Exception):
    """Base class for banking-related errors."""
    pass


class DatabaseConnectionError(BankingError):
    pass


class UserNotFoundError(BankingError):
    pass


class AccountNotFoundError(BankingError):
    pass


class InsufficientFundsError(BankingError):
    pass


class InvalidAmountError(BankingError):
    pass

class DuplicateUserError(BankingError):
    pass

