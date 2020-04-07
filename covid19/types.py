"""Type definitions"""

from dataclasses import dataclass
from enum import Enum
from typing import Dict, List, Union, Optional

import plotly.graph_objects as go

Infections = Dict[str, List[Dict[str, Union[str, int]]]]

HoverData = Optional[Dict[str, List[Dict[str, Union[int, str]]]]]


@dataclass
class Plot:
    """Plot collection"""
    curve: go.Figure
    trend: go.Figure
    bars: go.Figure
    map: go.Figure


class InfectionStatus(Enum):
    """Types of events that are observed in the infection data"""
    CONFIRMED = "confirmed"
    DEATHS = "deaths"
    RECOVERED = "recovered"
