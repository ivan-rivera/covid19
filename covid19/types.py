"""Type definitions"""

from enum import Enum
from typing import Dict, List, Union, Optional

Infections = Dict[str, List[Dict[str, Union[str, int]]]]

HoverData = Optional[Dict[str, List[Dict[str, Union[int, str]]]]]


class InfectionStatus(Enum):
    """Types of events that are observed in the infection data"""
    CONFIRMED = "confirmed"
    DEATHS = "deaths"
    RECOVERED = "recovered"
