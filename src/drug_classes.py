"""
defines class to sort drug attribute and pass to sql database
"""

from dataclasses import dataclass
import inspect

@dataclass
class Drug():
    name: str
    generic_name: str

@dataclass
class SideEffect():
    name: str
    description: str

@dataclass
class MedicalCondition():
    name: str
    description: str

def get_class_attributes(cls):
    return list(inspect.signature(cls).parameters)
