import sys
import os
import requests
from PyQt5.QtWidgets import (
    QApplication, QMainWindow, QVBoxLayout, QHBoxLayout, QWidget, QLabel, QPushButton, QLineEdit, QListWidget, QListWidgetItem, QMessageBox, QTextBrowser, QComboBox
)
from PyQt5.QtGui import QIcon, QFont
from PyQt5.QtCore import Qt
from git import Repo


class ProgramManager(QMainWindow):
    def __init__(self):
        super().__init__()
        self.setWindowTitle("Git Helper")
        self.setGeometry(100, 100, 800, 600)
        self.setWindowIcon(QIcon("icon.png"))

        self.central_widget = QWidget()
        self.setCentralWidget(self.central_widget)

        self.layout = QVBoxLayout(self.central_widget)

        self.header_layout = QHBoxLayout()
        self.header_label = QLabel("Program Manager")
        self.header_label.setFont(QFont("Arial", 20))
        self.header_layout.addWidget(self.header_label)

        self.theme_label = QLabel("Theme:")
        self.theme_label.setFont(QFont("Arial", 14))
        self.header_layout.addWidget(self.theme_label)

        self.theme_combo = QComboBox()
        self.theme_combo.addItems(["Light", "Dark"])
        self.theme_combo.setFont(QFont("Arial", 14))
        self.theme_combo.currentIndexChanged.connect(self.change_theme)
        self.header_layout.addWidget(self.theme_combo)

        self.layout.addLayout(self.header_layout)

        self.repo_layout = QHBoxLayout()
        self.repo_label = QLabel("Enter Repository Name:")
        self.repo_label.setFont(QFont("Arial", 14))
        self.repo_layout.addWidget(self.repo_label)

        self.repo_input = QLineEdit()
        self.repo_input.setFont(QFont("Arial", 14))
        self.repo_input.setPlaceholderText("repository-name")
        self.repo_layout.addWidget(self.repo_input)

        self.layout.addLayout(self.repo_layout)

        self.search_button = QPushButton("Search Repository")
        self.search_button.setFont(QFont("Arial", 14))
        self.search_button.clicked.connect(self.search_repository)
        self.layout.addWidget(self.search_button)

        self.repo_list = QListWidget()
        self.repo_list.setFont(QFont("Arial", 14))
        self.repo_list.itemClicked.connect(self.show_repo_info)
        self.layout.addWidget(self.repo_list)

        self.repo_info_label = QLabel("Repository Info:")
        self.repo_info_label.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.repo_info_label)

        self.repo_info_browser = QTextBrowser()
        self.repo_info_browser.setFont(QFont("Arial", 12))
        self.layout.addWidget(self.repo_info_browser)

        self.download_button = QPushButton("Download Selected Repository")
        self.download_button.setFont(QFont("Arial", 14))
        self.download_button.clicked.connect(self.download_repository)
        self.layout.addWidget(self.download_button)

        self.program_list = QListWidget()
        self.program_list.setFont(QFont("Arial", 14))
        self.layout.addWidget(self.program_list)

        self.load_programs()
        self.change_theme()

    def load_programs(self):
        self.program_list.clear()
        programs_dir = os.path.expanduser("~/programs")
        if not os.path.exists(programs_dir):
            os.makedirs(programs_dir)
        for program in os.listdir(programs_dir):
            item = QListWidgetItem(program)
            self.program_list.addItem(item)

    def search_repository(self):
        repo_name = self.repo_input.text().strip()
        if not repo_name:
            QMessageBox.warning(self, "Error", "Please enter a repository name.")
            return

        try:
            url = f"https://api.github.com/search/repositories?q={repo_name}"
            response = requests.get(url)
            response.raise_for_status()
            data = response.json()

            self.repo_list.clear()
            if data["total_count"] == 0:
                QMessageBox.information(self, "Info", "No repositories found.")
                return

            for repo in data["items"]:
                item = QListWidgetItem(f"{repo['full_name']} (Stars: {repo['stargazers_count']})")
                item.repo_data = repo
                self.repo_list.addItem(item)

        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to search repositories: {e}")

    def show_repo_info(self, item):
        repo_data = item.repo_data
        info = f"""
        Name: {repo_data['full_name']}
        Description: {repo_data['description']}
        Stars: {repo_data['stargazers_count']}
        Forks: {repo_data['forks_count']}
        URL: {repo_data['html_url']}
        """
        self.repo_info_browser.setText(info)

    def download_repository(self):
        selected_item = self.repo_list.currentItem()
        if not selected_item:
            QMessageBox.warning(self, "Error", "Please select a repository to download.")
            return

        repo_data = selected_item.repo_data
        repo_name = repo_data["full_name"].split("/")[-1]
        repo_url = repo_data["clone_url"]

        programs_dir = os.path.expanduser("~/programs")
        repo_path = os.path.join(programs_dir, repo_name)

        if os.path.exists(repo_path):
            QMessageBox.warning(self, "Error", f"Repository '{repo_name}' is already installed.")
            return

        try:
            Repo.clone_from(repo_url, repo_path)
            QMessageBox.information(self, "Success", f"Repository '{repo_name}' has been downloaded.")
            self.load_programs()
        except Exception as e:
            QMessageBox.critical(self, "Error", f"Failed to download repository: {e}")

    def change_theme(self):
        theme = self.theme_combo.currentText()
        if theme == "Dark":
            self.setStyleSheet("""
                QMainWindow { background-color: #2E3440; color: #D8DEE9; }
                QLabel { color: #D8DEE9; }
                QPushButton { background-color: #5E81AC; color: #D8DEE9; border-radius: 5px; padding: 5px; }
                QPushButton:hover { background-color: #81A1C1; }
                QLineEdit { background-color: #4C566A; color: #D8DEE9; border-radius: 5px; padding: 5px; }
                QListWidget { background-color: #4C566A; color: #D8DEE9; border-radius: 5px; padding: 5px; }
                QTextBrowser { background-color: #4C566A; color: #D8DEE9; border-radius: 5px; padding: 5px; }
                QComboBox { background-color: #5E81AC; color: #D8DEE9; border-radius: 5px; padding: 5px; }
            """)
        else:
            self.setStyleSheet("""
                QMainWindow { background-color: #FFFFFF; color: #000000; }
                QLabel { color: #000000; }
                QPushButton { background-color: #4CAF50; color: #FFFFFF; border-radius: 5px; padding: 5px; }
                QPushButton:hover { background-color: #81C784; }
                QLineEdit { background-color: #F1F1F1; color: #000000; border-radius: 5px; padding: 5px; }
                QListWidget { background-color: #F1F1F1; color: #000000; border-radius: 5px; padding: 5px; }
                QTextBrowser { background-color: #F1F1F1; color: #000000; border-radius: 5px; padding: 5px; }
                QComboBox { background-color: #4CAF50; color: #FFFFFF; border-radius: 5px; padding: 5px; }
            """)


if __name__ == "__main__":
    app = QApplication(sys.argv)
    window = ProgramManager()
    window.show()
    sys.exit(app.exec_())
