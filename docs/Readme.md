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
        1. test_dental_measurements
        - 測試有效數據是否可以正確實例化 DentalMeasurements 對象。
        - 測試無效數據是否會正確引發 ValidationError。

        2. test_stage_values
        - 測試所有有效的 stage 值是否可以正確實例化。
        - 測試所有無效的 stage 值是否會正確引發錯誤。  

        3. test_dental_measurements_serialization
        - 測試 DentalMeasurements 對象的序列化功能，驗證序列化後的數據正確性。  

        4. test_boundary_conditions
        - 測試各個屬性的邊界條件，確保最低和最高邊界值能正確處理。

        5. test_exception_handling
        - 測試不正確的數據是否能正確引發 ValidationError。
        - 驗證在不同屬性中出現的無效數據是否能被正確檢測並引發錯誤。  

        總共5項測試。

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

        <!-- 4. test_get_mask_dict_from_model 方法
        - 測試 get_mask_dict_from_model 函數的功能。
        - 模擬一個模型的返回結果，並驗證返回的遮罩字典是否包含預期的鍵（如 'dental_crown'、'dentin' 和 'gum'）。   -->

        5. test_dental_estimation 方法
        - 測試 dental_estimation 函數的功能。
        - 驗證該函數返回的圖像是否具有與原始測試圖像相同的形狀。   

        總共3項測試。
    
    3. ```
        test_dentalMeasure.py
        ```
        1. test_dentalEstimation_normalImage
        - 測試正常的 X-ray 影像是否能正確處理：
            - 確保能正確載入影像檔案，若檔案不存在或載入失敗，則引發錯誤。
            - 調用 dental_estimation 函數時，檢查是否能返回非空結果。
            - 若返回結果為空，則引發錯誤。

        2. test_dentalEstimation_blackimage
        - 測試全黑影像是否會被正確處理：
            - 確保能正確載入影像檔案，若檔案不存在或載入失敗，則引發錯誤。
            - 調用 dental_estimation 函數時，檢查返回的結果是否為空列表 []。
            - 若返回非空結果，則引發錯誤。

        總共2項測試。

12/17 檢查筆記：  
- schemas.py
    1. 可以增加更多無效值，例如：null、[]、False  
    2. stage的值應該為0、1、2、3；0、i、ii、iii
    3. 可以整理成一個list，讓指令更簡潔  
- main.py  
    1. test_get_mask_dict_from_model功能是檢查model是否正確，不正確範例如下：  
        a. 改名後的.pt  
        b. 隨便insert的.pt  
        p.s.這個可以先不加入  
# Nested if-else
## 概念  
 - Nested if-else 是指在一個 if 或 else 區塊內，嵌套另一個 if 或 else 條件語句。這樣的結構允許你在檢查一個條件之後，再針對更細緻的條件進行進一步的判斷。  
## 用意  
1. 多層條件檢查  
    當需要針對不同的條件進行多層次的檢查時，Nested if-else 是一種直觀的方式。例如，只有在某一條件成立的基礎上，再檢查另一個更具體的條件。
2. 細分邏輯  
    它可以將邏輯劃分為多個層次，每個層次處理不同的情況，這在處理複雜的業務邏輯時很常見。  
3. 控制流程  
    它允許在不同條件下執行不同的代碼塊，並根據條件的組合來決定結果。 
### Early Returns  
是一種控制流程的方式，可以在滿足條件時提前返回結果，減少不必要的嵌套和邏輯複雜性。  
### Ternary Operators  
是一種簡化條件語句的方式，通常用於簡短的邏輯判斷。  
```
def pass_or_fail(score):
    return "Pass" if score >= 60 else "Fail"
```
### Using Function or Dict  
利用函數或字典實現條件邏輯，可以減少冗長的 if-else 或 nested if-else。  

