import sys
import os
import time
from PyQt5.QtWidgets import QApplication, \
    QMainWindow, \
    QFileDialog,\
    QListWidgetItem, \
    QListWidget, \
    QDialog, \
    QVBoxLayout, \
    QLabel, \
    QDialogButtonBox, \
    QMessageBox
from PyQt5.QtCore import Qt
from PhotoManagerMainwindow import Ui_MainWindow


def main_application():
    """Entry point for program"""
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


def filter_unique(spisok):
    """Get unique values from list
    """
    spisok_uniq = []
    for x in range(0, len(spisok)):
        if spisok_uniq.count(spisok[x]) < 1:
            spisok_uniq.append(spisok[x])
    return spisok_uniq


def add_element_in_q_list_widget(list_widget, element):
    """Function which add item in list "QListWidget" the function obtains
    "item" and "QListWidget" instance where it is need to add "item"
    """
    item = QListWidgetItem()  # Create instance of list item for QListWidget
    item.setText(element)  # Set text for QListWidgetItem instance
    list_widget.addItem(item)  # Adding QListWidgetItem instance into the QListWidget


class FileObjectsSet:
    """Class of file-system objects set (files and folders) have a folder path,
     which have given to him while initialization by this path all objects inside collecting
     There is also link to application main window provided while instating"""
    def __init__(self, path, parent):
        self.name = 'unknown'
        self.path = path  # Set main folder path attribute
        self.parent = parent  # Set main window link attribute
        self.children_names = []  # This container will include absolute paths
        self.children_container = []  # This container will include objects (instance of FileSystemObject)
        self.folder_path_list = []  # This container will include paths to folders
        self.ext_list = []
        self.type_list = []
        self.size_list = []
        self.full_size = 0
        self.avg_size = None
        self.size_minimal = None
        self.size_maximal = None
        self.date_list = []
        self.voc_types = {}
        self.depth_of_folder = 0  # Set the depth of nesting

        # Call methods forming attributes of instance for first level of folder
        self.children()

        self.exts()
        self.types()

        # Call method for forming full list of files and folders
        self.create_initial_folder_list()
        self.search_subfolders_and_files_in_them()

        # Call methods forming attributes of instance for rest of the levels of folder
        self.exts()
        self.types()
        self.sizes()
        self.dates()
        self.get_sizes()

        # Count files with different extensions
        self.count_ext_types()

        # Perform quality control for self
        self.quality_control()

    def quality_control(self):
        """Method for quality control of prepared self"""

        # Prepare dictionaries with links to list with file objects parameters
        dict = {'children_name': self.children_names,
                'children_container': self.children_container,
                'ext_list': self.ext_list,
                'type_list': self.type_list,
                'size_list': self.size_list,
                'date_list': self.date_list}

        error = False  # initially set error flag to False
        error_count = 0  # counter for possible errors
        error_list = []  # list for possible error message

        for key in dict:
            if len(dict['children_container']) != len(dict[key]):
                error = True
                error_count += 1
                error_list.append(F'Something wrong with length of list {[key]}')
        if error:
            QMessageBox.warning(self.parent,
                                "Warning",
                                str(error_list),
                                QMessageBox.Ok,
                                QMessageBox.Ok)
        else:
            print('prepared nice object! The quantity of elements of list within object matches to each other')

    def children(self):

        """Searching for file objects inside main folder"""
        self.children_names = []
        self.children_container = []
        for name in os.listdir(self.path): #pass through all objects in main folder
            if os.path.exists(F'{self.path}{name}'):
                self.children_names.append(F'{self.path}{name}') #add path to file object in "children_names" attribute
                self.children_container.append(FileSystemObject(F'{self.path}{name}')) #Create instance and add it to container
            else:
                # Show warning message if the incorrect path observed
                QMessageBox.warning(self.parent, "Warning", F"incorrect path to file or folder {self.path}{name}", QMessageBox.Ok)

    def exts(self):
        """Extension list creation according objects in "children_container" attribute"""
        self.ext_list = []
        for obj in self.children_container:
            self.ext_list.append(obj.ext)

    def types(self):
        """Types list creation according objects in "children_container" attribute"""
        self.type_list = []
        for obj in self.children_container:
            self.type_list.append(obj.type)

    def sizes(self):
        """Types list creation according objects in "children_container" attribute"""
        self.size_list = []
        for obj in self.children_container:
            self.size_list.append(obj.size)

    def dates(self):
        """Dates of creation list creation according objects in "children_container" attribute"""
        self.date_list = []
        for obj in self.children_container:
            self.date_list.append(obj.date)
        print(self.date_list)

    def get_sizes(self):
        """Calculate full, minimal and maximal sizes of files"""
        sum = 0
        count = 0
        # Calculate full size of files
        for size in self.size_list:
            if size is not None:
                sum += size
                count += 1
        self.full_size = sum/1048576
        self.avg_size = (sum/1048576)/count

        # Calculate minimal and maximal size of files
        sizes = list(self.size_list)
        for x in range(sizes.count(None)):
            try:
                sizes.remove(None)
            except:
                pass
        self.size_maximal = max(sizes)/1048576
        self.size_minimal = min(sizes)/1048576
        del sizes

    def create_initial_folder_list(self):
        """Create a folder list"""
        self.folder_path_list = []
        for obj in self.children_container:
            if obj.type == 'folder':
                self.folder_path_list.append(obj.path)

    def search_subfolders_and_files_in_them(self):
        """Метод выполняющий поиск в подпапках основной папки, по результатам работы
         атрибуты объекта дополняются в соответствии с содержащимися в подпапках файловыми объектами
         , оценивается уровень вложенности папок.

         Add data in following attributes of object FileObjectsSet

         self.children_names -
         self.children_container
         self.folder_list
        """

        def cycle_sub_find(folders, folders_new):
            temp_children = []
            temp_folders = []
            # Initially we have the list of folders which have been stored in main folder (folders)
            for curr_folder in folders:  # Go through folders
                curr_children_of_folder = (os.listdir(curr_folder))  # For each folder get list of content
                for cur_name in curr_children_of_folder:  # Go through content of folder for each folder
                    if os.path.isdir(F'{curr_folder}/{cur_name}'):
                        temp_folders.append(F'{curr_folder}/{cur_name}')

            # This way at the finish of the operation we have list of all objects stored in first level folders
            # including subfolders.
            folders_new.extend(temp_folders)

            # If after viewing there are subfolders exists and the
            # viewing depth is less than 100, recursively launch the function
            if len(temp_folders) > 0 and self.depth_of_folder < 100:
                self.depth_of_folder = self.depth_of_folder+1
                # Recursively running the function inside itself
                cycle_sub_find(folders=temp_folders, folders_new=folders_new)

        # Running the recursive folder search function
        print(self.folder_path_list)
        cycle_sub_find(folders=self.folder_path_list, folders_new=self.folder_path_list)

        # По всем найденным папкам ищем файловые объекты (под файловыми объектами понимаем как непосредственно файлы,
        # так и папки как таковые без содержимого)
        all_children = []
        for folder in self.folder_path_list:
            children_of_folder = (os.listdir(folder))
            for name in children_of_folder:
                all_children.append(F'{folder}/{name}')

        # Путь к каждому файлу включаем в список и создаем объект, помещаем в контейнер объектов файловой системы
        for abs_path in all_children:
            self.children_names.append(F'{abs_path}')
            self.children_container.append(FileSystemObject(F'{abs_path}'))

    def count_ext_types(self):

        def ext_counter(ext_list, parent):
            """Функция для суммирования колличества файлов с однотипными расширениями
            :param ext_list:
            :param parent:
            :return counter:
            """
            counter = 0
            for ext in ext_list:
                counter += parent.ext_list.count(ext.lower())
            return counter

        # С помощью стандартного метода count получаем колличество файлов и папок в атрибуте "type_list"
        # представляющем из себя словарь, добавляем результат в словарь колличества файлов определенного типа
        self.voc_types.update({'file': self.type_list.count('file')})
        self.voc_types.update({'folder': self.type_list.count('folder')})

        # Считаем сколько файлов и с какими расширениями есть в каталоге
        # По результатам подсчета колличества файлов с определенными расширениями дополняем словарь
        doc_ext = ['.doc', '.docx']
        self.voc_types.update({'doc file': ext_counter(doc_ext, self)})
        excel_ext = ['.xls', '.xlsx', '.xlsm']
        self.voc_types.update({'xls file': ext_counter(excel_ext, self)})
        rar_ext = ['.rar', '.zip']
        self.voc_types.update({'rar file': ext_counter(rar_ext, self)})
        pdf_ext = ['.pdf']
        self.voc_types.update({'pdf file': ext_counter(pdf_ext, self)})
        pict_ext = ['jpg.', 'png.', 'tiff.', 'tif.', 'jpeg.', 'bmp.']
        self.voc_types.update({'pict. file': ext_counter(pict_ext, self)})
        txt_ext = ['.txt']
        self.voc_types.update({'txt file': ext_counter(txt_ext, self)})
        csv_ext = ['.csv']
        self.voc_types.update({'csv file': ext_counter(csv_ext, self)})
        exe_ext = ['.exe', '.bat']
        self.voc_types.update({'exe file': ext_counter(exe_ext, self)})
        las_ext = ['.las']
        self.voc_types.update({'las file': ext_counter(las_ext, self)})
        dlis_ext = ['.dlis']
        self.voc_types.update({'dlis file': ext_counter(dlis_ext, self)})


