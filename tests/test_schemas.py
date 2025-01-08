import logging
import pytest
import numpy as np
from pydantic import ValidationError
import sys
import os
sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.dental_measure.schemas import DentalMeasurements

# 初始化日誌
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# 測試資料
TEST_VALUES = {
    "valid_numbers": [0, 1, 2, 3, 10, sys.maxsize],
    "invalid_numbers": [None, -1, "invalid", [], False, 1.5, -1.5, float('inf')],
    "valid_stages": [0, 1, 2, 3, "i", "ii", "iii"],
    "invalid_stages": ["x", 4, None, [], -1, "iiiiiiii", 1.0],
    "valid_tuples": [(0, 0), (1, 2), (sys.maxsize, sys.maxsize)],
    "invalid_tuples": [(1.5, "a"), (1,), (1, 2, 3), [], None]
}

def generate_test_data(valid: bool) -> list[dict]:
    """根據測試狀態生成測試資料。"""
    numbers = TEST_VALUES["valid_numbers" if valid else "invalid_numbers"]
    stages = TEST_VALUES["valid_stages" if valid else "invalid_stages"]
    # 使用 map() 來生成每個數據項，將其轉換為字典形式
    data_list = map(
        lambda num: [
            {
                "side_id": num,
                "CEJ": (1, 2),
                "ALC": (3, 4),
                "APEX": (5, 6),
                "CAL": 1.5,
                "TRL": 2.5,
                "ABLD": 3.5,
                "stage": stage
            }
            for stage in stages
        ],
        numbers
    )
    # 使用 filter() 來過濾掉不符合要求的數據
    filtered_data = filter(lambda x: x >= 0, numbers)
    # 扁平化資料，使其不再是嵌套的列表，而是直接的字典
    flattened_data = [item for sublist in data_list for item in sublist]
    return flattened_data

def run_test_case(data: dict, expected_valid: bool, index: int):
    """通用測試函數，用於驗證單一案例。"""
    try:
        measurement = DentalMeasurements(**data)
        if not expected_valid:
            pytest.fail(f"Test {index} should have failed: {data}")
        logger.info(f"Test {index} passed for valid data: {data}")
        return  # 成功時提前返回
    except ValidationError as e:
        if expected_valid:
            pytest.fail(f"Validation failed for valid data {data}: {e}")
        logger.info(f"Test {index} failed as expected: {e}")
        return  # 失敗時提前返回

@pytest.mark.parametrize("data,expected_valid", [
    ({"side_id": 1, "CEJ": (1, 2), "ALC": (3, 4), "APEX": (5, 6), "CAL": 1.5, "TRL": 2.5, "ABLD": 3.5, "stage": "i"}, True),
    ({"side_id": -1, "CEJ": (1, 2), "ALC": (3, 4), "APEX": (5, 6), "CAL": 1.5, "TRL": 2.5, "ABLD": 3.5, "stage": 0}, False),
])
def test_validate_measurement(data, expected_valid):
    """驗證單一測量的測試。"""
    run_test_case(data, expected_valid, index=0)

def test_dental_measurements():
    """測試有效與無效的 DentalMeasurements 資料。"""
    logger.info("Testing dental_measurements function...")
    for valid in [True, False]:
        data_list = generate_test_data(valid=valid)
        for i, data in enumerate(data_list):
            run_test_case(data, valid, i)
    logger.info("dental_measurements tests passed!")

def test_stage_values():
    """測試 stage 欄位的驗證。"""
    logger.info("Testing stage values...")

    def create_data(stage):
        return {
            "side_id": 1,
            "CEJ": (1, 2),
            "ALC": (3, 4),
            "APEX": (5, 6),
            "CAL": 1.5,
            "TRL": 2.5,
            "ABLD": 3.5,
            "stage": stage
        }

    for valid, key in [(True, "valid_stages"), (False, "invalid_stages")]:
        for stage in TEST_VALUES[key]:
            run_test_case(create_data(stage), valid, index=0)

    logger.info("Stage values tests passed!")

def test_serialization():
    """測試 DentalMeasurements 的序列化功能。"""
    logger.info("Testing serialization...")

    for stage in TEST_VALUES["valid_stages"]:
        data = {
            "side_id": 1,
            "CEJ": (1, 2),
            "ALC": (3, 4),
            "APEX": (5, 6),
            "CAL": 1.5,
            "TRL": 2.5,
            "ABLD": 3.5,
            "stage": stage
        }
        measurement = DentalMeasurements(**data)
        serialized = measurement.model_dump()
        if serialized != data:
            pytest.fail(f"Serialization mismatch: {serialized} != {data}")
    
    logger.info("Serialization tests passed!")

def test_boundary_conditions():
    """測試邊界條件。"""
    logger.info("Testing boundary conditions...")
    boundary_data = [
        {"side_id": 0, "CEJ": (0, 0), "ALC": (0, 0), "APEX": (0, 0), "CAL": 0.0, "TRL": 0.0, "ABLD": 0.0, "stage": 0},
        {"side_id": 1, "CEJ": (1, 1), "ALC": (1, 1), "APEX": (1, 1), "CAL": 1.0, "TRL": 1.0, "ABLD": 1.0, "stage": "i"},
        {"side_id": 10, "CEJ": (10, 10), "ALC": (10, 10), "APEX": (10, 10), "CAL": 10.0, "TRL": 10.0, "ABLD": 10.0, "stage": "iii"}
    ]
    for i, data in enumerate(boundary_data):
        run_test_case(data, True, i)
    logger.info("Boundary condition tests passed!")

def test_exception_handling():
    """測試例外處理。"""
    logger.info("Testing exception handling...")
    exception_data = [
        {"side_id": "invalid", "CEJ": (1, 2), "ALC": (3, 4), "APEX": (5, 6), "CAL": 1.5, "TRL": 2.5, "ABLD": 3.5, "stage": 0},
        {"side_id": 1, "CEJ": "invalid", "ALC": (3, 4), "APEX": (5, 6), "CAL": 1.5, "TRL": 2.5, "ABLD": 3.5, "stage": 0},
    ]
    for i, data in enumerate(exception_data):
        run_test_case(data, False, i)
    logger.info("Exception handling tests passed!")

if __name__ == "__main__":
    logger.info("Starting all tests...")
    test_dental_measurements()
    test_stage_values()
    test_serialization()
    test_boundary_conditions()
    test_exception_handling()
    logger.info("All tests completed!")