import unittest
import os.path
from PIL import Image
from source import change_image


class TestBulkImageProcess(unittest.TestCase):
    def setUp(self):
        self.test_images = ["apple.jpg", "banana.jpg", "grapes.jpeg"]
        self.test_dir = os.path.join(
            os.path.dirname(os.path.abspath(__file__)), "test_images"
        )
        os.makedirs(self.test_dir, exist_ok=True)
        for img in self.test_images:
            Image.new("RGB", (640, 480), color=(255, 0, 0)).save(
                os.path.join(self.test_dir, img)
            )

    def tearDown(self):
        for img in self.test_images:
            os.remove(os.path.join(change_image.DESTINATION, img))
        os.rmdir(self.test_dir)

    def test_changer_resizes_and_saves_image(self):
        img_path = os.path.join(self.test_dir, "apple.jpg")
        change_image.changer(img_path)
        expected_path = os.path.join(change_image.DESTINATION, "apple.jpg")
        self.assertTrue(os.path.exists(expected_path))
        with Image.open(expected_path) as img:
            self.assertEqual(img.size, (600, 400))

    def test_changer_raises_error_if_image_file_not_found(self):
        with self.assertRaises(Exception):
            change_image.changer("nonexistent.jpg")

    def test_changer_raises_error_if_file_is_not_image(self):
        txt_path = os.path.join(self.test_dir, "file.txt")
        with open(txt_path, "w") as txt_file:
            txt_file.write("this is a text file")
        with self.assertRaises(Exception):
            change_image.changer(txt_path)


if __name__ == "__main__":
    unittest.main()
