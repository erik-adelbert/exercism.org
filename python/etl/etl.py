"""
etl.py -- 
"""


def transform(legacy_data):
    """
    A toy transformation
    """
    return {c.lower(): k for k, cars in legacy_data.items() for c in cars}
