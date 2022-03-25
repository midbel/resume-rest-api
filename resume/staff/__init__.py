from dataclasses import dataclass, field
from typing import List
import datetime

@dataclass
class CareerItem:
    id: int
    dtstart: datetime.date
    dtend: datetime.date
    title: str
    desc: str

@dataclass
class Career:
    id: int
    dtstart: datetime.date
    dtend: datetime.date
    title: str
    desc: str
    employer: str
    profile_id: int
    items: List[CareerItem] = field(default_factory=list)

@dataclass
class Language:
    id: int
    lang: str
    mother: bool
    desc: str
    level: int
    profile_id: int

@dataclass
class Achievement:
    id: int
    name: str
    desc: str
    web: str
    profile_id: int

@dataclass
class Interest:
    id: int
    name: str
    profile_id: int

@dataclass
class SoftSkill:
    id: int
    name: str
    profile_id: int

@dataclass
class HardSkill:
    id: int
    category: str
    name: str
    desc: str
    level: int
    seniority: int
    profile_id: int

@dataclass
class Education:
  id: int
  school: str
  degree: str
  dtstart: datetime.date
  dtend: datetime.date
  profile_id: int

@dataclass
class Profile:
    id: int
    first_name: str
    last_name: str
    phone: str
    email: str
    web: str
    position: str
    about: str
    careers: List[Career] = field(default_factory=list)
    softs: List[SoftSkill] = field(default_factory=list)
    hards: List[HardSkill] = field(default_factory=list)
    achievements: List[Achievement] = field(default_factory=list)
    languages: List[Language] = field(default_factory=list)
    educations: List[Education] = field(default_factory=list)
    interests: List[Interest] = field(default_factory=list)
