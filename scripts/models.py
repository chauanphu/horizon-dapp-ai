from datetime import datetime
from enum import Enum

from pydantic import BaseModel

class EntityType(Enum):
    CRYPTOCURRENCY = "Cryptocurrency"
    ORGANIZATION = "Organization"
    PERSON = "Person"
    EVENT = "Event"
    LOCATION = "Location"
    METRIC = "Metric"

class Entity(BaseModel):
    name: str
    type: EntityType
    attributes: dict = {}

class RelationType(Enum):
    CAUSAL = "Mentions"
    ASSOCIATIVE = "About"
    TEMPORAL = "Happened After"
    SENTIMENT_BASED = "Sentiment-based"

class Relationship(BaseModel):
    details: str
    type: RelationType

class KnowledgeGraph(BaseModel):
    src_entity: Entity
    dst_entity: Entity
    description: str
    relationship: Relationship
    time: datetime
    metadata: dict = {}