# 建立環境
1. 開啟Anaconda Prompt，並執行以下指令
    ``` 
    conda create --name cvat-fastapi python=3.9
    ``` 
    ```
    conda activate cvat-fastapi  
    ```
2. 開啟VSCode選擇CONDA環境並執行指令
    ```  
     pip install -r requirements.txt
     ```  
P.S要先從 https://huggingface.co/smartsurgery/dentistry-models/tree/main 下載兩個MODEL  
1. dentistry_yolov11x-seg-all_4.42.pt
2. dentistryContour_yolov11n-seg_4.46.pt  
下載完畢後，將兩個檔案複製到./model目錄下
# 測試
3. 切換到tests目錄並執行指令
    
    1. ```
        pytest test_schemas.py  
        ```
    - 測試項目：  
        1. 測試有效的牙科測量數據(test_dental_measurements_valid)
        - 驗證 DentalMeasurements 類能夠正確處理有效的輸入數據，確保各屬性被正確設置。

        2. 測試有效的測量數據 (test_measurements_valid)
        - 驗證 Measurements 類能夠正確處理有效的輸入數據，包括牙齒 ID 和測量對的正確性。

        3. 測試有效的推斷響應數據 (test_inference_response_valid)
        - 驗證 InferenceResponse 類能夠正確處理有效的輸入數據，確保請求 ID、測量數據和消息的正確性。   

        4. 測試無效的牙科測量數據 (test_dental_measurements_invalid)
        - 驗證 DentalMeasurements 類對無效輸入數據的處理，確保在遇到無效數據時能夠引發相應的驗證錯誤。

        5. 測試無效的測量數據 (test_measurements_invalid)
        - 驗證 Measurements 類對無效輸入數據的處理，確保在遇到無效數據時能夠引發相應的驗證錯誤。

        6. 測試無效的推斷響應數據 (test_inference_response_invalid)
        - 驗證 InferenceResponse 類對無效輸入數據的處理，確保在遇到無效數據時能夠引發相應的驗證錯誤。

        7. 測試邊界條件的牙科測量數據 (test_dental_measurements_empty_tuple)
        - 驗證 DentalMeasurements 類能夠正確處理邊界條件，特別是使用空元組作為輸入數據。

        8. 測試牙科測量的序列化 (test_dental_measurements_serialization)
        - 驗證 DentalMeasurements 類的序列化功能，確保能夠正確轉換為字典格式以便於存儲或傳輸。

        9. 測試測量的序列化 (test_measurements_serialization)
        - 驗證 Measurements 類的序列化功能，確保能夠正確轉換為字典格式以便於存儲或傳輸。  
    2. ```
        test_main.py
        ```
        1. setUp 方法
        - 設置測試環境，包括創建一個黑色圖像和模擬的遮罩字典。這些遮罩代表牙冠、牙本質和牙齦，並用於後續的測試。  

        2. test_extract_features 方法

        - 測試 extract_features 函數的功能。
        - 驗證該函數返回的圖像（overlay、line_image 和 non_masked_area）是否都是三通道（即形狀為 (500, 500, 3)）。

        3. test_locate_points 方法
        - 測試 locate_points 函數的功能。
        - 驗證返回的預測結果中是否包含預期的鍵（例如 "teeth_center"）。

        4. test_get_mask_dict_from_model 方法
        - 測試 get_mask_dict_from_model 函數的功能。
        - 模擬一個模型的返回結果，並驗證返回的遮罩字典是否包含預期的鍵（如 'dental_crown'、'dentin' 和 'gum'）。  

        5. test_dental_estimation 方法

        - 測試 dental_estimation 函數的功能。
        - 驗證該函數返回的圖像是否具有與原始測試圖像相同的形狀。 

        錯誤如下：
        ```
        ----------------------------------------------------------- Captured stdout call ----------------------------------------------------------- 
        正在測試 get_mask_dict_from_model 函數...
        ========================================================= short test summary info ========================================================== 
        FAILED test_main.py::TestDentalFunctions::test_get_mask_dict_from_model - AttributeError: 'list' object has no attribute 'data'
        ======================================================= 1 failed, 3 passed in 7.47s ======================================================== 



12/17 檢查筆記：  
- schemas.py
    1. 可以增加更多無效值，例如：null、[]、False  
    2. stage的值應該為0、1、2、3；0、i、ii、iii
    3. 可以整理成一個list，讓指令更簡潔  
- main.py  
    1. test_get_mask_dict_from_model功能是檢查model是否正確，不正確範例如下：  
        a. 改名後的.pt  
        b. 隨便insert的.pt  