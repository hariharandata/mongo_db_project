from pydantic import BaseModel

class DataModel(BaseModel):
    """
    Base class for the collection the data.
    """
    id: str
    name: str
    age: int
    place: str
