import sys, os
from PyQt5.QtWidgets import QApplication, QMainWindow, QFileDialog, QListWidgetItem
from PyQt5.QtCore import Qt
from PhotoManagerMainwindow import Ui_MainWindow


def add_element_in_QListWidget(list_widget, element):
    """
    Функцция которая добавляет элемент в список на вход подается элемент и список в который он добавляется
    """
    item = QListWidgetItem()  # Создаем объект элемента списка QListWidget
    item.setCheckState(Qt.Checked)  # Добавляем chekbox для объекта QListWigetItem и делаеи его выделенным
    item.setText(element)  # Устанавливаем текст в элемент
    list_widget.addItem(item)  # Добавляем элемент в список QListWidget

class MainWindow(QMainWindow, Ui_MainWindow):
    '''
    Класс основного окна приложения с методами для запуска обработки данных
    '''
    def __init__(self):
        QMainWindow.__init__(self)
        self.setupUi(self)
        self.adjust_widgets()
        self.objects_set = []

    def adjust_widgets(self):
        '''
        Метод настраивает работу виджетов основного окна
        :return: void
        '''
        self.toolButton_choose_dir.clicked.connect(self.folder_dialog)
        self.toolButton_load_files.clicked.connect(self.get_file_list_and_stat)
        self.lineEdit_for_dir_name.setText('c:/Users/Сергей/Documents/main/+Работа/+corantine 2020/')

    def folder_dialog(self):
        '''
        Метод вызывает диалог для выбора пути к дерркитории, которую необходимо проанализировать
        :return: void
        '''
        dialog_name = 'Please choose some folder to open'
        folder_init_name = 'c:/Users/Сергей/Documents/main/+Работа/+corantine 2020/'
        foldername = QFileDialog.getExistingDirectory(self, dialog_name, folder_init_name)
        self.lineEdit_for_dir_name.setText(F'{foldername}/')

    def get_file_list_and_stat(self):
        '''
        Метод помещает список объектов выбранной дирректории в QListWidget, а такжже проводит их анализ
        выводит результат в QTextEdit
        :return: void
        '''

        object_set = ObjectSet(self.lineEdit_for_dir_name.text())

        self.objects_set.append(object_set)

        # Помещаем список файлов в QListWidget

        self.listWidget_for_files.clear()
        for file in object_set.children_names:
            add_element_in_QListWidget(self.listWidget_for_files, file)

        self.textEdit_for_report.setText('')
        self.textEdit_for_report.setText(F'Всего в дирректории {len(object_set.children_names)} объекта')
        self.textEdit_for_report.append(F'из них {object_set.voc_types["file"]} файла и {object_set.voc_types["folder"]} папки')
        self.textEdit_for_report.append(F'{object_set.voc_types["xls file"]} excel файла')
        self.textEdit_for_report.append(F'{object_set.voc_types["doc file"]} word документа')
        self.textEdit_for_report.append(F'{object_set.voc_types["rar file"]} файла архива')
        self.textEdit_for_report.append(F'{object_set.voc_types["pict. file"]} файла рисунка')
        self.textEdit_for_report.append(F'{object_set.voc_types["pdf file"]} файла pdf')
        self.textEdit_for_report.append(F'{object_set.voc_types["txt file"]} файла txt')
        self.textEdit_for_report.append(F'{object_set.voc_types["csv file"]} файла csv')
        self.textEdit_for_report.append(F'{object_set.voc_types["exe file"]} файла exe')
        self.textEdit_for_report.append(F'{object_set.voc_types["las file"]} файла las')
        self.textEdit_for_report.append(F'{object_set.voc_types["dlis file"]} файла dlis')
        self.textEdit_for_report.append(F'минимальный размер файла: {min(object_set.size_list)/1048576} МБ')
        self.textEdit_for_report.append(F'максимальный размер файла: {max(object_set.size_list)/1048576} МБ')
        self.textEdit_for_report.append(F'суммарный размер файлов: {object_set.full_size/1048576} МБ')
        self.textEdit_for_report.append(F'Глубина вложенности: {object_set.depth_of_folder}')

        del object_set

class General:
    def __init__(self, path):
        self.general_path
        self.folder_list = 1

class ObjectSet:
    '''
    Класс набора объектов (файлов и папок) имеет путь папки, который передается ему при инстанцировании
    '''
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
            self.children_container.append(Object(F'{self.path}{obj}'))

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

        def cycle_sub_find(self, folders, folders_new):
            temp_children = []
            temp_folders = []
            for folder in folders:
                children_of_folder = (os.listdir(folder))
                for name in children_of_folder:
                    temp_children.append(F'{folder}/{name}')

            for child in temp_children:
                if os.path.isdir(child):
                    temp_folders.append(child)
                    folders_new.append(child)

            if len(temp_folders) > 0 and self.depth_of_folder < 12:
               print(self.depth_of_folder)
               self.depth_of_folder = self.depth_of_folder+1
               cycle_sub_find(self = self, folders = temp_folders, folders_new = folders_new)

        # Запускаем рекурсивную функцию поиска папок
        cycle_sub_find(self, folders = self.folder_list, folders_new = self.folder_list)

        # По всем найденным папкам ищим файлы и вложенные папки
        all_children = []
        for folder in self.folder_list:
            children_of_folder = (os.listdir(folder))
            for name in children_of_folder:
                all_children.append(F'{folder}/{name}')

        # Путь к каждому файлу включаем в список и создаем объект, который помещаем в контейнер
        for name in all_children:
            self.children_names.append(F'{name}')
            self.children_container.append(Object(F'{name}'))

    def count_ext_types(self):

        def ext_counter(ext_list, self):
            'функция для суммирования колличества файлов с однотипными рас'
            counter = 0
            for ext in ext_list:
                counter += self.ext_list.count(ext.lower())
            return counter

        self.voc_types.update({'file': self.type_list.count('file')})
        self.voc_types.update({'folder': self.type_list.count('folder')})

        # Считаем сколько файлов и с какими расширениями есть в каталоге
        # По результатам подсчетом колличества файлов с оопределенными расширениями дополняем словарь
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
        las_ext = ['.las',]
        self.voc_types.update({'las file': ext_counter(las_ext, self)})
        dlis_ext = ['.dlis']
        self.voc_types.update({'dlis file': ext_counter(dlis_ext, self)})


class Object:
    '''
    Класс объекта, может быть как папкой, так и файлом
    '''
    def __init__(self, path):
        self.path = path
        print(path, len(path))
        self.ext = os.path.splitext(path)[1]
        print(self.ext)
        self.type = ''
        if len(path)>256:
            self.size = 0
        else:
            self.size = os.path.getsize(self.path)
        self.date = ''
        # Вызываем методы формирующие экземпляр класса
        self.type_findout()

    def type_findout(self):
        if os.path.isdir(self.path):
            self.type = 'folder'
            self.ext = '.folder'
        elif os.path.isfile(self.path):
            self.type = 'file'
        else:
            self.type = 'unknown'
            self.ext = '.unknown'

def main_application():
    app = QApplication(sys.argv)
    main = MainWindow()
    main.show()
    sys.exit(app.exec_())

if __name__ == '__main__':
   main_application()