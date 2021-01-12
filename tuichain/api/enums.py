from enum import Enum

class LoanState(Enum):
    """Possible States of a Loan."""

    PENDING = 0
    """Waiting for approval."""

    CREATING = 1
    """After approval, waiting for Loan to be created by the BlockChain Component."""

    APPROVED = 2
    """After creation, it becomes approved. All states can be collected on the BlockChain Component."""

    WITHDRAWN = 3
    """As been withdrawn by the user."""
    
    REJECTED = 4
    """Has not been approved by an Admin."""

    def __str__(self):
        return self.name
