"""
Утилита командной строки Django для выполнения административных задач.

Этот файл является точкой входа для команд Django (manage.py).
Он используется для запуска миграций, создания суперпользователя,
запуска сервера разработки и других административных команд.
"""
import os
import sys


def main() -> None:
    """
    Запускает административные задачи Django.

    Устанавливает переменную окружения DJANGO_SETTINGS_MODULE,
    которая указывает Django, где найти файл настроек проекта.
    Затем выполняет команду, переданную через аргументы командной строки.

    Raises:
        ImportError: Если Django не установлен или недоступен в PYTHONPATH.
    """
    os.environ.setdefault('DJANGO_SETTINGS_MODULE', 'config.settings')
    try:
        from django.core.management import execute_from_command_line
    except ImportError as exc:
        raise ImportError(
            "Не удалось импортировать Django. Убедитесь, что Django установлен и "
            "доступен в переменной окружения PYTHONPATH. Возможно, вы "
            "забыли активировать виртуальное окружение?"
        ) from exc
    execute_from_command_line(sys.argv)


if __name__ == '__main__':
    main()