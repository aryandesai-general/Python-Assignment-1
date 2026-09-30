"""Q5: Object-oriented bank settlement with atomic batch rollback."""
import sys


class BankError(Exception):
    """Base class for bank operation errors."""


class AccountNotFoundError(BankError):
    pass


class InvalidAmountError(BankError):
    pass


class InsufficientFundsError(BankError):
    pass


class Account:
    def __init__(self, account_id, balance=0):
        if balance < 0:
            raise InvalidAmountError("Opening balance cannot be negative")
        self.account_id = account_id
        self._balance = int(balance)

    @property
    def balance(self):
        return self._balance

    def _set_balance(self, value):
        self._balance = value


class Transaction:
    def __init__(self, operation, details):
        self.operation = operation
        self.details = details


class Bank:
    def __init__(self):
        self.accounts = {}
        self.history = []
        self.batch_snapshot = None
        self.batch_history_start = 0
        self.batch_number = 0
        self.failed_batches = []
        self.skip_failed_batch = False

    def account(self, account_id):
        if account_id not in self.accounts:
            raise AccountNotFoundError(f"Unknown account: {account_id}")
        return self.accounts[account_id]

    @staticmethod
    def check_amount(amount):
        if amount <= 0:
            raise InvalidAmountError("Amount must be positive")

    def deposit(self, account_id, amount):
        self.check_amount(amount)
        account = self.account(account_id)
        account._set_balance(account.balance + amount)
        self.history.append(Transaction("DEPOSIT", (account_id, amount)))

    def withdraw(self, account_id, amount):
        self.check_amount(amount)
        account = self.account(account_id)
        if account.balance < amount:
            raise InsufficientFundsError("Insufficient funds")
        account._set_balance(account.balance - amount)
        self.history.append(Transaction("WITHDRAW", (account_id, amount)))

    def transfer(self, source, destination, amount):
        self.check_amount(amount)
        if source == destination:
            raise BankError("Source and destination must differ")
        source_account = self.account(source)
        destination_account = self.account(destination)
        if source_account.balance < amount:
            raise InsufficientFundsError("Insufficient funds")
        source_account._set_balance(source_account.balance - amount)
        destination_account._set_balance(destination_account.balance + amount)
        self.history.append(Transaction("TRANSFER", (source, destination, amount)))

    def begin_batch(self):
        if self.batch_snapshot is not None:
            raise BankError("Nested batches are not supported")
        self.batch_number += 1
        self.batch_snapshot = {key: account.balance for key, account in self.accounts.items()}
        self.batch_history_start = len(self.history)

    def end_batch(self):
        if self.batch_snapshot is None:
            raise BankError("No batch is active")
        self.batch_snapshot = None

    def rollback_batch(self):
        for key, balance in self.batch_snapshot.items():
            self.accounts[key]._set_balance(balance)
        del self.history[self.batch_history_start:]
        self.failed_batches.append(self.batch_number)
        self.batch_snapshot = None
        self.skip_failed_batch = True


def main():
    lines = iter(sys.stdin)
    try:
        count = int(next(lines).strip())
        bank = Bank()
        for _ in range(count):
            account_id, balance = next(lines).split()
            bank.accounts[account_id] = Account(account_id, int(balance))
        operation_count = int(next(lines).strip())
    except (ValueError, StopIteration):
        print("Invalid input.")
        return

    for _ in range(operation_count):
        try:
            parts = next(lines).split()
        except StopIteration:
            print("Invalid input.")
            return
        if not parts:
            continue
        command = parts[0].upper()
        # Once a batch fails, ignore its remaining operations through BATCH_END.
        if bank.skip_failed_batch:
            if command == "BATCH_END":
                bank.skip_failed_batch = False
            continue
        try:
            if command == "BATCH_BEGIN":
                bank.begin_batch()
            elif command == "BATCH_END":
                bank.end_batch()
            elif command == "DEPOSIT" and len(parts) == 3:
                bank.deposit(parts[1], int(parts[2]))
            elif command == "WITHDRAW" and len(parts) == 3:
                bank.withdraw(parts[1], int(parts[2]))
            elif command == "TRANSFER" and len(parts) == 4:
                bank.transfer(parts[1], parts[2], int(parts[3]))
            else:
                raise BankError("Invalid operation")
        except (BankError, ValueError):
            if bank.batch_snapshot is not None:
                bank.rollback_batch()
            else:
                print("ERROR", " ".join(parts))

    for failed in bank.failed_batches:
        print(f"FAILED {failed}")
    for account_id in sorted(bank.accounts):
        print(account_id, bank.accounts[account_id].balance)


if __name__ == "__main__":
    main()
