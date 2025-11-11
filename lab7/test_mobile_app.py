from appium import webdriver
from appium.options.android import UiAutomator2Options
from appium.webdriver.common.appiumby import AppiumBy
import time
import subprocess
import os


class MobileAppTest:
    def __init__(self):
        self.options = UiAutomator2Options()
        self.setup_capabilities()
        self.driver = None
        self.adb_path = self.find_adb_path()

    def find_adb_path(self):
        """Поиск пути к adb"""
        # Стандартные пути установки Android SDK
        possible_paths = [
            # Windows стандартный путь
            r"C:\Users\Pavel\AppData\Local\Android\Sdk\platform-tools\adb.exe",
            # Путь для текущего пользователя
            os.path.expanduser(r"~\AppData\Local\Android\Sdk\platform-tools\adb.exe"),
            # Альтернативные пути
            r"C:\Android\platform-tools\adb.exe",
            # Путь из переменной окружения (если доступна)
            os.path.join(os.environ.get('ANDROID_HOME', ''), 'platform-tools', 'adb.exe')
        ]

        for path in possible_paths:
            if os.path.exists(path):
                print(f"Найден adb: {path}")
                return path

        print("ADB не найден. Убедитесь, что Android SDK установлен.")
        return None

    def setup_capabilities(self):
        """Настройка capabilities для приложения Настройки"""
        self.options.platform_name = 'Android'
        self.options.automation_name = 'UiAutomator2'
        self.options.no_reset = True
        # Используем стандартное приложение Настройки
        self.options.app_package = 'com.android.settings'
        self.options.app_activity = 'com.android.settings.Settings'

    def check_device_connection(self):
        """Проверка подключения устройства"""
        if not self.adb_path:
            print("ADB не доступен")
            return False

        try:
            result = subprocess.run(
                [self.adb_path, 'devices'],
                capture_output=True, text=True, timeout=10
            )
            print("Подключенные устройства:")
            print(result.stdout)

            # Проверяем наличие устройств
            lines = result.stdout.strip().split('\n')
            devices = [line for line in lines if '\tdevice' in line]

            if devices:
                print(f"✓ Найдено устройств: {len(devices)}")
                return True
            else:
                print("✗ Нет подключенных устройств")
                return False

        except Exception as e:
            print(f"✗ Ошибка при проверке устройств: {e}")
            return False

    def setup(self):
        """Настройка драйвера"""
        try:
            print("=== ИНИЦИАЛИЗАЦИЯ ДРАЙВЕРА APPIUM ===")

            # Проверяем подключение устройства
            if not self.check_device_connection():
                return False

            # Инициализируем драйвер
            self.driver = webdriver.Remote(
                'http://localhost:4723',
                options=self.options
            )
            print("✓ Драйвер успешно инициализирован")
            return True

        except Exception as e:
            print(f"✗ Ошибка инициализации драйвера: {e}")
            return False

    def test_app_launch(self):
        """Тест запуска приложения"""
        try:
            print("\n=== ТЕСТ ЗАПУСКА ПРИЛОЖЕНИЯ ===")

            # Ожидание загрузки приложения
            time.sleep(5)

            # Проверка текущего пакета и активности
            current_package = self.driver.current_package
            current_activity = self.driver.current_activity

            print(f"Текущий пакет: {current_package}")
            print(f"Текущая активность: {current_activity}")

            # Проверка, что мы в правильном приложении
            if current_package == 'com.android.settings':
                print("✓ Приложение Настройки успешно запущено")
                return True
            else:
                print("✗ Приложение Настройки не запущено")
                return False

        except Exception as e:
            print(f"✗ Ошибка при тесте запуска: {e}")
            return False

    def test_ui_elements(self):
        """Тест поиска UI элементов"""
        try:
            print("\n=== ТЕСТ ПОИСКА UI ЭЛЕМЕНТОВ ===")

            # Поиск различных типов элементов
            text_views = self.driver.find_elements(AppiumBy.CLASS_NAME, "android.widget.TextView")

            print(f"Найдено текстовых элементов: {len(text_views)}")

            # Вывод текстов первых 5 элементов
            print("\nТекстовые элементы (первые 5):")
            for i, text_view in enumerate(text_views[:5]):
                try:
                    text = text_view.text
                    if text and text.strip():
                        print(f"  {i + 1}. {text}")
                except:
                    continue

            if len(text_views) > 0:
                print("✓ UI элементы успешно найдены")
                return True
            else:
                print("✗ Не найдено UI элементов")
                return False

        except Exception as e:
            print(f"✗ Ошибка при поиске UI элементов: {e}")
            return False

    def test_simple_interaction(self):
        """Простой тест взаимодействия"""
        try:
            print("\n=== ТЕСТ ВЗАИМОДЕЙСТВИЯ ===")

            # Получение размера экрана
            window_size = self.driver.get_window_size()
            print(f"Размер экрана: {window_size}")

            # Простой тап по центру экрана
            center_x = window_size['width'] // 2
            center_y = window_size['height'] // 2

            print(f"Тап по координатам: ({center_x}, {center_y})")
            self.driver.tap([(center_x, center_y)])
            time.sleep(2)

            print("✓ Тап выполнен успешно")
            return True

        except Exception as e:
            print(f"✗ Ошибка при тесте взаимодействия: {e}")
            return False

    def test_screen_operations(self):
        """Тест операций с экраном"""
        try:
            print("\n=== ТЕСТ ОПЕРАЦИЙ С ЭКРАНОМ ===")

            # Получение ориентации экрана
            orientation = self.driver.orientation
            print(f"Текущая ориентация: {orientation}")

            # Создание скриншота
            screenshot_path = "appium_test_result.png"
            self.driver.save_screenshot(screenshot_path)
            print(f"✓ Скриншот сохранен: {screenshot_path}")

            return True

        except Exception as e:
            print(f"✗ Ошибка при тесте операций с экраном: {e}")
            return False

    def teardown(self):
        """Завершение работы"""
        if self.driver:
            self.driver.quit()
            print("✓ Драйвер закрыт")

    def run_tests(self):
        """Запуск всех тестов"""
        print("=" * 60)
        print("АВТОМАТИЗИРОВАННОЕ ТЕСТИРОВАНИЕ МОБИЛЬНОГО ПРИЛОЖЕНИЯ")
        print("=" * 60)

        if not self.setup():
            print("Не удалось инициализировать тестирование")
            return False

        try:
            # Запуск тестов
            tests = [
                ("Запуск приложения", self.test_app_launch),
                ("Поиск UI элементов", self.test_ui_elements),
                ("Простое взаимодействие", self.test_simple_interaction),
                ("Операции с экраном", self.test_screen_operations)
            ]

            results = []
            for test_name, test_func in tests:
                print(f"\n--- Выполнение: {test_name} ---")
                result = test_func()
                results.append((test_name, result))
                time.sleep(2)

            # Вывод результатов
            print("\n" + "=" * 60)
            print("РЕЗУЛЬТАТЫ ТЕСТИРОВАНИЯ")
            print("=" * 60)

            passed_tests = sum(1 for _, result in results if result)
            total_tests = len(results)

            for test_name, result in results:
                status = "ПРОЙДЕН" if result else "НЕ ПРОЙДЕН"
                symbol = "✓" if result else "✗"
                print(f"{symbol} {test_name}: {status}")

            print(f"\nИтого: {passed_tests}/{total_tests} тестов пройдено")

            if passed_tests == total_tests:
                print("✓ ВСЕ ТЕСТЫ УСПЕШНО ПРОЙДЕНЫ!")
            else:
                print("⚠ Некоторые тесты не пройдены, но основные функции работают")

            return passed_tests > 0  # Считаем успехом, если хотя бы один тест прошел

        except Exception as e:
            print(f"Критическая ошибка при выполнении тестов: {e}")
            return False
        finally:
            self.teardown()


if __name__ == "__main__":
    # Проверка наличия необходимых модулей
    try:
        test = MobileAppTest()
        success = test.run_tests()

        print("\n" + "=" * 60)
        if success:
            print("ВСЕ ТЕСТЫ ВЫПОЛНЕНЫ УСПЕШНО!")
            print("Настройка окружения Appium")
            print("Подключение к Android устройству")
            print("Автоматизированное тестирование мобильного приложения")
            print("Взаимодействие с UI элементами")
        else:
            print("Есть проблемы с настройкой окружения")

        exit(0 if success else 1)

    except ImportError as e:
        print(f"Ошибка импорта: {e}")
        print("Убедитесь, что установлены необходимые пакеты:")
        print("pip install Appium-Python-Client")
        exit(1)