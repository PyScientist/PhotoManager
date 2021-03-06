import sys
import os

import time

from PyQt5.QtCore import QThread

from PyQt5.QtWidgets import QApplication, \
                            QMainWindow, \
                            QFileDialog,\
                            QListWidgetItem, \
                            QDialog, \
                            QMessageBox

from PyQt5.QtCore import QSize, \
                         Qt

from PyQt5.QtGui import QPixmap

from PIL import Image

from PhotoManagerMainwindow import Ui_MainWindow
from FigureListDialog import Ui_Visualise_figure_list_form
from ProgressBarWidget import Ui_ProgressWidget

from threading import Thread


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

    # Dictionary of correspondence of extensions types and extensions
    extension_dict = {'doc file': ['.doc', '.docx'],
                      'xls file': ['.xls', '.xlsx', '.xlsm'],
                      'rar file': ['.rar', '.zip'],
                      'pdf file': ['.pdf'],
                      'pict. file': ['.jpg', '.png', '.tiff', '.tif', '.jpeg', '.bmp'],
                      'txt file': ['.txt'],
                      'csv file': ['.csv'],
                      'exe file': ['.exe', '.bat'],
                      'las file': ['.las'],
                      'dlis file': ['.dlis']}

    def __init__(self, path, parent):
        self.name = 'unknown'
        self.path = path  # Set main folder path attribute
        self.parent = parent  # Set main window link attribute
        self.children_names = []  # This container will include absolute paths
        self.children_container = []  # This container will include objects (instance of FileSystemObject)
        self.folder_path_list = []  # This container will include paths to folders
        self.figure_path_list = [] # This container will include paths to figures
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

        # Call methods forming attributes of instance for rest of the folder levels of main folder
        self.exts()
        self.types()
        self.sizes()
        self.dates()
        self.get_sizes()
        self.get_figure_path_lsit()

        # Count files with different extensions
        self.count_ext_types()

        # Perform quality control for self
        self.quality_control()

    def quality_control(self):
        """Method for quality control of prepared self"""

        # Prepare dictionaries with links to list with file objects parameters
        dict_list = {'children_name': self.children_names,
                     'children_container': self.children_container,
                     'ext_list': self.ext_list,
                     'type_list': self.type_list,
                     'size_list': self.size_list,
                     'date_list': self.date_list}

        error = False  # initially set error flag to False
        error_count = 0  # counter for possible errors
        error_list = []  # list for possible error message

        for key in dict_list:
            if len(dict_list['children_container']) != len(dict_list[key]):
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


    def get_figure_path_lsit(self):
        for object in self.children_container:
            if self.extension_dict['pict. file'].count(object.ext) > 0:
                self.figure_path_list.append(object.path)

    def children(self):

        """Searching for file objects inside main folder"""
        self.children_names = []
        self.children_container = []
        for name in os.listdir(self.path):  # pass through all objects in main folder
            if os.path.exists(F'{self.path}{name}'):
                # Add path to file object in "children_names" attribute
                self.children_names.append(F'{self.path}{name}')
                # Create instance and add it to container
                self.children_container.append(FileSystemObject(F'{self.path}{name}'))
            else:
                # Show warning message if the incorrect path observed
                QMessageBox.warning(self.parent,
                                    "Warning",
                                    F"incorrect path to file or folder {self.path}{name}",
                                    QMessageBox.Ok)

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

    def get_sizes(self):
        """Calculate full, minimal and maximal sizes of files"""
        sum_sizes = 0
        count = 0
        # Calculate full size of files
        for size in self.size_list:
            if size is not None:
                sum_sizes += size
                count += 1
        self.full_size = sum_sizes/1048576
        self.avg_size = (sum_sizes/1048576)/count

        # Calculate minimal and maximal size of files
        sizes = list(self.size_list)
        for x in range(sizes.count(None)):
            try:
                sizes.remove(None)
            except Exception:
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
        """Method which performing search in subfolders of main folderbased on results
           object attributes are supplemented according to the file objects contained in subfolders
           , there is also evaluates the level of folder nesting.
           Add data in following attributes of object FileObjectsSet

           self.children_names - container for path to file system objects
           self.children_container - container for instances of file system objects
           self.folder_list - list of folders in main folder"""

        def cycle_sub_find(folders, folders_new):
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
        cycle_sub_find(folders=self.folder_path_list, folders_new=self.folder_path_list)

        # We search for file objects in all folders have been found
        # (under file objects we understand files and also the folders not taking into account the files inside)
        all_children = []
        for folder in self.folder_path_list:
            children_of_folder = (os.listdir(folder))
            for name in children_of_folder:
                all_children.append(F'{folder}/{name}')

        # We put the path to each file in the list and also put in the container the instances of file system objects
        for abs_path in all_children:
            self.children_names.append(F'{abs_path}')
            self.children_container.append(FileSystemObject(F'{abs_path}'))

    def count_ext_types(self):

        def ext_counter(ext_list, parent):
            """Function for summing the number of files with the same type of extensions
            :param ext_list:
            :param parent:
            :return counter:
            """
            counter = 0
            for ext in ext_list:
                counter += parent.ext_list.count(ext.lower())
            return counter

        # Using the standard "count" method for attribute "type_list"
        # we get the number of files and folders in main folder
        self.voc_types.update({'file': self.type_list.count('file')})
        self.voc_types.update({'folder': self.type_list.count('folder')})
        # Based on the results of counting the number of files with certain extensions, we supplement the dictionary
        self.voc_types.update({'doc file': ext_counter(self.extension_dict['doc file'], self)})
        self.voc_types.update({'xls file': ext_counter(self.extension_dict['xls file'], self)})
        self.voc_types.update({'rar file': ext_counter(self.extension_dict['rar file'], self)})
        self.voc_types.update({'pdf file': ext_counter(self.extension_dict['pdf file'], self)})
        self.voc_types.update({'pict. file': ext_counter(self.extension_dict['pict. file'], self)})
        self.voc_types.update({'txt file': ext_counter(self.extension_dict['txt file'], self)})
        self.voc_types.update({'csv file': ext_counter(self.extension_dict['csv file'], self)})
        self.voc_types.update({'exe file': ext_counter(self.extension_dict['exe file'], self)})
        self.voc_types.update({'las file': ext_counter(self.extension_dict['las file'], self)})
        self.voc_types.update({'dlis file': ext_counter(self.extension_dict['dlis file'], self)})


