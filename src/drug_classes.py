"""
defines class to sort drug attribute and pass to sql database
"""

import inspect

class Drug():
    def __init__(self, name, generic_name):
        self.name = name
        self.generic_name = generic_name

class SideEffect():
    def __init__(self, name, description):
        self.name = name
        self.description = description

class MedicalCondition():
    def __init__(self, name, description):
        self.name = name
        self.description = description

def get_class_attributes(cls):
    return list(inspect.signature(cls).parameters)
