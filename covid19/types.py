"""Type definitions"""

from enum import Enum
from typing import Dict, List, Union

Infections = Dict[str, List[Dict[str, Union[str, int]]]]


class InfectionStatus(Enum):
    """Types of events that are observed in the infection data"""
    CONFIRMED = "confirmed"
    DEATHS = "deaths"
    RECOVERED = "recovered"
