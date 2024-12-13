import sys
import os

# 將 src 目錄添加到系統路徑，以便可以進行絕對導入
sys.path.insert(0, os.path.abspath(os.path.join(os.path.dirname(__file__), '../src')))

# 導入所需的類
from dental_measure.schemas import DentalMeasurements, Measurements, InferenceResponse

def test_dental_measurements_valid():
    # 測試有效的牙科測量數據
    data = {
        "side_id": 1,
        "CEJ": (1, 2),
        "ALC": (3, 4),
        "APEX": (5, 6),
        "CAL": 1.5,
        "TRL": 2.5,
        "ABLD": 3.5,
        "stage": "initial"
    }
    measurement = DentalMeasurements(**data)  # 創建 DentalMeasurements 實例
    # 驗證每個屬性是否正確
    assert measurement.side_id == 1
    assert measurement.CEJ == (1, 2)
    assert measurement.ALC == (3, 4)
    assert measurement.APEX == (5, 6)
    assert measurement.CAL == 1.5
    assert measurement.TRL == 2.5
    assert measurement.ABLD == 3.5
    assert measurement.stage == "initial"
    print("test_dental_measurements_valid: 成功")

def test_measurements_valid():
    # 測試有效的測量數據
    dental_measurements = [
        {
            "side_id": 1,
            "CEJ": (1, 2),
            "ALC": (3, 4),
            "APEX": (5, 6),
            "CAL": 1.5,
            "TRL": 2.5,
            "ABLD": 3.5,
            "stage": "initial"
        }
    ]
    data = {
        "teeth_id": 1,
        "pair_measurements": [DentalMeasurements(**dm) for dm in dental_measurements],
        "teeth_center": (100, 200)
    }
    measurements = Measurements(**data)  # 創建 Measurements 實例
    # 驗證每個屬性是否正確
    assert measurements.teeth_id == 1
    assert len(measurements.pair_measurements) == 1
    assert measurements.teeth_center == (100, 200)
    print("test_measurements_valid: 成功")

def test_inference_response_valid():
    # 測試有效的推斷數據
    dental_measurements = [
        {
            "side_id": 1,
            "CEJ": (1, 2),
            "ALC": (3, 4),
            "APEX": (5, 6),
            "CAL": 1.5,
            "TRL": 2.5,
            "ABLD": 3.5,
            "stage": "initial"
        }
    ]
    measurements_data = {
        "teeth_id": 1,
        "pair_measurements": [DentalMeasurements(**dm) for dm in dental_measurements],
        "teeth_center": (100, 200)
    }
    data = {
        "request_id": 123,
        "measurements": [Measurements(**measurements_data)],
        "message": "Success"
    }
    inference_response = InferenceResponse(**data)  # 創建 InferenceResponse 實例
    # 驗證每個屬性是否正確
    assert inference_response.request_id == 123
    assert len(inference_response.measurements) == 1
    assert inference_response.message == "Success"
    print("test_inference_response_valid: 成功")

def test_dental_measurements_invalid():
    # 測試無效的牙科測量數據
    invalid_data = {
        "side_id": -1,  # 無效的 side_id
        "CEJ": (1, 2),
        "ALC": (3, 4),
        "APEX": (5, 6),
        "CAL": "invalid",  # 無效的 CAL
        "TRL": 2.5,
        "ABLD": 3.5,
        "stage": "initial"
    }
    try:
        DentalMeasurements(**invalid_data)  # 嘗試創建無效的 DentalMeasurements 實例
        assert False, "應該引發驗證錯誤"  # 如果沒有引發錯誤，則測試失敗
    except ValueError as e:
        print(f"test_dental_measurements_invalid: 失敗，錯誤信息: {e}")  # 輸出錯誤信息

def test_measurements_invalid():
    # 測試無效的測量數據
    invalid_data = {
        "teeth_id": -1,  # 無效的 teeth_id
        "pair_measurements": [],
        "teeth_center": (100, "invalid")  # 無效的 teeth_center
    }
    try:
        Measurements(**invalid_data)  # 嘗試創建無效的 Measurements 實例
        assert False, "應該引發驗證錯誤"  # 如果沒有引發錯誤，則測試失敗
    except ValueError as e:
        print(f"test_measurements_invalid: 失敗，錯誤信息: {e}")  # 輸出錯誤信息

def test_inference_response_invalid():
    # 測試無效的推斷響應數據
    invalid_data = {
        "request_id": -1,  # 無效的 request_id
        "measurements": [],  # 可以是空列表，但可能需要至少一個有效的測量
        "message": ""  # 無效的 message
    }
    try:
        InferenceResponse(**invalid_data)  # 嘗試創建無效的 InferenceResponse 實例
        assert False, "應該引發驗證錯誤"  # 如果沒有引發錯誤，則測試失敗
    except ValueError as e:
        print(f"test_inference_response_invalid: 失敗，錯誤信息: {e}")  # 輸出錯誤信息
    except Exception as e:
        print(f"test_inference_response_invalid: 失敗，發生了其他錯誤: {e}")  # 輸出其他錯誤信息

def test_dental_measurements_empty_tuple():
    # 測試邊界條件，使用空元組
    data = {
        "side_id": 1,
        "CEJ": (0, 0),  # 邊界條件
        "ALC": (0, 0),
        "APEX": (0, 0),
        "CAL": 0.0,
        "TRL": 0.0,
        "ABLD": 0.0,
        "stage": "initial"
    }
    measurement = DentalMeasurements(**data)  # 創建 DentalMeasurements 實例
    assert measurement.CEJ == (0, 0)  # 驗證 CEJ 是否正確
    print("test_dental_measurements_empty_tuple: 成功")

def test_dental_measurements_serialization():
    # 測試牙科測量的序列化
    data = {
        "side_id": 1,
        "CEJ": (1, 2),
        "ALC": (3, 4),
        "APEX": (5, 6),
        "CAL": 1.5,
        "TRL": 2.5,
        "ABLD": 3.5,
        "stage": "initial"
    }
    measurement = DentalMeasurements(**data)  # 創建 DentalMeasurements 實例
    measurement_dict = measurement.model_dump()  # 使用 model_dump 代替 dict
    # 驗證序列化後的數據是否正確
    assert measurement_dict["side_id"] == 1
    assert measurement_dict["CEJ"] == (1, 2)
    print("test_dental_measurements_serialization: 成功")

def test_measurements_serialization():
    # 測試測量的序列化
    dental_measurements = [
        {
            "side_id": 1,
            "CEJ": (1, 2),
            "ALC": (3, 4),
            "APEX": (5, 6),
            "CAL": 1.5,
            "TRL": 2.5,
            "ABLD": 3.5,
            "stage": "initial"
        }
    ]
    data = {
        "teeth_id": 1,
        "pair_measurements": [DentalMeasurements(**dm) for dm in dental_measurements],
        "teeth_center": (100, 200)
    }
    measurements = Measurements(**data)  # 創建 Measurements 實例
    measurements_dict = measurements.model_dump()  # 使用 model_dump 代替 dict
    # 驗證序列化後的數據是否正確
    assert measurements_dict["teeth_id"] == 1
    print("test_measurements_serialization: 成功")