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
    """Represents a monetary amount with a maximum limit of $99,999"""
    amount: Union[int, float]
    MAX_AMOUNT: ClassVar[int] = 99999

    def __post_init__(self):
        if not isinstance(self.amount, Decimal):
            self.amount = Decimal(str(self.amount))  
        if self.amount > self.MAX_AMOUNT:
            raise ValueError(f"Amount cannot exceed ${self.MAX_AMOUNT:,}")
        if self.amount < 0:
            raise ValueError("Amount cannot be negative")
        
    def __repr__(self) -> str:
        return f"${self.amount:,.2f}"
