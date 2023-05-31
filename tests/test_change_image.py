import unittest
import os.path
from PIL import Image
from source import change_image


class TestBulkImageProcess(unittest.TestCase):
    """
    A class for testing the bulk image processing functionality of the 'change_image' module.
    """
    def setUp(self):
        """
        Initializes test data by creating test images in the destination directory.
        
        :return: None
        """
        self.test_images = ["apple.jpg", "banana.jpg", "grapes.jpeg"]
        self.test_dir = change_image.DESTINATION
        for img in self.test_images:
            Image.new("RGB", (640, 480), color=(255, 0, 0)).save(
                os.path.join(self.test_dir, img)
            )

    def tearDown(self):
        """
        Removes test images from the destination directory.
        
        :return: None
        """
        for img in self.test_images:
            os.remove(os.path.join(change_image.DESTINATION, img))

    def test_changer_resizes_and_saves_image(self):
        """
        Tests the 'changer' method of the 'change_image' module by verifying 
        that it resizes and saves an image correctly.
        
        :return: None
        """
        img_path = os.path.join(self.test_dir, "apple.jpg")
        change_image.changer(img_path)
        expected_path = os.path.join(change_image.DESTINATION, "apple.jpg")
        self.assertTrue(os.path.exists(expected_path))
        with Image.open(expected_path) as img:
            self.assertEqual(img.size, (600, 400))


if __name__ == "__main__":
    unittest.main()
