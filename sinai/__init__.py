"""Sinai is a library to help you monitor everything."""

VERSION = "0.0.3"


from abc import ABC

from sinai.types import MonitorInstance

class BaseView(ABC):
    def __init__(self, monitor: MonitorInstance):
        self.monitor = monitor
