import hashlib
import json
import sys

import numpy as np  # todo remove
from PySide6.QtWidgets import QMainWindow, QWidget, QVBoxLayout, QHBoxLayout, QPushButton, QLabel, QTextEdit, \
    QApplication
from loguru import logger
from matplotlib.backends.backend_qt5agg import FigureCanvasQTAgg as FigureCanvas
from matplotlib.backends.backend_qt5agg import NavigationToolbar2QT as NavigationToolbar
from matplotlib.figure import Figure

from backup_files_loader import find_backup_files, BackupFilesNotFoundError, BackupFilesLoadingError
from backup_files_mapper import extract_current_state_from_backup_file
from singularity_parser.backup_files_repository import DatabaseManager

# path_to_backup_files = "C:\\Users\\79198\\AppData\\Roaming\\SingularityApp\\nedb-backup"
path_to_backup_files = "D:\\PythonProjects\\singularity-parser\\test_backup_files"

MAX_BACKUP_FILES = 5


class MainWindow(QMainWindow):

    def __init__(self):
        super().__init__()
        self.setWindowTitle("Статистика задач")
        self.setGeometry(100, 100, 1200, 700)

        # Центральный виджет и главный макет
        central_widget = QWidget()
        self.setCentralWidget(central_widget)
        main_layout = QVBoxLayout(central_widget)

        # --- 1. Верхняя панель: кнопка и метка ---
        top_panel = QHBoxLayout()
        self.update_button = QPushButton("Обновить данные")
        self.update_button.clicked.connect(self.update_all_data)  # Связь с функцией-обработчиком
        self.status_label = QLabel("Готово к загрузке данных.")
        top_panel.addWidget(self.update_button)
        top_panel.addStretch()  # Растягивающееся пространство
        top_panel.addWidget(self.status_label)
        main_layout.addLayout(top_panel)

        # --- 2. Средняя секция: два графика ---
        graphs_layout = QHBoxLayout()

        # График 1 (задачи по дням)
        self.canvas1, self.toolbar1, self.ax1 = self.create_matplotlib_widget()
        graph1_widget = QWidget()
        layout1 = QVBoxLayout(graph1_widget)
        layout1.addWidget(self.toolbar1)  # Панель инструментов (зум, сохранение)
        layout1.addWidget(self.canvas1)
        graphs_layout.addWidget(graph1_widget)

        # График 2 (задачи по проектам)
        self.canvas2, self.toolbar2, self.ax2 = self.create_matplotlib_widget()
        graph2_widget = QWidget()
        layout2 = QVBoxLayout(graph2_widget)
        layout2.addWidget(self.toolbar2)
        layout2.addWidget(self.canvas2)
        graphs_layout.addWidget(graph2_widget)

        main_layout.addLayout(graphs_layout)

        # --- 3. Нижняя секция: текстовая область ---
        self.text_area = QTextEdit()
        self.text_area.setPlaceholderText("Здесь будет выводиться сводная статистика...")
        main_layout.addWidget(self.text_area)

        # Инициализация графиков с пустыми данными
        self.initialize_plots()

    def create_matplotlib_widget(self):
        """Вспомогательная функция для создания холста, панели инструментов и осей."""
        fig = Figure(figsize=(5, 4), dpi=100)
        canvas = FigureCanvas(fig)
        toolbar = NavigationToolbar(canvas, self)  # Добавляет интерактивность
        ax = fig.add_subplot(111)
        return canvas, toolbar, ax

    def initialize_plots(self):
        """Настраивает начальный вид графиков (заголовки, подписи)."""
        self.ax1.set_title('Количество выполненных задач по дням')
        self.ax1.set_xlabel('День')
        self.ax1.set_ylabel('Кол-во задач')
        self.ax1.grid(True, alpha=0.3)

        self.ax2.set_title('Распределение задач по проектам')
        self.ax2.set_xlabel('Проект')
        self.ax2.set_ylabel('Кол-во задач')
        self.ax2.grid(True, alpha=0.3)

        # Обновляем холсты
        self.canvas1.draw()
        self.canvas2.draw()

    def update_all_data(self):
        """
        Основная функция, которая будет вызываться при нажатии кнопки.
        Здесь вы должны:
        1. Считать и распарсить ваш JSON с задачами.
        2. Преобразовать данные (например, с помощью Pandas).
        3. Обновить графики и текстовую область.
        """
        self.status_label.setText("Данные обновляются...")
        QApplication.processEvents()  # Чтобы интерфейс не "зависал"

        # === ЗДЕСЬ ВАШ КОД ДЛЯ РАБОТЫ С ДАННЫМИ ===
        # 1. Загрузка JSON (замените на ваш путь)
        # with open('backup.json', 'r') as f:
        #     data = json.load(f)
        # 2. Пример: использование pandas для агрегации
        # df = pd.DataFrame(data)
        # df['date'] = pd.to_datetime(df['date'])
        # daily_stats = df.groupby(df['date'].dt.date).size()
        # project_stats = df.groupby('project').size()

        # === ПРИМЕР С ГЕНЕРАЦИЕЙ ТЕСТОВЫХ ДАННЫХ (УДАЛИТЕ ЭТО) ===
        # Имитация данных за последние 7 дней
        days = np.arange(1, 8)
        tasks_per_day = np.random.randint(3, 10, size=7)
        projects = ['Проект А', 'Проект Б', 'Проект В', 'Проект Г']
        tasks_per_project = np.random.randint(5, 20, size=4)
        # =====================================================

        # --- Обновление графика 1 ---
        self.ax1.clear()
        self.ax1.bar(days, tasks_per_day, color='skyblue', edgecolor='black')
        self.ax1.set_title('Количество выполненных задач по дням (пример)')
        self.ax1.set_xlabel('День')
        self.ax1.set_ylabel('Кол-во задач')
        self.ax1.grid(True, alpha=0.3)
        self.canvas1.draw()

        # --- Обновление графика 2 ---
        self.ax2.clear()
        self.ax2.bar(projects, tasks_per_project, color='lightgreen', edgecolor='black')
        self.ax2.set_title('Распределение задач по проектам (пример)')
        self.ax2.set_xlabel('Проект')
        self.ax2.set_ylabel('Кол-во задач')
        self.canvas2.draw()

        # --- Обновление текстовой области ---
        total_tasks = tasks_per_day.sum()
        avg_tasks = tasks_per_day.mean()
        most_productive_day = days[np.argmax(tasks_per_day)]
        summary_text = f"""СВОДКА (на примере данных):
        Всего задач выполнено: {total_tasks}
        Среднее количество в день: {avg_tasks:.1f}
        Самый продуктивный день: День {most_productive_day}
        Самый загруженный проект: {projects[np.argmax(tasks_per_project)]}
        """
        self.text_area.setText(summary_text)

        self.status_label.setText(f"Данные обновлены. Всего задач: {total_tasks}")


def run_gui():
    app = QApplication(sys.argv)
    window = MainWindow()
    window.show()
    sys.exit(app.exec())


def init():
    backup_file = find_backup_files(path_to_backup_files)
    file_hash = hashlib.md5(str(backup_file.content).encode()).hexdigest()
    logger.info(f"Найден файл {backup_file.name}, MD5 хэш содержимого: {file_hash}")
    db_manager = DatabaseManager()

    if not db_manager.backup_file_exists(backup_file.name, file_hash):
        db_manager.save_backup_file(backup_file.name, json.dumps(backup_file.content), file_hash)

    current_state = extract_current_state_from_backup_file(backup_file.content)
    db_manager.save_projects(current_state.active_projects)
    db_manager.save_projects(current_state.archived_projects)
    db_manager.save_projects(current_state.deleted_projects)
    db_manager.save_tasks(current_state.active_tasks)
    db_manager.save_tasks(current_state.archived_tasks)

    db_manager.delete_last_backup_files(MAX_BACKUP_FILES)


if __name__ == '__main__':
    try:
        init()
        run_gui()
    except BackupFilesNotFoundError as e:
        logger.warning(str(e))
    except BackupFilesLoadingError as e:
        logger.error(str(e))