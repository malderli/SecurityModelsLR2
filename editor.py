from PyQt5.QtWidgets import QWidget, QGroupBox, QLineEdit, QTextEdit, QLabel, QPushButton, QTableWidget, QComboBox, QTableWidgetItem
from PyQt5.Qt import QGridLayout, QHBoxLayout, QMessageBox, Qt
import os
import json

class Editor(QWidget):
    USER = 0
    SHARED = 1

    def __init__(self):
        super(Editor, self).__init__()

        self.permissions = {}
        self.objects = []
        self.users = []

        self.currentUser = ""
        self.currentObjects = []

        self.setWindowTitle('МБКС ЛР2 | Лазарев Михайлин')
        self.setMinimumWidth(500)

        # +++++++++++++++++++++++++++ Folders +++++++++++++++++++++++++++

        self.gbPaths = QGroupBox('Пути')
        self.layoutPaths = QGridLayout()
        self.leSharedFolderPath = QLineEdit('Shared')
        self.lePermissionsFilePath = QLineEdit('permissions.json')

        self.layoutPaths.addWidget(QLabel('Папка сохранения: '), 0, 0)
        self.layoutPaths.addWidget(self.leSharedFolderPath, 0, 1)
        self.layoutPaths.addWidget(QLabel('Файл прав доступа: '), 1, 0)
        self.layoutPaths.addWidget(self.lePermissionsFilePath, 1, 1)

        self.gbPaths.setLayout(self.layoutPaths)

        # ++++++++++++++=++++++++++++++++++++++++++++++++++++++++++++++++

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^ Permissions ^^^^^^^^^^^^^^^^^^^^^^^^

        self.gbPermissionsView = QGroupBox('Права доступа:')
        self.lytPermissions = QGridLayout()
        self.twPermissions = QTableWidget()
        self.twPermissions.setAlternatingRowColors(True)

        self.lytPermissions.addWidget(self.twPermissions, 0, 0)

        self.gbPermissionsView.setLayout(self.lytPermissions)

        # ^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^^

        # &&&&&&&&&&&&&&&&&&&&&&&&& User select &&&&&&&&&&&&&&&&&&&&&&&&&

        self.gbUserSelection = QGroupBox('Выбор пользователя:')
        self.lytUserSelection = QGridLayout()
        self.cbUserSelect = QComboBox()
        self.lblAvailable = QLabel('Доступно:')

        self.lytUserSelection.addWidget(self.cbUserSelect, 0, 0)
        self.lytUserSelection.addWidget(self.lblAvailable, 1, 0)

        self.gbUserSelection.setLayout(self.lytUserSelection)

        # &&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&&

        # **************************** EDITOR ***************************

        self.gbEditor = QGroupBox('Редактор')
        self.layoutEditor = QGridLayout()
        self.leFileName = QLineEdit()
        self.teEditor = QTextEdit()
        self.layoutEditorSub = QHBoxLayout()

        self.btnOpen = QPushButton('Открыть')
        self.btnSaveFile = QPushButton('Сохранить')

        self.layoutEditorSub.setStretch(0, 1)
        self.layoutEditorSub.addWidget(self.btnSaveFile, 1)

        self.layoutEditor.addWidget(QLabel('Имя файла: '), 0, 0)
        self.layoutEditor.addWidget(self.leFileName, 0, 1)
        self.layoutEditor.addWidget(self.btnOpen, 0, 2)
        self.layoutEditor.addWidget(self.teEditor, 1, 0, 1, 3)
        self.layoutEditor.addLayout(self.layoutEditorSub, 2, 0, 1, 3)

        self.gbEditor.setLayout(self.layoutEditor)

        # ***************************************************************

        self.btnOpen.clicked.connect(self.btnOpenFileClicked)
        self.btnSaveFile.clicked.connect(self.btnSaveFileClicked)
        self.cbUserSelect.currentTextChanged.connect(self.cbUserSelectIndexChanged)

        self.loadPermissions()

        self.layoutMain = QGridLayout()
        self.layoutMain.addWidget(self.gbPaths, 0, 0)
        self.layoutMain.addWidget(self.gbPermissionsView, 1, 0)
        self.layoutMain.addWidget(self.gbUserSelection, 2, 0)
        self.layoutMain.addWidget(self.gbEditor, 3, 0)

        self.setLayout(self.layoutMain)

    def loadPermissions(self):
        self.twPermissions.clear()

        try:
            with open(self.lePermissionsFilePath.text(), "r") as fs:
                permissions = json.loads(fs.read())

                self.permissions = permissions
                self.objects = list(permissions['objects'])
                self.users = list(permissions['users'].keys())

                # Filling permissions table
                self.twPermissions.setColumnCount(len(self.objects))
                self.twPermissions.setHorizontalHeaderLabels(self.objects)
                self.twPermissions.setRowCount(len(self.users))
                self.twPermissions.setVerticalHeaderLabels(self.users)
                self.twPermissions.resizeColumnsToContents()

                for oid, obj in enumerate(self.objects):
                    for uid, user in enumerate(self.users):
                        if obj in self.permissions['users'][user]:
                            self.twPermissions.setItem(uid, oid, QTableWidgetItem("+"))

                # Adding users to selector
                self.cbUserSelect.clear()
                self.cbUserSelect.addItems(self.users)

        except:
            pass

    def cbUserSelectIndexChanged(self, user):
        self.lblAvailable.setText("Доступно: " + self.permissions['users'][user])

    def teTextChanged(self):
        pass

    def btnSaveFileClicked(self):
        fileName = self.leFileName.text()

        if len(fileName) <= 3:
            QMessageBox.warning(None, 'Некорректное название файла', 'Название файла должно содержать более 3 '
                                                                     'симоволов', QMessageBox.Ok)
            return

        with open(os.path.join(self.leSharedFolderPath.text(), fileName), 'w') as fs:
            fs.write(self.teEditor.toPlainText())

        self.updateUserFilesList()

    def btnOpenFileClicked(self):
        pass

    def keyPressEvent(self, event):
        try:
            if event.key() == Qt.Key_Delete:
                if self.focusWidget() == self.lwUserFolder:
                    os.remove(os.path.join(self.leSharedFolderPath.text(), self.lwUserFolder.currentItem().text()))
                    self.updateUserFilesList()

                elif self.focusWidget() == self.lwSharedFolder:
                    os.remove(os.path.join(self.lePermissionsFilePath.text(), self.lwSharedFolder.currentItem().text()))
                    self.updateSharedFilesList()
        except:
            QMessageBox.warning(None, 'Ошибка', 'Ошибка удаления файла', QMessageBox.Ok)
