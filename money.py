from dataclasses import dataclass
from typing import Union, ClassVar
from decimal import Decimal #Removes floating point issues


# Money class, for storing money and printing it nicely
# Usage examples:
# money1 = Money(1234.56)  # Creates: $1,234.56
# money2 = Money(50)       # Creates: $50.00
# Will raise ValueError
# money3 = Money(100000)   # Error: Amount cannot exceed $99,999
# print(money) will print as $X,XXX.XX

@dataclass
class Money:
    """Money amount, max $99,999"""
    amount: Union[int, float]
    MAX_AMOUNT: ClassVar[int] = 99999

    def __post_init__(self):
        self.amount = Decimal(str(self.amount))
        if not 0 <= self.amount <= self.MAX_AMOUNT:
            raise ValueError(f"Amount must be between $0 and ${self.MAX_AMOUNT:,}")
        
    def __repr__(self) -> str:
        return f"${self.amount:,.2f}"
