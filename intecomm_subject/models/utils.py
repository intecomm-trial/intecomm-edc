from __future__ import annotations

import re
from dataclasses import dataclass, field
from datetime import timedelta


@dataclass
class Duration:
    duration_str: str
    hrs: int = field(default=0)
    mins: int = field(default=0)
    hm_pattern: str = field(default=r"^([0-9]{1,3}h([0-5]?[0-9]m))$", init=False)
    h_pattern: str = field(default=r"^([0-9]{1,3}h)$", init=False)
    m_pattern: str = field(default=r"^([0-5]?[0-9]m)$", init=False)
    timedelta: timedelta = field(default=timedelta(hours=0, minutes=0), init=False)

    def __post_init__(self):
        if re.match(self.hm_pattern, self.duration_str):
            h, m = self.duration_str.split("h")
            self.hrs = int(h)
            self.mins = int(m.split("m")[0])
        elif re.match(self.h_pattern, self.duration_str):
            h = self.duration_str.split("h")[0]
            self.hrs = int(h)
        elif re.match(self.m_pattern, self.duration_str):
            m = self.duration_str.split("m")[0]
            self.mins = int(m)
        else:
            raise ValueError()
        self.timedelta = timedelta(hours=self.hrs, minutes=self.mins)
