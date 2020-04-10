"""Type definitions"""

from abc import ABC
from dataclasses import dataclass
from datetime import datetime
from enum import Enum
from typing import Dict, List, Union, Optional, TypeVar, Generic, Callable

import plotly.graph_objects as go

Infections = Dict[str, List[Dict[str, Union[str, int]]]]
HoverData = Optional[Dict[str, List[Dict[str, Union[int, str]]]]]

T = TypeVar("T")


class InfectionStatus(Enum):
    """Types of events that are observed in the infection data"""
    CONFIRMED = "confirmed"
    DEATHS = "deaths"


@dataclass
class __SummaryStat(ABC, Generic[T]):

    title: str
    value: T

    def __post_init__(self):
        self.id_str = self.title.replace(" ", "_").lower()


@dataclass
class SummaryDate(__SummaryStat[datetime]):
    def __post_init__(self):
        super().__post_init__()
        self.value_str: str = self.value.strftime("%Y-%m-%d")


@dataclass
class SummaryCount(__SummaryStat[int]):
    def __post_init__(self):
        super().__post_init__()
        self.value_str: str = f"{self.value:,}"


@dataclass
class SummaryPercentage(__SummaryStat[float]):
    def __post_init__(self):
        super().__post_init__()
        self.value_str: str = f"{self.value:.2%}"


@dataclass
class Summary:
    last_update: SummaryDate
    total_cases: SummaryCount
    total_deaths: SummaryCount
    mortality_rate: SummaryPercentage
    global_growth: SummaryPercentage


@dataclass
class FigureInstance:
    id_str: str
    figure: go.Figure
    reset: Callable[[go.Figure], go.Figure]
    highlight: Callable[[go.Figure, str], go.Figure]