class FileSystemObject:
    """Класс объекта представляющий собой папку или файл (при создании на вход подается
    абсолютный путь по которому находится объект).
    Содержит атрибуты:
    path - абсолютный путь по которому находится объект;
    ext - расширение объекта, в случае папки присваивается расширение '.folder';
    type - тип объекта [file, folder, unknown];
    size - размер объекта (как ведеь себя в случае папки?).
    """

    def __init__(self, path):
        self.path = path
        self.type = 'unknown'
        self.ext = '.unknown'


        # Check the correctness of its path (by length <= 256) then find out the file object size if it is not folder,
        if len(path) > 256:
            self.size = None
            print('Caution!!!! the length of file path more than 256 characters')
        else:
            if os.path.isfile(self.path):
                self.size = os.path.getsize(self.path)  # if it is file get the size in bites
            else:
                self.size = None  # if it is folder set size to zero

        # Set date to initialy date
        self.date = ''

        # Вызываем метод с помощью которого получаем тип и расширение
        self.get_type_ext_findout()
        # Вызываем метод с помощью которого получаем время последнего доступа к файлу
        self.get_date()

    def get_type_ext_findout(self):
        """The method assigns to attributes "type" and "ext" the values have been obtained as a result of processing
        absolute path to the file
        :return: void
        """
        if os.path.isdir(self.path):
            self.type = 'folder'
            self.ext = '.folder'
        elif os.path.isfile(self.path):
            self.type = 'file'
            self.ext = os.path.splitext(self.path)[1]

    def get_date(self):
        """The method assigns to attributes "date" the values have been obtained as a result of processing
        absolute path to the file
        :return: void
        """
        self.date = os.stat(self.path).st_mtime
        # print(time.ctime(os.stat(self.path).st_mtime))
        '''Выполните системный вызов stat () по данному пути. Возвращаемое значение - это объект, атрибуты 
        которого соответствуют членам структуры stat, а именно: st_mode (бит защиты), st_ino (номер inode),
        st_dev (устройство), st_nlink (количество жестких ссылок), st_uid (идентификатор пользователя владельца ), 
        st_gid (идентификатор группы владельца), st_size (размер файла, в байтах), st_atime (время последнего доступа),
        st_mtime (время последней модификации контента), st_ctime (зависит от платформы, время изменения последних метаданных
        в Unix или время создания в Windows):'''


