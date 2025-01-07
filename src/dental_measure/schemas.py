from pydantic import BaseModel, field_validator
from typing import List, Tuple, Any
from fastapi import FastAPI, HTTPException
from typing import Annotated
from typing import Union, Tuple
from pydantic import BaseModel, Field
from typing_extensions import Literal
import ast

    
class DentalMeasurements(BaseModel):
    side_id: int = Field(..., ge=0, description="Side ID must be a non-negative integer")
    CEJ: Tuple[int, int]
    ALC: Tuple[int, int]
    APEX: Tuple[int, int]
    CAL: float = Field(..., ge=0, description="CAL must be a non-negative float")
    TRL: float = Field(..., ge=0, description="TRL must be a non-negative float")
    ABLD: float = Field(..., ge=0, description="ABLD must be a non-negative float")
    stage: Union[Literal[0, 1, 2, 3, "i", "ii", "iii"]]
    
    @field_validator("TRL", "CAL")
    def validate_reasonable_values(cls, v, field):
        if (field.name == "TRL" and v > 25) or (field.name == "CAL" and v > 15):
            raise ValueError(f"Value too large for {field.name}")
        return v

class Measurements(BaseModel):
    teeth_id: int
    pair_measurements: List[DentalMeasurements]
    teeth_center: Tuple[int, int]
    
class InferenceResponse(BaseModel):
    request_id: int
    measurements: List[Measurements]
    message: str

