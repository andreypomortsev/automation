import unittest
from unittest.mock import patch, MagicMock
import socket
from source import health_check


class TestCheckHealthCheck(unittest.TestCase):
    @patch("psutil.cpu_percent", MagicMock(return_value=85))
    def test_cpu_usage_above_threshold(self):
        result = health_check.check_cpu()
        self.assertEqual(result, "Error - CPU usage is over 80%")

    @patch("psutil.cpu_percent", MagicMock(return_value=70))
    def test_cpu_usage_below_threshold(self):
        result = health_check.check_cpu()
        self.assertIsNone(result)

    @patch("psutil.virtual_memory")
    def test_check_ram_less_than_threshold(self, mock_vm):
        # set available memory to 499 MB
        mock_vm.return_value = MagicMock(available=499 * 1024 * 1024)
        result = health_check.check_ram()
        self.assertEqual(result, "Error - Available memory is less than 500MB")

    @patch("psutil.virtual_memory")
    def test_check_ram_greater_than_threshold(self, mock_vm):
        # set available memory to 501 MB
        mock_vm.return_value = MagicMock(available=501 * 1024 * 1024)
        result = health_check.check_ram()
        self.assertIsNone(result)

    @patch("shutil.disk_usage")
    def test_check_disk_below_threshold(self, mock_disk):
        total = 10000  # 10 GB
        used = 8500  # 8.5 GB
        free = total - used  # 1.5 GB
        mock_disk.return_value = MagicMock(total=total, used=used, free=free)
        result = health_check.check_disk()
        self.assertEqual(result, "Error - Available disk space is less than 20%")

    @patch("shutil.disk_usage")
    def test_check_disk_above_threshold(self, mock_disk):
        total = 10000  # 10 GB
        used = 6000  # 6 GB
        free = total - used  # 4 GB
        mock_disk.return_value = MagicMock(total=total, used=used, free=free)
        result = health_check.check_disk()
        self.assertIsNone(result)

    @patch("socket.gethostbyname")
    def test_check_network_with_internet(self, mock_gethostbyname):
        mock_gethostbyname.side_effect = lambda x: "127.0.0.1"
        result = health_check.check_network()
        self.assertIsNone(result)

    @patch("socket.gethostbyname")
    def test_check_network_wo_internet(self, mock_gethostbyname):
        mock_gethostbyname.side_effect = socket.gaierror
        result = health_check.check_network()
        self.assertEqual(result, "Error - localhost cannot be resolved to 127.0.0.1")

    @patch("source.health_check.check_disk")
    @patch("source.health_check.check_network")
    @patch("source.health_check.check_ram")
    @patch("source.health_check.check_cpu")
    @patch("source.emails.generate")
    @patch("source.emails.send")
    def test_system_ok(
        self,
        mock_send,
        mock_generate,
        mock_check_disk,
        mock_check_network,
        mock_check_ram,
        mock_check_cpu,
    ):
        mock_check_cpu.return_value = None
        mock_check_disk.return_value = None
        mock_check_network.return_value = None
        mock_check_ram.return_value = None

        health_check.system_check()

        mock_check_cpu.assert_called_once()
        mock_check_disk.assert_called_once()
        mock_check_network.assert_called_once()
        mock_check_ram.assert_called_once()
        mock_generate.assert_not_called()
        mock_send.assert_not_called()

    @patch("source.emails.send")
    @patch("source.health_check.check_cpu")
    @patch("source.health_check.check_ram")
    @patch("source.health_check.check_network")
    @patch("source.health_check.check_disk")
    def test_system_is_not_ok(
        self,
        mock_check_disk,
        mock_check_network,
        mock_check_ram,
        mock_check_cpu,
        mock_send,
    ):
        errors = (
            "Error - CPU usage is over 80%",
            "Error - Available memory is less than 500MB",
            "Error - localhost cannot be resolved to 127.0.0.1",
            "Error - Available disk space is less than 20%",
        )
        mock_check_cpu.side_effect = errors
        mock_check_ram.side_effect = errors
        mock_check_network.side_effect = errors
        mock_check_disk.side_effect = errors

        health_check.system_check()

        mock_check_cpu.assert_called_once()
        mock_check_ram.assert_called_once()
        mock_check_network.assert_called_once()
        mock_check_disk.assert_called_once()
        mock_send.assert_has_calls(mock_send.mock_calls)


if __name__ == "__main__":
    unittest.main()
