import unittest
import numpy as np
import cv2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.dental_measure.main import *

class TestDentalFunctions(unittest.TestCase):

    def setUp(self):
        # 設置測試用的假圖像和遮罩
        self.test_image = np.zeros((500, 500, 3), dtype=np.uint8)  # 創建一個黑色圖像
        self.masks_dict = {
            'dental_crown': np.ones((500, 500), dtype=np.uint8) * 255,  # 模擬牙冠的遮罩
            'dentin': np.ones((500, 500), dtype=np.uint8) * 255,        # 模擬牙本質的遮罩
            'gum': np.ones((500, 500), dtype=np.uint8) * 255            # 模擬牙齦的遮罩
        }

    def test_extract_features(self):
        """測試 extract_features 函數"""
        print("正在測試 extract_features 函數...")
        overlay, line_image, non_masked_area = extract_features(self.masks_dict, self.test_image)

        # 確保返回的圖像是三通道
        if len(overlay.shape) == 2:  # 如果是單通道
            overlay = cv2.cvtColor(overlay, cv2.COLOR_GRAY2BGR)
        if len(line_image.shape) == 2:  # 如果是單通道
            line_image = cv2.cvtColor(line_image, cv2.COLOR_GRAY2BGR)
        if len(non_masked_area.shape) == 2:  # 如果是單通道
            non_masked_area = cv2.cvtColor(non_masked_area, cv2.COLOR_GRAY2BGR)

        # 驗證返回的 overlay 是否為正確形狀
        self.assertEqual(overlay.shape, (500, 500, 3))
        self.assertEqual(line_image.shape, (500, 500, 3))
        self.assertEqual(non_masked_area.shape, (500, 500, 3))
        print("extract_features 測試通過！")

    def test_locate_points(self):
        """測試 locate_points 函數"""
        print("正在測試 locate_points 函數...")
        component_mask = np.ones((500, 500), dtype=np.uint8) * 255  # 模擬完整的遮罩
        binary_images = {
            'dental_crown': self.masks_dict['dental_crown'],
            'gum': self.masks_dict['gum'],
            'dentin': self.masks_dict['dentin']
        }
        overlay = self.test_image.copy()
        prediction = locate_points(self.test_image, component_mask, binary_images, idx=0, overlay=overlay)

        # 驗證返回的預測是否包含預期的鍵
        self.assertIn("teeth_center", prediction)
        print("locate_points 測試通過！")

    def test_get_mask_dict_from_model(self):
        """測試 get_mask_dict_from_model 函數"""
        print("正在測試 get_mask_dict_from_model 函數...")
        
        # 模擬一個模型返回的結果
        class MockModel:
            def predict(self, image):
                class Box:
                    def __init__(self, cls):
                        self.cls = cls
                        self.conf = 1.0  # 模擬的置信度

                class Mask:
                    def __init__(self, mask):
                        self.data = mask  # 將 mask 存儲在 data 屬性中

                class Result:
                    def __init__(self):
                        self.names = {0: 'dental_crown', 1: 'dentin', 2: 'gum'}
                        self.boxes = [Box(0), Box(1), Box(2)]  # 模擬的框
                        self.masks = [Mask(np.ones((500, 500), dtype=np.uint8) * 255) for _ in range(3)]  # 模擬的遮罩

                return [Result()]  # 返回一個包含 Result 對象的列表

        model = MockModel()  # 創建模擬模型實例
        masks_dict = get_mask_dict_from_model(model, self.test_image)  # 調用函數處理結果

        # 驗證返回的遮罩字典是否包含預期的鍵
        self.assertIn('dental_crown', masks_dict)
        self.assertIn('dentin', masks_dict)
        self.assertIn('gum', masks_dict)
        print("get_mask_dict_from_model 測試通過！")

    def test_dental_estimation(self):
        """測試 dental_estimation 函數"""
        print("正在測試 dental_estimation 函數...")
        result_image = dental_estimation(self.test_image, return_type='image')

        # 驗證返回的圖像是否為正確形狀
        self.assertEqual(result_image.shape, self.test_image.shape)
        print("dental_estimation 測試通過！")

if __name__ == '__main__':
    unittest.main()