class FileSystemObject:
    """An object class that represents an empty folder or a file (when creating as the input parameter is given
    absolute path where the object is located).
    Includes attributes:
    path - absolute path where the object is located;
    ext - expansion of the object, in case the folder is given the extensionя расширение '.folder';
    type - object type ['file', 'folder', 'unknown'];
    size - object size (in case of taking into consideration of emty folder ist size is equal zero).
    """

    def __init__(self, path):
        self.path = path
        self.type = 'unknown'
        self.ext = '.unknown'
        # Set date to initially date
        self.date = ''

        # Calling the method to get sizes
        self.get_size()
        # Calling the method to get the types and extensions
        self.get_type_ext()
        # Calling the method to get dates
        self.get_date()

    def get_size(self):
        # Check the correctness of its path (by length <= 256) then find out the file object size if it is not folder,
        if len(self.path) > 256:
            self.size = None
            print(F'Caution!!!! the length of file path {self.path} more than 256 characters')
        else:
            if os.path.isfile(self.path):
                self.size = os.path.getsize(self.path)  # if it is file get the size in bites
            else:
                self.size = None  # if it is folder set size to zero

    def get_type_ext(self):
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


class LasObject():
    pass


class FigureObject():
    """Class of figure object"""
    def __init__(self, path):
        self.path = path
        self.name = None
        self.size = None
        self.date = None
        self.width = None
        self.height = None
        self.includes_name = None
        self.includes_size = None

        self.get_size()
        self.get_date()
        self.get_name()

        try:
            self.get_dimensions()
        except Exception as exception:
            print(F'{exception} some strange dimensions behaviour for {self.path}')


    def get_size(self):
        """Method to get size of the picture"""
        # Check the correctness of its path (by length <= 256) then find out the file object size
        if len(self.path) > 256:
            self.size = None
            print(F'Caution!!!! the length of file path {self.path} more than 256 characters')
        else:
            self.size = os.path.getsize(self.path)  # if it is file get the size in bites

    def get_date(self):
        """Method to get date of last modification of the figure"""
        self.date = os.stat(self.path).st_mtime

    def get_name(self):
        """Method to get name of the figure"""
        _, self.name = os.path.split(self.path)

    def get_dimensions(self):
        """Method to get dimensions (height and width) of the figure"""
        image = Image.open(self.path)
        self.width, self.height = image.size

