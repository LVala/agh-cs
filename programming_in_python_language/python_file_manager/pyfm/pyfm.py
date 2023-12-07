import sys
import os
import subprocess
from pathlib import Path
from copy import copy

import pyfm.qrc_resources
from pyfm.flow_layout import FlowLayout
from pyfm.file_button import FileButton
from pyfm.file_manage import *

from PyQt5.QtCore import Qt
from PyQt5.QtGui import QIcon, QPalette, QColor
from PyQt5.QtWidgets import (
    QApplication, 
    QWidget, 
    QMainWindow,
    QDialog,
    QMessageBox,
    QAction, 
    QLineEdit, 
    QLabel, 
    QCompleter, 
    QSplitter,
    QVBoxLayout,
    QHBoxLayout,
    QScrollArea,
    QTreeWidgetItem,
    QTreeWidget,
    QInputDialog,
    QDirModel,
)

TEXT_EDITOR = "code"

class PropertiesDialog(QDialog):
    def __init__(self, path, parent=None):
        super().__init__(parent)
        self.setWindowTitle('Properties')
        layout = QVBoxLayout()
        self.setLayout(layout)

        info = get_file_info(path)
        name = QLabel(f"Name: {path.split(os.sep)[-1]}")
        location = QLabel(f"Location: {'/'.join(path.split(os.sep)[0:-1])}")
        ftype = QLabel(f"Type: {info['type']}")
        permissions = QLabel(f"Permissions: {info['permissions']}")
        size = QLabel(f"Size: {info['size']} K")
        last_mod = QLabel(f"Last modification date: {info['lastmod']}")
        last_access = QLabel(f"Last access date: {info['lastaccess']}")
        last_meta = QLabel(f"Last metadata modification date: {info['lastmeta']}")
        layout.addWidget(name)
        layout.addWidget(location)
        layout.addWidget(ftype)
        layout.addWidget(permissions)
        layout.addWidget(size)
        layout.addWidget(last_mod)
        layout.addWidget(last_access)
        layout.addWidget(last_meta)

