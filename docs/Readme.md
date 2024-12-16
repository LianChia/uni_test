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
        1. 測試 extract_features 函數
        - 驗證是否正確提取特徵，例如 overlay 和 non_masked_area 的形狀是否與原始圖像一致。
        - 檢查輸入遮罩中是否包含有效數據。
        - 添加日誌輸出便於調試。  

        2. 測試 locate_points 函數  
        - 驗證返回值是否包含 teeth_center 並且該值是元組類型。  
        - 測試使用的遮罩和二值圖像是否正常運行。  

        3. 測試 get_mask_dict_from_model 函數
        - 確保從模型返回的遮罩字典類型為 dict。
        - 檢查字典是否包含關鍵鍵（例如 dental_crown）。

        4. 測試 generate_error_image 函數  
        - 確保生成的錯誤圖像具有預期的形狀（500x500x3）。  
        - 驗證圖像中心像素顏色是否為白色 [255, 255, 255]。  

        5. 測試 dental_estimation 函數
        - 驗證返回的圖像結果是否與原始圖像形狀一致。  

        6. 測試牙科估計功能的特定場景
        - 測試正常牙科 X 光圖像，驗證結果是否非空且正確。
        - 測試黑色圖像，檢查是否返回空結果清單。  

        但目前第二、三、四項出現錯誤  
        錯誤如下：
        ```
        ----------------------------------------------------------- Captured stdout call ----------------------------------------------------------- 
        正在加載模型...
        測試定位點...
        ========================================================= short test summary info ========================================================== 
        FAILED test_main.py::TestDentalAnalysis::test_extract_features - ValueError: attempt to get argmax of an empty sequence
        FAILED test_main.py::TestDentalAnalysis::test_generate_error_image - AssertionError: False is not true : 中心像素不是白色
        FAILED test_main.py::TestDentalAnalysis::test_get_mask_dict_from_model - AssertionError: 'dental_crown' not found in {'Alveolar_bone': array([[  0,   0,   0, ...,   0,   0,   0],
        FAILED test_main.py::TestDentalAnalysis::test_locate_points - AssertionError: 'teeth_center' not found in {}
        ======================================================= 4 failed, 3 passed in 16.65s ======================================================= 