class FiguresSet():
    def __init__(self, paths, mainwindow):
        self.mainwindow = mainwindow
        self.figure_objects_container = []
        self.two_criteria_similar_figures = []
        self.paths = paths
        self.names = []
        self.sizes = []
        self.includes_name = []
        self.includes_size = []

        print('бл.... готовится к работе')
        self.getFiguresThread = GetFiguresThread(self)
        self.getFiguresThread.start()

        ProgressBarDialog()

        self.getFiguresThread.finished.connect(self.fff)

        print('Работает бл...')

    def fff(self):
        print('fff')


class GetFiguresThread(QThread):
    def __init__(self, figures_set):
        super().__init__()
        self.paths = figures_set.paths
        self.names = figures_set.names
        self.sizes = figures_set.sizes
        self.figure_objects_container = figures_set.figure_objects_container



    def run(self):
        start_time = time.time()
        count_elem = 0
        for path in self.paths:
            count_elem += 1
            self.figure_objects_container.append(FigureObject(path))
            print(F'Performed {count_elem/len(self.paths)*100} percent of calculation')
        complete_time = time.time()
        print(complete_time-start_time)

        for fig_obj in self.figure_objects_container:
            self.names.append(fig_obj.name)
            self.sizes.append(fig_obj.size)


class ProgressBarDialog(QDialog, Ui_ProgressWidget):
    def __init__(self):
        super().__init__()
        self.setupUi(self)
        print('here')
        self.show()
        self.exec_()


