import unittest
import numpy as np
import cv2
import sys
import os

sys.path.append(os.path.abspath(os.path.join(os.path.dirname(__file__), '../')))
from src.dental_measure.main import *

class TestDentalAnalysis(unittest.TestCase):

    def setUp(self):
        print("正在加載模型...")
        self.components_model = YOLO('C:/Users/SSTek/Desktop/LianChia/dentistry-inference-fastapi-main/model/dentistry_yolov11x-seg-all_4.42.pt')
        self.contour_model = YOLO('C:/Users/SSTek/Desktop/LianChia/dentistry-inference-fastapi-main/model/dentistryContour_yolov11n-seg_4.46.pt')
        
        # 使用帶有特徵的測試圖像
        self.original_img = np.ones((500, 500, 3), dtype=np.uint8) * 255  
        # 使用已知的遮罩字典
        self.masks_dict = {
            'dental_crown': np.random.randint(0, 2, (500, 500), dtype=np.uint8),
            'dentin': np.random.randint(0, 2, (500, 500), dtype=np.uint8),
            'gum': np.random.randint(0, 2, (500, 500), dtype=np.uint8)
        }

    def test_extract_features(self):
        print("測試提取特徵...")
        print("masks_dict:", self.masks_dict)  # 添加日誌
        if not np.any(self.masks_dict['dental_crown']):
            self.fail("dental_crown遮罩為空，無法提取特徵")
        
        overlay, line_image, non_masked_area = extract_features(self.masks_dict, self.original_img)
        self.assertEqual(overlay.shape, self.original_img.shape)
        self.assertEqual(non_masked_area.shape, self.original_img.shape)
        print("提取特徵成功，overlay形狀:", overlay.shape)

    def test_locate_points(self):
        print("測試定位點...")
        component_mask = self.masks_dict['dentin']
        binary_images = {
            "dental_crown": self.masks_dict['dental_crown'],
            "gum": self.masks_dict['gum']
        }
        idx = 0
        overlay = self.original_img.copy()
        prediction = locate_points(self.original_img, component_mask, binary_images, idx, overlay)
        self.assertIn('teeth_center', prediction)
        self.assertIsInstance(prediction['teeth_center'], tuple)
        print("定位點成功，teeth_center:", prediction['teeth_center'])

    def test_get_mask_dict_from_model(self):
        print("測試從模型獲取遮罩字典...")
        masks_dict = get_mask_dict_from_model(self.components_model, self.original_img, method='semantic')
        self.assertIsInstance(masks_dict, dict)
        self.assertIn('dental_crown', masks_dict)
        print("獲取遮罩字典成功，遮罩類別:", masks_dict.keys())

    def test_generate_error_image(self):
        print("測試生成錯誤圖像...")
        text = "Test Error"
        error_image = generate_error_image(text)
        self.assertEqual(error_image.shape, (500, 500, 3))
        center_pixel = error_image[250, 250]
        self.assertTrue(np.array_equal(center_pixel, [255, 255, 255]), "中心像素不是白色")
        print("生成錯誤圖像成功，中心像素顏色:", center_pixel)

    def test_dental_estimation(self):
        print("測試牙科估計...")
        result_image = dental_estimation(self.original_img, return_type='image')
        self.assertEqual(result_image.shape, self.original_img.shape)
        print("牙科估計成功，結果圖像形狀:", result_image.shape)

class TestDentalEstimation(unittest.TestCase):

    def test_dentalEstimation_normalImage(self):
        print("測試正常圖像...")
        image = cv2.imread('C:/Users/SSTek/Desktop/LianChia/dentistry-inference-fastapi-main/tests/nomal-x-ray-0.8510638-270-740_0_2022011008.png')
        if image is None:
            self.fail("Image not found, check test image path (or utf8 problems) or cv2 package")
        
        results_list = dental_estimation(image, scale=(31/960, 41/1080), return_type='dict')
        self.assertIsNotNone(results_list, "When input normal image, the result should be found")
        self.assertGreater(len(results_list), 0, "When input normal image, the result should not be empty")

    def test_dentalEstimation_blackimage(self):
        print("測試黑色圖像...")
        image = cv2.imread('C:/Users/SSTek/Desktop/LianChia/dentistry-inference-fastapi-main/tests/black.png')
        if image is None:
            self.fail("Image not found, check test image path (or utf8 problems) or cv2 package")
        
        results_list = dental_estimation(image, scale=(31/960, 41/1080), return_type='dict')
        self.assertIsNotNone(results_list, "When input black image, the result should be []")
        self.assertEqual(results_list, [], "When input black image, the result should be empty")

if __name__ == '__main__':
    unittest.main()