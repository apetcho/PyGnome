'''
environment module
'''
from environment import Environment, Water, WaterSchema
from tide import Tide, TideSchema
from wind import Wind, WindSchema, constant_wind

__all__ = [Environment,
           Water,
           WaterSchema,
           Tide,
           TideSchema,
           Wind,
           WindSchema,
           constant_wind]

'''
Constants are mostly used internally. They are all documented here to keep them
in one place. The 'units' serve as documentation ** do not mess with them **.
There is no unit conversion when using these constants - they are used as is
in the code, implicitly assuming the units are SI and untouched.
'''
units = {'gas_constant': 'J/(K mol)',
         'pressure': 'Pa',
         'acceleration': 'm/s^2'}
constants = {'gas_constant': 8.314,
             'atmos_pressure': 101325.0,
             'gravity': 9.80665,
             }