class FigureListDialog(QDialog, Ui_Visualise_figure_list_form):
    """Class inherited from "QDialog" provides dialog which shows figure list
    and allows to do some manipulation with them
    """
    def __init__(self, figures, parent):
        super().__init__()
        self.setupUi(self)

        self.mainwindow = parent
        self.figures_paths = figures
        self.figure_sets = []
        self.fig_set_to_operate = 0
        self.duplicate_plotted = False

        # Create initial list of figures
        initial_fig_set = FiguresSet(self.figures_paths, self.mainwindow)

        self.figure_sets.append(initial_fig_set)
        # Put the objects into QListWidget
        self.list_widget_figures.clear()
        for path in self.figure_sets[self.fig_set_to_operate].paths:
            add_element_in_q_list_widget(self.list_widget_figures, path)

        # Adjust the connect method for button which shows probably duplicated figures
        self.show_dupicate_figures_button.clicked.connect(self.show_duplicate_figures)

        # Adjust buttonBox buttons connects
        self.buttonBox.accepted.connect(self.accept)
        self.buttonBox.rejected.connect(self.reject)

        # Prepare Figure and put it in QLabel at the right
        pixmap = QPixmap(self.figure_sets[self.fig_set_to_operate].paths[0]).scaled(QSize(400, 400), Qt.KeepAspectRatio)
        self.label_for_figure_show.setPixmap(pixmap)

        # Show what method we want to launch if itemActivated signal emitted from list widget
        self.list_widget_figures.itemActivated.connect(self.redraw_pixmap)

        # Resize Dialog dimensions according to Desktop properties
        self.resize(QApplication.desktop().width()/3, QApplication.desktop().height()/2)

        # Plot initial message in stat field
        self.Statistics_Field.setText(F'Figures quantity is: {len(self.figure_sets[0].figure_objects_container)}')

        # Show dialog and waiting for reply
        self.show()
        if self.exec_() == QDialog.Accepted:
            self.result = 'Оk'

    def redraw_pixmap(self):
        """Method for redraw Pixmap on the Label if was selected another item in list widget"""
        row_selected = self.list_widget_figures.row(self.list_widget_figures.selectedItems()[0])

        if self.duplicate_plotted:
            FigSet_similar = self.figure_sets[self.fig_set_to_operate].two_criteria_similar_figures
            fig_obj = FigSet_similar[row_selected]
        else:
            FigSet = self.figure_sets[self.fig_set_to_operate]
            fig_obj = FigSet.figure_objects_container[row_selected]

        pixmap = QPixmap(fig_obj.path).scaled(QSize(400, 400), Qt.KeepAspectRatio)
        self.label_for_figure_show.setPixmap(pixmap)
        self.Statistics_Field.setText(F'Figure path: {fig_obj.path}')
        self.Statistics_Field.append(F'Figure Name: {fig_obj.name}')
        self.Statistics_Field.append(F'Figure size: {fig_obj.size/1048576} MB')
        self.Statistics_Field.append(F'Figure dimensions (width x height): {fig_obj.width} x {fig_obj.height}')
        self.Statistics_Field.append(F'Similarity ("similiar name" x "similiar size"):'
                                     F' {fig_obj.includes_name} x {fig_obj.includes_size}')

    def show_duplicate_figures(self):
        """Method to highlight figure which probably have a duplicates"""
        names = []
        sizes = []
        figure_set = []

        # Get link to appropriate figure set 
        FigSet = self.figure_sets[self.fig_set_to_operate]

        # Get count of identical file names
        for iterable in enumerate(FigSet.names):
            FigSet.includes_name.append(FigSet.names.count(iterable[1]))
            FigSet.figure_objects_container[iterable[0]].includes_name = FigSet.names.count(iterable[1])

        # Get count of identical sizes
        for iterable in enumerate(FigSet.sizes):
            FigSet.includes_size.append(FigSet.sizes.count(iterable[1]))
            FigSet.figure_objects_container[iterable[0]].includes_size = FigSet.sizes.count(iterable[1])
            
        zipped = list(zip(FigSet.includes_name, FigSet.includes_size, FigSet.names, FigSet.sizes, FigSet.figure_objects_container))

        FigSet.two_criteria_similar_figures = []
        for row in enumerate(zipped):
            if row[1][0] > 1 and row[1][1] > 1:
                FigSet.two_criteria_similar_figures.append(FigSet.figure_objects_container[row[0]])

        # Clear list widget and plot there all path to figures which may be duplicated
        self.list_widget_figures.clear()
        for obj in FigSet.two_criteria_similar_figures:
            add_element_in_q_list_widget(self.list_widget_figures, obj.path)

        # Plot message in stat field
        self.Statistics_Field.setText(F'Found {len(FigSet.two_criteria_similar_figures)} probably duplicated figures')

        # Set flag if method performed
        self.duplicate_plotted = True


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
        self.lineEdit_for_dir_name.setText('c:/Python36/Scripts/PhotoManager/test_figures/')

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
                                        F' файла и {file_objects_set.voc_types["folder"]} папки')
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

    def find_figures(self):

        # Make link to System Objects Set with compliance of number of its set in spinbox
        file_objects_set = self.objects_sets_container[self.set_to_print]

        # Create dialog which shows list of figures in main folder and can do some stat
        dialog = FigureListDialog(file_objects_set.figure_path_list, self)
        del dialog

if __name__ == '__main__':
    main_application()