class Window(QMainWindow):
    def __init__(self, parent=None):
        super().__init__(parent)
        self.setWindowTitle("pyfm")
        self.resize(900, 700)
        self.centralWidget = QWidget(self)
        self.setCentralWidget(self.centralWidget)

        self.cur_path = os.getenv("HOME")
        self.files = list_all_files(self.cur_path)
        self.highlighted = []
        self.clipboard = []
        self.clipaction = None
        self.history_index = 0
        self.history = [os.getenv("HOME")]

        self._create_actions()
        self._create_menu_bar()
        self._create_tool_bars()
        self._create_context_menu()
        self._create_status_bar()
        self._create_side_panel()
        self._create_main_panel()

        layout = QHBoxLayout(self.centralWidget)
        splitter = QSplitter(self.centralWidget)
        layout.addWidget(splitter)
        splitter.addWidget(self.side_panel)
        splitter.addWidget(self.main_panel)

    ##### MISCELLANEOUS #####

    def _add_to_hist(self, dir_path):
        if self.history_index == len(self.history)-1:
            self.history.append(dir_path)
            self.history_index += 1
        else:
            self.history_index += 1
            self.history[self.history_index] = dir_path
            self.history = self.history[:self.history_index+1]

    def _clear_highlighted(self):
        for i in self.highlighted:
            i.dehighlight()
        self.highlighted.clear()

        self._get_item_count()

    def manage_highlighted(self, button, ctrl):
        if button not in self.highlighted:
            if ctrl:
                button.highlight()
                self.highlighted.append(button)
            else:
                self._clear_highlighted()
                button.highlight()
                self.highlighted.append(button)
        else:
            if ctrl:
                button.dehighlight()
                self.highlighted.remove(button)

        self._get_item_count()

    def jump_to_dir(self, dir_path, add_to_hist):
        try:
            dir_path = os.path.realpath(dir_path)
            if os.path.isdir(dir_path):
                if add_to_hist: 
                    self._add_to_hist(dir_path)

                self.cur_path = dir_path
                self.files = list_all_files(self.cur_path)
                self.dir_path_spinbox.setText(self.cur_path)
                self._update_main_panel()
                self._clear_highlighted()
        except PermissionError:
            QMessageBox.about(self, "Error", "Unable to open the directory due to lack of permissions")

    ##### ACTIONS AND ACTION HANDLING #####

    def _handle_go_prev_action(self):
        if self.history_index > 0:
            self.history_index -= 1
            self.jump_to_dir(self.history[self.history_index], False)

    def _handle_go_next_action(self):
        if self.history_index < len(self.history)-1:
            self.history_index += 1
            self.jump_to_dir(self.history[self.history_index], False)

    def _handle_go_parent_action(self):
        pathob = Path(self.cur_path)
        path = pathob.parent.absolute()
        self.jump_to_dir(path, True)

    def _handle_go_gome_action(self):
        self.jump_to_dir(os.getenv("HOME"), True)

    def _handle_go_to_action(self):
        self.jump_to_dir(self.dir_path_spinbox.text(), True)

    def _handle_new_window_action(self):
        subprocess.Popen(["pyfm"])

    def _handle_close_window_action(self):
        exit(0)

    def _handle_remove_action(self):
        try:
            remove_all_files([button.path for button in self.highlighted])
            self.files = list_all_files(self.cur_path)
            self._update_main_panel()
        except PermissionError:
            QMessageBox.about(self, "Error", "Unable remove the file due to lack of permissions")

    def _handle_select_all_action(self):
        self._clear_highlighted()
        for i in reversed(range(self.grid_layout.count())): 
            self.manage_highlighted(self.grid_layout.itemAt(i).widget(), True)

    def _handle_reload_folder_action(self):
        self.files = list_all_files(self.cur_path)
        self._update_main_panel()

    def _handle_cut_action(self):
        self.clipboard = copy([button.path for button in self.highlighted])
        self.clipaction = move_all_files

    def _handle_copy_action(self):
        self.clipboard = copy([button.path for button in self.highlighted])
        self.clipaction = copy_all_files

    def _handle_paste_action(self):
        try:
            if len(self.clipboard) > 0:
                self.clipaction(self.clipboard, self.cur_path)
                self.clipboard.clear()
                self.files = list_all_files(self.cur_path)
                self._update_main_panel()
        except PermissionError:
            QMessageBox.about(self, "Error", "Unable to paste the files due to lack of permissions")
        except shutil.Error:
            QMessageBox.about(self, "Error", "Unable to paste, files already exist")

    def _handle_get_prop_action(self):
        try:
            if len(self.highlighted) > 0:
                dlg = PropertiesDialog(self.highlighted[0].path, parent=self)
                dlg.show()
        except PermissionError:
            QMessageBox.about(self, "Error", "Unable to get file properties due to lack of permissions")

    def _handle_new_folder_action(self):
        try:
            text, ok = QInputDialog.getText(self, "folder name input", "Enter new folder name")
            if ok:
                create_directory(os.path.join(self.cur_path, text))
                self.files = list_all_files(self.cur_path)
                self._update_main_panel()
        except PermissionError:
            QMessageBox.about(self, "Error", "Unable to create folder due to lack of permissions")
        except FileExistsError:
            QMessageBox.about(self, "Error", "Unable to create, the folder already exists")

    def _handle_new_file_action(self):
        try:
            text, ok = QInputDialog.getText(self, "folder name input", "Enter new file name")
            if ok:
                create_empty_file(os.path.join(self.cur_path, text))
                self.files = list_all_files(self.cur_path)
                self._update_main_panel()
        except PermissionError:
            QMessageBox.about(self, "Error", "Unable to create file due to lack of permissions")
        except FileExistsError:
            QMessageBox.about(self, "Error", "Unable to create, the file already exists")

    def _handle_rename_action(self):
        try:
            if len(self.highlighted) == 1:
                text, ok = QInputDialog.getText(self, "folder name input", "Enter new file name")
                if ok:
                    rename_file(self.highlighted[0].path, os.path.join(self.cur_path, text))
                    self.files = list_all_files(self.cur_path)
                    self._update_main_panel()
        except PermissionError:
            QMessageBox.about(self, "Error", "Unable to rename the file due to lack of permissions")
        except IsADirectoryError:
            QMessageBox.about(self, "Error", "Unable to rename, directory with that name already exists")

    def _handle_get_cur_prop_action(self):
        try:
            dlg = PropertiesDialog(self.cur_path, parent=self)
            dlg.show()
        except PermissionError:
            QMessageBox.about(self, "Error", "Unable to get file properties due to lack of permissions")
    
    def _handle_open_action(self):
        if len(self.highlighted) == 1:
            if os.path.isdir(self.highlighted[0].path):
                self.jump_to_dir(self.highlighted[0].path, True)
            else:
                subprocess.Popen([TEXT_EDITOR, self.highlighted[0].path])

    def _handle_about_action(self):
        QMessageBox.about(self, "About", "Python file manager\nŁukasz Wala")

    def _create_actions(self):
        self.new_window_action = QAction(QIcon(":add.svg"), "&New Window", self)
        self.new_window_action.triggered.connect(self._handle_new_window_action)
        self.new_window_action.setShortcut("Ctrl+N")
        self.close_window_action = QAction(QIcon(":minus.svg"), "&Close Window")
        self.close_window_action.triggered.connect(self._handle_close_window_action)
        self.close_window_action.setShortcut("Ctrl+Q")
        self.new_folder_action = QAction(QIcon(":folder.svg"), "&Folder", self)
        self.new_folder_action.triggered.connect(self._handle_new_folder_action)
        self.new_folder_action.setShortcut("Shift+Ctrl+N")
        self.new_file_action = QAction(QIcon(":file.svg"), "&File", self)
        self.new_file_action.triggered.connect(self._handle_new_file_action)
        self.new_file_action.setShortcut("Alt+Ctrl+N")

        self.open_action = QAction(QIcon(":add.svg"), "&Open", self)
        self.open_action.triggered.connect(self._handle_open_action);
        self.cut_action = QAction(QIcon(":scissors.svg"), "C&ut", self)
        self.cut_action.triggered.connect(self._handle_cut_action)
        self.cut_action.setShortcut("Ctrl+X")
        self.copy_action = QAction("&Copy", self)
        self.copy_action.triggered.connect(self._handle_copy_action)
        self.copy_action.setShortcut("Ctrl+C")
        self.paste_action = QAction("&Paste", self)
        self.paste_action.triggered.connect(self._handle_paste_action)
        self.paste_action.setShortcut("Ctrl+V")
        self.remove_action = QAction(QIcon(":delete.svg"), "&Remove", self)
        self.remove_action.triggered.connect(self._handle_remove_action)
        self.get_prop_action = QAction("&Properties", self)
        self.get_prop_action.triggered.connect(self._handle_get_prop_action)
        self.get_prop_action.setShortcut("Alt+Return")
        self.rename_action = QAction(QIcon(":edit.svg"), "&Rename", self)
        self.rename_action.triggered.connect(self._handle_rename_action)
        self.rename_action.setShortcut("F2")
        self.select_all_action = QAction("&Select All", self)
        self.select_all_action.triggered.connect(self._handle_select_all_action)
        self.select_all_action.setShortcut("Ctrl+A")

        self.reload_folder_action = QAction(QIcon(":refresh.svg"), "&Reload Folder", self)
        self.reload_folder_action.triggered.connect(self._handle_reload_folder_action)
        self.reload_folder_action.setShortcut("F5")

        self.go_prev_action = QAction(QIcon(":left.svg"), "&Previous Folder", self)
        self.go_prev_action.triggered.connect(self._handle_go_prev_action)
        self.go_prev_action.setShortcut("Alt+Left")
        self.go_next_action = QAction(QIcon(":right.svg"), "&Next Folder", self)
        self.go_next_action.triggered.connect(self._handle_go_next_action)
        self.go_next_action.setShortcut("Alt+Right")
        self.go_parent_action = QAction(QIcon(":down.svg"), "&Parent Folder", self)
        self.go_parent_action.triggered.connect(self._handle_go_parent_action)
        self.go_parent_action.setShortcut("Alt+Up")
        self.go_home_action = QAction(QIcon(":home.svg"), "&Home", self)
        self.go_home_action.triggered.connect(self._handle_go_gome_action)
        self.go_home_action.setShortcut("Alt+Home")

        self.go_to_action = QAction(QIcon(":forward.svg"), "&Go to the path in the location bar", self)
        self.go_to_action.triggered.connect(self._handle_go_to_action)

        self.get_cur_prop_action = QAction("&Folder Properties", self)
        self.get_cur_prop_action.triggered.connect(self._handle_get_cur_prop_action)

    ##### MENU, TOOLBAR, CONTEXT MENU #####

    def _create_menu_bar(self):
        menu_bar = self.menuBar()
        file_menu = menu_bar.addMenu("&File")
        file_menu.addAction(self.new_window_action)
        file_menu.addSeparator()
        create_menu = file_menu.addMenu("&Create")
        create_menu.addAction(self.new_folder_action)
        create_menu.addAction(self.new_file_action)
        file_menu.addSeparator()
        file_menu.addSeparator()
        file_menu.addAction(self.close_window_action)

        edit_menu = menu_bar.addMenu("Edit")
        edit_menu.addAction(self.open_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.cut_action)
        edit_menu.addAction(self.copy_action)
        edit_menu.addAction(self.paste_action)
        edit_menu.addAction(self.remove_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.get_prop_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.rename_action)
        edit_menu.addSeparator()
        edit_menu.addAction(self.select_all_action)

        view_menu = menu_bar.addMenu("&View")
        view_menu.addAction(self.reload_folder_action)

        go_menu = menu_bar.addMenu("&Go")
        go_menu.addAction(self.go_prev_action)
        go_menu.addAction(self.go_next_action)
        go_menu.addAction(self.go_parent_action)
        go_menu.addAction(self.go_home_action)

    def _create_tool_bars(self):
        tool_bar = self.addToolBar("Toolbar")
        tool_bar.setMovable(False)
        tool_bar.addAction(self.go_prev_action)
        tool_bar.addAction(self.go_next_action)
        tool_bar.addAction(self.go_parent_action)
        tool_bar.addAction(self.go_home_action)

        self.dir_path_spinbox = QLineEdit()
        self.dir_path_spinbox.setText(self.cur_path)
        self.dir_path_spinbox.returnPressed.connect(self._handle_go_to_action)
        
        completer = QCompleter(self)
        completer.setModel(QDirModel(completer))
        self.dir_path_spinbox.setCompleter(completer)

        tool_bar.addWidget(self.dir_path_spinbox)

        tool_bar.addAction(self.go_to_action)

    def _create_context_menu(self):
        self.centralWidget.setContextMenuPolicy(Qt.ActionsContextMenu)
        
        separator1 = QAction(self)
        separator1.setSeparator(True)
        separator2 = QAction(self)
        separator2.setSeparator(True)
        separator3 = QAction(self)
        separator3.setSeparator(True)

        self.centralWidget.addAction(self.new_file_action)
        self.centralWidget.addAction(self.new_folder_action)
        self.centralWidget.addAction(separator1)
        self.centralWidget.addAction(self.paste_action)
        self.centralWidget.addAction(separator2)
        self.centralWidget.addAction(self.select_all_action)
        self.centralWidget.addAction(separator3)
        self.centralWidget.addAction(self.get_cur_prop_action)

    ##### STATUS BAR #####

    def _create_status_bar(self):
        self.statusbar = self.statusBar()
        self._get_space_used(True)

    def _get_item_count(self):
        if len(self.highlighted) == 0:
            message = f"{len(self.files)} items"
        elif len(self.highlighted) == 1:
            message = f"\"{self.highlighted[0].path.split(os.sep)[-1]}\" selected"
        else:
            message = f"{len(self.highlighted)} items selected"

        self.statusbar.showMessage(message, 0)

    def _get_space_used(self, iffirst):
        if not iffirst:
            self.statusbar.removeWidget(self.item_count_label)
        total, free = get_part_usage(self.cur_path)
        self.item_count_label = QLabel(f"Free space: {free[0]:.1f} {free[1]} (Total: {total[0]:.1f} {total[1]})")
        self.statusbar.addPermanentWidget(self.item_count_label)

    ##### SIDE PANEL #####

    def _print_dir_tree(self, item):
        if item.was_expanded: return
        item.was_expanded = True
        start_path = item.path
        try:
            for element in os.listdir(start_path):
                path_info = start_path + "/" + element
                if os.path.isdir(path_info):
                    parent_itm = QTreeWidgetItem(item, [os.path.basename(element)])
                    parent_itm.path = path_info
                    parent_itm.setIcon(0, QIcon(":folder.svg"))
                    parent_itm.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
                    parent_itm.was_expanded = False
            
            if len(os.listdir(start_path)) == 0:
                parent_itm = QTreeWidgetItem(item, ["<No subfolders>"])
                parent_itm.path = ""

        except PermissionError:
            parent_itm = QTreeWidgetItem(item, ["<Permissions denied>"])
            parent_itm.path = ""
    
    def _create_side_panel(self):
        self.side_panel = QWidget(self.centralWidget)
        layout = QVBoxLayout()
        self.side_panel.setLayout(layout)


        dir_tree = QTreeWidget(self.side_panel)
        dir_tree.setHeaderLabels(["Directory Tree"])

        def on_item_clicked():
            self.jump_to_dir(dir_tree.selectedItems()[0].path, True)

        dir_tree.doubleClicked.connect(on_item_clicked)
        dir_tree.itemExpanded.connect(self._print_dir_tree)

        home = QTreeWidgetItem(dir_tree, [os.path.basename(os.getenv("HOME"))])
        home.path = os.getenv("HOME")
        home.setIcon(0, QIcon(":folder.svg"))
        home.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        home.was_expanded = False

        root = QTreeWidgetItem(dir_tree, ["/"])
        root.path = "/"
        root.setIcon(0, QIcon(":folder.svg"))
        root.setChildIndicatorPolicy(QTreeWidgetItem.ShowIndicator)
        root.was_expanded = False

        self.side_panel.setMinimumWidth(100)
        self.side_panel.setMaximumWidth(300)
        
        layout.addWidget(dir_tree)

    ##### MAIN PANEL #####

    def _update_main_panel(self):
        for i in reversed(range(self.grid_layout.count())): 
            self.grid_layout.itemAt(i).widget().setParent(None)
        
        for f in self.files:
            file_button = FileButton(f, 60, 60, parent=self)
            self.grid_layout.addWidget(file_button)

        self._clear_highlighted()
        self._get_space_used(False)

    def _create_main_panel(self):
        grid = QWidget()
        grid.mouseReleaseEvent = lambda event: self._clear_highlighted()
        self.grid_layout = FlowLayout()
        grid.setLayout(self.grid_layout)

        self.main_panel = QScrollArea()
        self.main_panel.setWidgetResizable(True)
        self.main_panel.setWidget(grid)

        self._update_main_panel()


def create_color_palette():
    palette = QPalette()
    palette.setColor(QPalette.Window, QColor(53, 53, 53))
    palette.setColor(QPalette.WindowText, Qt.white)
    palette.setColor(QPalette.Base, QColor(25, 25, 25))
    palette.setColor(QPalette.AlternateBase, QColor(53, 53, 53))
    palette.setColor(QPalette.ToolTipBase, Qt.black)
    palette.setColor(QPalette.ToolTipText, Qt.white)
    palette.setColor(QPalette.Text, Qt.white)
    palette.setColor(QPalette.Button, QColor(53, 53, 53))
    palette.setColor(QPalette.ButtonText, Qt.white)
    palette.setColor(QPalette.BrightText, Qt.red)
    palette.setColor(QPalette.Link, QColor(42, 130, 218))
    palette.setColor(QPalette.Highlight, QColor(42, 130, 218))
    palette.setColor(QPalette.HighlightedText, Qt.black)

    return palette

def main():
    app = QApplication(sys.argv)

    app.setPalette(create_color_palette())

    win = Window()
    win.show()
    sys.exit(app.exec_())
