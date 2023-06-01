import unittest
from unittest.mock import patch, MagicMock
from source import health_check

class TestCheckCpu(unittest.TestCase):
    @patch('psutil.cpu_percent', MagicMock(return_value=85))
    def test_above_threshold(self):
        result = health_check.check_cpu()
        self.assertEqual(result, "Error - CPU usage is over 80%")

    @patch('psutil.cpu_percent', MagicMock(return_value=70))
    def test_below_threshold(self):
        result = health_check.check_cpu()
        self.assertIsNone(result)

    @patch('psutil.virtual_memory')
    def test_available_memory_less_than_500MB(self, mock_vm):
    	# set available memory to 499 MB
        mock_vm.return_value = MagicMock(available=499 * 1024 * 1024)
        result = health_check.check_ram()
        self.assertEqual(result, "Error - Available memory is less than 500MB")

    @patch('psutil.virtual_memory')
    def test_available_memory_greater_than_500MB(self, mock_vm):
    	# set available memory to 501 MB
        mock_vm.return_value = MagicMock(available=501 * 1024 * 1024)
        result = health_check.check_ram()
        self.assertIsNone(result)

    @patch('shutil.disk_usage')
    def test_check_disk_below_threshold(self, mock_disk):
        total = 10000 # 10 GB
        used = 8500 # 8.5 GB
        free = total - used # 2 GB
        mock_disk.return_value = MagicMock(total=total, used=used, free=free)
        result = health_check.check_disk()
        self.assertEqual(result, "Error - Available disk space is less than 20%")
    
    @patch('shutil.disk_usage')
    def test_check_disk_above_threshold(self, mock_disk):
        total = 10000 # 10 GB
        used = 6000 # 6 GB
        free = total - used # 4 GB
        mock_disk.return_value = MagicMock(total=total, used=used, free=free)
        result = health_check.check_disk()
        self.assertIsNone(result)

if __name__ == '__main__':
    unittest.main()