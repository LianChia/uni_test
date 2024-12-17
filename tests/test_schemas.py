# tests/test_schemas.py
import sys
import os
from typing import Any
from pydantic import ValidationError

sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))
from dental_measure.schemas import DentalMeasurements

test_values = {
    "valid_numbers": [0, 1, 2, 3, 10, 20.5],
    "invalid_numbers": [None, -1, "invalid", [], False],  # 確保這些無效值會被正確處理
    "valid_stages": [0, 1, 2, 3, "i", "ii", "iii"],
    "invalid_stages": ["x", 4, None, [], -1]  # 同樣確保無效值被正確處理
}


def test_dental_measurements():
    valid_data_list = [
        {"side_id": num, "CEJ": (1, 2), "ALC": (3, 4), "APEX": (5, 6), "CAL": 1.5, "TRL": 2.5, "ABLD": 3.5, "stage": stage}
        for num in test_values["valid_numbers"]
        for stage in test_values["valid_stages"]
    ]
    invalid_data_list = [
        {"side_id": num, "CEJ": (1, 2), "ALC": (3, 4), "APEX": (5, 6), "CAL": 1.5, "TRL": 2.5, "ABLD": 3.5, "stage": stage}
        for num in test_values["invalid_numbers"]
        for stage in test_values["invalid_stages"]
    ]

    # Valid data test
    for data in valid_data_list:
        try:
            measurement = DentalMeasurements(**data)
            assert measurement.side_id == data["side_id"]
            assert measurement.CEJ == data["CEJ"]
            assert measurement.stage in test_values["valid_stages"]
        except ValidationError as e:
            print(f"Validation error for valid data {data}: {e}")

    # Invalid data test
    for i, invalid_data in enumerate(invalid_data_list):
        try:
            DentalMeasurements(**invalid_data)
            assert False, f"Test {i} 應該引發 ValueError"
        except ValidationError as e:
            print(f"Test {i} validation failed: {e}")

def test_stage_values():
    for stage in test_values["valid_stages"]:
        data = {
            "side_id": 1, "CEJ": (1, 2), "ALC": (3, 4), "APEX": (5, 6), "CAL": 1.5, "TRL": 2.5, "ABLD": 3.5, "stage": stage
        }
        measurement = DentalMeasurements(**data)
        assert measurement.stage == stage

    for invalid_stage in test_values["invalid_stages"]:
        data = {
            "side_id": 1, "CEJ": (1, 2), "ALC": (3, 4), "APEX": (5, 6), "CAL": 1.5, "TRL": 2.5, "ABLD": 3.5, "stage": invalid_stage
        }
        try:
            DentalMeasurements(**data)
            assert False, f"stage={invalid_stage} 應該引發錯誤"
        except ValueError as e:
            print(f"test_stage_values: stage={invalid_stage} 失敗，錯誤信息: {e}")

def test_dental_measurements_serialization():
    for stage in test_values["valid_stages"]:
        data = {
            "side_id": 1, "CEJ": (1, 2), "ALC": (3, 4), "APEX": (5, 6), "CAL": 1.5, "TRL": 2.5, "ABLD": 3.5, "stage": stage
        }
        measurement = DentalMeasurements(**data)
        serialized = measurement.model_dump()
        assert serialized["side_id"] == 1
        assert serialized["CEJ"] == (1, 2)
        assert serialized["stage"] == stage
    print("test_dental_measurements_serialization: 成功")

# 執行所有測試
if __name__ == "__main__":
    test_dental_measurements()
    test_stage_values()
    test_dental_measurements_serialization()
