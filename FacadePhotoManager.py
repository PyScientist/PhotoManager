import sys
import os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from PyQt5.QtCore import Qt
from PhotoManagerMainwindow import Ui_MainWindow


def add_element_in_q_list_widget(list_widget, element):
    """Function which add item in list "QListWidget" the function obtains
    "item" and "QListWidget" instance where it is need to add "item"
    """
    item = QListWidgetItem()  # Create instance of list item for QListWidget
    item.setCheckState(Qt.Checked)  # Adding "checkbox"  for QListWidgetItem instance and set it checked
    item.setText(element)  # Set text for QListWidgetItem instance
    list_widget.addItem(item)  # Adding QListWidgetItem instance into the QListWidget


class MainWindow(QMainWindow, Ui_MainWindow):
    """Class of application main window with methods of data processing
    """
    def __init__(self):
        QMainWindow.__init__(self, parent=None, flags=Qt.WindowFlags())
        self.setupUi(self)
        # Launch adjustments for Application widgets
        self.adjust_widgets()
        self.objects_set = []

    def adjust_widgets(self):
        """Method adjusts work of Application main window widgets
        :return: void
        """
        self.toolButton_choose_dir.clicked.connect(self.folder_dialog)
        self.toolButton_load_files.clicked.connect(self.get_file_list_and_stat)
        self.lineEdit_for_dir_name.setToolTip('Set folder path here!')

    def folder_dialog(self):
        """Method calls dialog for path to directory which need to analyse choosing
        :return: void
        """
        dialog_name = 'Please choose some folder to analyse'
        folder_name = QFileDialog.getExistingDirectory(QFileDialog(), dialog_name, '-', None, None)
        self.lineEdit_for_dir_name.setText(F'{folder_name}/')

    def get_file_list_and_stat(self):
        """Method launch the processing, puts list of objects of selected directory in QListWidget, puts results of
        analysis into QTextEdit widget
        :return: void
        """

        file_objects_set = FileObjectsSet(self.lineEdit_for_dir_name.text())

        self.objects_set.append(file_objects_set)

        # Put the list of file objects into QListWidget
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
        self.textEdit_for_report.append(F'минимальный размер файла: {min(file_objects_set.size_list)/1048576} МБ')
        self.textEdit_for_report.append(F'максимальный размер файла: {max(file_objects_set.size_list)/1048576} МБ')
        self.textEdit_for_report.append(F'суммарный размер файлов: {file_objects_set.full_size/1048576} МБ')
        self.textEdit_for_report.append(F'Глубина вложенности: {file_objects_set.depth_of_folder}')

        print(file_objects_set.search_subfolders_and_files_in_them.__doc__)


class FileObjectsSet:
    """Класс набора объектов (файлов и папок) имеет путь папки, который передается ему при инстанцировании
    """
    def __init__(self, path):
        self.name = 'unknown'
        self.path = path
        self.children_names = []
        self.children_container = []
        self.folder_list = []
        self.ext_list = []
        self.type_list = []
        self.size_list = []
        self.full_size = 0
        self.date_list = []
        self.voc_types = {}
        self.depth_of_folder = 0

        # Вызываемм методы формирующщие экземпляр класса
        self.children()
        self.exts()
        self.types()

        self.create_folder_list()
        self.search_subfolders_and_files_in_them()

        self.exts()
        self.types()
        self.sizes()
        self.dates()
        self.summ_size()

        self.count_ext_types()

    def children(self):
        self.children_names = []
        for name in os.listdir(self.path):
            self.children_names.append(F'{self.path}{name}')
        self.children_container = []
        for obj in os.listdir(self.path):
            self.children_container.append(FileSystemObject(F'{self.path}{obj}'))

    def exts(self):
        self.ext_list = []
        for obj in self.children_container:
            self.ext_list.append(obj.ext)

    def types(self):
        self.type_list = []
        for obj in self.children_container:
            self.type_list.append(obj.type)

    def sizes(self):
        self.size_list = []
        for obj in self.children_container:
            self.size_list.append(obj.size)

    def dates(self):
        self.date_list = []
        for obj in self.children_container:
            self.date_list.append(obj.date)

    def summ_size(self):
        summ = 0

        for size in self.size_list:
            summ += size
        self.full_size = summ

    def create_folder_list(self):
        self.folder_list = []
        for obj in self.children_container:
            if obj.type == 'folder':
                self.folder_list.append(obj.path)

    def search_subfolders_and_files_in_them(self):
        """Метод выполняющий поиск в подпапках основной папки, по результатам работы
         атрибуты объекта дополняются в соответствии с содержащимися в подпапках файловыми объектами
         , оценивается уровень вложенности папок.

         добавляет данные в следующие атрибуты объекта FileObjectsSet

         self.children_names -
         self.children_container
         self.folder_list
        """

        def cycle_sub_find(folders, folders_new):
            temp_children = []
            temp_folders = []
            for curr_folder in folders:
                curr_children_of_folder = (os.listdir(curr_folder))
                for cur_name in curr_children_of_folder:
                    temp_children.append(F'{curr_folder}/{cur_name}')

            # Перебираем список с путями к файловым объектоам
            for child_path in temp_children:
                # Если объект по указанном пути является папкой, то добавляем ее в список
                if os.path.isdir(child_path):
                    temp_folders.append(child_path)
                    folders_new.append(child_path)

            if len(temp_folders) > 0 and self.depth_of_folder:
                print(self.depth_of_folder)
                self.depth_of_folder = self.depth_of_folder+1
                # Рекурсивно запускаем функцию внутри самой себя
                cycle_sub_find(folders=temp_folders, folders_new=folders_new)

        # Запускаем рекурсивную функцию поиска папок
        cycle_sub_find(folders=self.folder_list, folders_new=self.folder_list)

        # По всем найденным папкам ищем файловые объекты (под файловыми объектами понимаем как непосредственно файлы,
        # так и папки как таковые без содержимого)
        all_children = []
        for folder in self.folder_list:
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

        # Узнаем размер файла, также проверяем корректность его пути (на длинну)
        if len(path) > 256:
            self.size = 0
            print('Caution!!!! the length of file path more than 256 characters')
        else:
            self.size = os.path.getsize(self.path)
        self.date = ''

        # Вызываем метод с помощью которого получаем тип и расширение
        self.type_ext_findout()

    def type_ext_findout(self):
        """Метод присваивает в атрибуты "type" и "ext" класса значения полученные в результате обработки
        абсолютного пути к файлу, возвращает None как результат корректной работы
        :return: void
        """
        if os.path.isdir(self.path):
            self.type = 'folder'
            self.ext = '.folder'
        elif os.path.isfile(self.path):
            self.type = 'file'
            self.ext = os.path.splitext(self.path)[1]


def main_application():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())


if __name__ == '__main__':
    main_application()
