import unittest
from Konfigdz1 import execute_command

class TestEmulator(unittest.TestCase):
    def setUp(self):
        self.tar_file = "test_archive.tar"
        self.log_file = "logfile.csv"

    def test_ls(self):
        # Ожидаем, что файлы из архива будут выведены
        output = execute_command("ls", self.tar_file, self.log_file)
        print(output)  # Выводим для отладки
        expected_files = ['file3.txt']  # Ожидаем только file3.txt
        for file in expected_files:
            self.assertIn(file, output)

    def test_cd(self):
        # Переход в подкаталог и проверка содержимого
        execute_command("cd subdir", self.tar_file, self.log_file)
        output = execute_command("ls", self.tar_file, self.log_file)
        self.assertIn('file3.txt', output)

    def test_exit(self):
        # Проверка на правильный выход
        output = execute_command("exit", self.tar_file, self.log_file)
        self.assertEqual(output.strip(), "Exiting emulator...")

    def test_du(self):
        # Проверка команды du
        output = execute_command("du", self.tar_file, self.log_file)
        self.assertIn("Disk usage", output)

    def test_pwd(self):
        # Проверка команды pwd
        output = execute_command("pwd", self.tar_file, self.log_file)
        # Ожидаем вывод текущего каталога
        self.assertIn("subdir", output)  # Если вы в подкаталоге, проверьте его имя

    def test_uptime(self):
        # Проверка команды uptime
        output = execute_command("uptime", self.tar_file, self.log_file)
        self.assertIn("Uptime", output)

if __name__ == "__main__":
    unittest.main()
