from pydantic import BaseModel, Field, model_validator
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

    @model_validator(mode='before')
    def validate_reasonable_values(cls, values):
        """進行欄位範圍檢查"""
        side_id = values.get('side_id')
        stage = values.get('stage')
        cal = values.get('CAL')
        trl = values.get('TRL')
        # 檢查 side_id 是否為有效整數
        if side_id is not None and not isinstance(side_id, int):
            raise ValueError("side_id must be an integer")
        # 檢查 stage 是否是有效的整數或字串
        if isinstance(stage, float):
            raise ValueError("stage must be an integer or a valid string ('i', 'ii', 'iii')")
        # 檢查 CAL 和 TRL 使用邏輯運算符
        if (cal is not None and cal > 15) or (trl is not None and trl > 25):
            raise ValueError(f"{'CAL' if cal is not None and cal > 15 else 'TRL'} must be less than or equal to {'15' if cal is not None else '25'}")
        return values

class Measurements(BaseModel):
    teeth_id: int
    pair_measurements: List[DentalMeasurements]
    teeth_center: Tuple[int, int]
    
class InferenceResponse(BaseModel):
    request_id: int
    measurements: List[Measurements]
    message: str

