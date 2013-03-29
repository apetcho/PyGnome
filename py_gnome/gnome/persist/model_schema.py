'''
Created on Mar 4, 2013
'''
from datetime import timedelta

from colander import (
    SchemaNode,
    MappingSchema,
    Bool,
    Float,
    Range,
    TupleSchema,
    Int,
    String,
    SequenceSchema,
    drop
    )

import gnome
from gnome.persist import validators, extend_colander, base_schema


class ArrayTypeShape(TupleSchema):
     len_ = SchemaNode(Int())

class ArrayType(MappingSchema):
     shape = ArrayTypeShape()
     dtype = SchemaNode( String() )
     #initial_value = SchemaNode( String() )    # Figure out what this is - tuple?
    
class AllArrayTypes(SequenceSchema):
    name = SchemaNode( String() )
    value = ArrayType()
    
    
class SpillContainerPair(MappingSchema):
    certain_spills = base_schema.OrderedCollection()
    uncertain_spills = base_schema.OrderedCollection(missing=drop)  # only present if uncertainty is on

class MapBounds(SequenceSchema):
    map_bounds = base_schema.LongLat()

class Map(base_schema.Id, MappingSchema):
    map_bounds = MapBounds(missing=drop)
    filename = SchemaNode(String(), missing=drop)
    refloat_halflife = SchemaNode( Float(), missing=drop)

class Model(base_schema.Id, MappingSchema):
    time_step = SchemaNode( Float()) 
    start_time= SchemaNode(extend_colander.LocalDateTime(), validator=validators.convertible_to_seconds)
    duration = SchemaNode(extend_colander.TimeDelta() )   # put a constraint for max duration?
    movers = base_schema.OrderedCollection()
    environment = base_schema.OrderedCollection()
    uncertain = SchemaNode( Bool() )
    spills = SpillContainerPair()
    map = Map()