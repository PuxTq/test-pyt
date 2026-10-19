import shutil
import subprocess


def pytest_sessionfinish(session, exitstatus):
    results_dir = session.config.option.allure_report_dir
    if not results_dir:
        return

    allure = shutil.which("allure")
    if allure is None:
        print("\nКоманда 'allure' не найдена.")
        return

    report_dir = "allure-report"

    print("\n--- Создание отчёта Allure ---")
    result = subprocess.run([allure, "generate", results_dir, "-o", report_dir, "--clean"])
    if result.returncode != 0:
        print("Не удалось создать отчёт Allure.")
        return

    print("Отчёт сохранён в папке 'allure-report', открываем в браузере...")
    subprocess.Popen([allure, "open", report_dir])