class FigureListDialog(QDialog):
    """Class of dialog which sows figure list
    inherited from QDialog
    """
    def __init__(self, figures):
        super().__init__()

        self.setWindowTitle("Visualise figure list")
        self.setModal(True)
        self.layout = QVBoxLayout()
        self.label = QLabel('The figures list')
        self.layout.addWidget(self.label)
        self.list_widget = QListWidget()

        # Put the objects into QListWidget
        self.list_widget.clear()

        figures = filter_unique(figures)

        for obj in figures:
            add_element_in_q_list_widget(self.list_widget, obj)

        self.layout.addWidget(self.list_widget)

        self.button_box = QDialogButtonBox(QDialogButtonBox.Ok | QDialogButtonBox.Cancel, parent=self)
        self.button_box.accepted.connect(self.accept)
        self.button_box.rejected.connect(self.reject)

        self.layout.addWidget(self.button_box)

        self.setFixedSize(700, 900)

        self.setLayout(self.layout)

        self.show()
        if self.exec_() == QDialog.Accepted:
            self.result = 'Оk'


class MainWindow(QMainWindow, Ui_MainWindow):
    """Class of application main window with methods of data processing
    """
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        # Launch adjustments for Application widgets
        self.set_to_print = 0
        self.adjust_widgets()
        self.objects_sets_container = []  # Container for objects sets

    def adjust_widgets(self):
        """Method adjusts work of Application main window widgets
        :return: void
        """
        self.toolButton_choose_dir.clicked.connect(self.folder_dialog)  # Button to choose path to folder
        self.toolButton_create_files_set_object.clicked.connect(self.create_objects_set)  # Button to obtain file set
        self.toolButton_plot_files_set_object.clicked.connect(self.put_file_list_and_stat)  # Button to plot stat

        self.spinBox_of_file_object.setValue(self.set_to_print)
        self.spinBox_of_file_object.valueChanged.connect(self.spinBox_of_file_object_value_changed)


        self.lineEdit_for_dir_name.setToolTip('Set folder path here!')
        self.lineEdit_for_dir_name.setText('./')
        # self.lineEdit_for_dir_name.setText('Z:/GeolResearch/_INTERNAL_/Отдел ОПМ/+Geolog Projects/West_Qurna-2/')

        self.toolButton_find_figures.clicked.connect(self.find_figures)

    def folder_dialog(self):
        """Method calls dialog for path to directory which need to analyse choosing
        :return: void
        """
        dialog_name = 'Please choose some folder to analyse'
        folder_name = QFileDialog.getExistingDirectory(QFileDialog(), dialog_name, '-')
        self.lineEdit_for_dir_name.setText(F'{folder_name}/')

    def create_objects_set(self):
        """Method for set of objects creation"""
        # Processing exceptions while object creation (FileObjectsSet)
        try:
            file_objects_set = FileObjectsSet(self.lineEdit_for_dir_name.text(), self)
            file_objects_set_validate = 'Created'
        except Exception:
            if len(self.lineEdit_for_dir_name.text()) == 0:
                QMessageBox.warning(self, "Warning", "File path is empty, please enter correct path to folder",
                                    QMessageBox.Ok)
            else:
                QMessageBox.warning(self, "Warning", "Something going wrong", QMessageBox.Ok)
            file_objects_set_validate = 'Error!'

        # If the (FileObjectsSet) instance was created successfully perform next action
        if file_objects_set_validate == 'Error!':
            QMessageBox.warning(self, "Warning", "The FileObjectsSet instance was not created", QMessageBox.Ok)
        else:
            self.objects_sets_container.append(file_objects_set)

    def put_file_list_and_stat(self):
        """Method launches the processing, puts list of objects of selected directory in QListWidget, puts results of
        analysis into QTextEdit widget
        :return: void
        """
        file_objects_set = self.objects_sets_container[self.set_to_print]

        # Put the list of file-system objects into QListWidget
        self.listWidget_for_files.clear()
        for file in file_objects_set.children_names:
            add_element_in_q_list_widget(self.listWidget_for_files, file)

        # Print the results of analysis into QTextEdit widget
        self.textEdit_for_report.setText('')
        self.textEdit_for_report.setText(F'Всего в дирректории {len(file_objects_set.children_names)} объекта')
        self.textEdit_for_report.append(F'из них {file_objects_set.voc_types["file"]}'
                                        F'файла и {file_objects_set.voc_types["folder"]} папки')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["xls file"]} excel файла')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["doc file"]} word документа')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["rar file"]} файла архива')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["pict. file"]} файла рисунка')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["pdf file"]} файла pdf')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["txt file"]} файла txt')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["csv file"]} файла csv')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["exe file"]} файла exe')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["las file"]} файла las')
        self.textEdit_for_report.append(F'{file_objects_set.voc_types["dlis file"]} файла dlis')
        self.textEdit_for_report.append(F'минимальный размер файла: {file_objects_set.size_minimal} МБ')
        self.textEdit_for_report.append(F'максимальный размер файла: {file_objects_set.size_maximal} МБ')
        self.textEdit_for_report.append(F'суммарный размер файлов: {file_objects_set.full_size} МБ')
        self.textEdit_for_report.append(F'средний размер файла: {file_objects_set.avg_size} МБ')
        self.textEdit_for_report.append(F'Глубина вложенности папок: {file_objects_set.depth_of_folder}')

    def spinBox_of_file_object_value_changed(self):
        self.set_to_print = self.spinBox_of_file_object.value()
        if self.set_to_print > len(self.objects_sets_container)-1:
           self.spinBox_of_file_object.setValue(len(self.objects_sets_container)-1)
        print(self.set_to_print)

    def find_figures(self):
        file_objects_set = self.objects_sets_container[self.set_to_print]




        dialog = FigureListDialog(file_objects_set.ext_list)
        del dialog
        print('successfully clicked')


if __name__ == '__main__':
    main_application()
