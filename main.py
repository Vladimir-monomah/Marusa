import sys
from PyQt5 import QtCore
from PyQt5.QtWidgets import QApplication, QWidget, QPushButton, QLabel, QFileDialog, QLineEdit, QDesktopWidget, \
    QTextEdit, QMessageBox, QInputDialog
from vk_api import VkUpload
import vk_api
import os


class App(QWidget):

    def __init__(self):
        super().__init__()
        self.title = 'ChatBot Marusya'
        self.left = 100
        self.top = 100
        self.width = 720
        self.height = 500
        self.initUI()

    def initUI(self):
        self.setWindowTitle(self.title)
        screen = app.primaryScreen()
        screen_size = screen.size()
        self.left = (screen_size.width() - self.width) // 2
        self.top = (screen_size.height() - self.height) // 2
        self.setGeometry(self.left, self.top, self.width, self.height)

        self.setMinimumSize(self.width, self.height)
        self.setMaximumSize(self.width, self.height)

        # Создаем кнопки
        self.post_button = QPushButton('Отправить пост на стену группы', self)
        self.post_button.move(20, 20)
        self.post_button.clicked.connect(self.post_on_wall)

        self.send_button = QPushButton('Отправить сообщение всем участникам группы', self)
        self.send_button.move(20, 60)
        self.send_button.clicked.connect(self.send_message)

        self.send_to_some_button = QPushButton('Отправить сообщение некоторым участникам группы', self)
        self.send_to_some_button.move(20, 100)
        self.send_to_some_button.clicked.connect(self.send_to_some_members)

        self.upload_button = QPushButton('Выбрать изображение', self)
        self.upload_button.move(20, 140)
        self.upload_button.clicked.connect(self.upload_photo)

        self.file_label = QLabel('Изображение не выбрано', self)
        self.file_label.move(20, 180)
        self.file_label.setStyleSheet('color: red')

        screen_width = screen_size.width()
        self.file_label.setFixedWidth(screen_width - 40)

        self.group_id_label = QLabel('ID группы:', self)
        self.group_id_label.move(20, 200)

        self.group_id_edit = QLineEdit(self)
        self.group_id_edit.setGeometry(105, 200, 120, 20)

        self.user_token_label = QLabel('Токен пользователя:', self)
        self.user_token_label.move(20, 240)

        self.user_token_edit = QLineEdit(self)
        self.user_token_edit.setGeometry(180, 240, 520, 20)

        self.message_edit = QTextEdit(self)
        self.message_edit.setGeometry(20, 280, 680, 110)
        self.message_edit.setAlignment(QtCore.Qt.AlignTop | QtCore.Qt.AlignLeft)

        self.max_photos = 2
        self.photo_labels = []
        self.photo_paths = []
        self.add_photo_label()

        # Создаем кнопку для перехода на сайт
        self.site_button = QPushButton('Перейти на сайт для получения токена', self)
        self.site_button.move(20, 400)
        self.site_button.clicked.connect(self.go_to_site)

        self.show()

    def go_to_site(self):
        import webbrowser
        webbrowser.open('https://vkhost.github.io/')

    def add_photo_label(self):
        if len(self.photo_labels) < self.max_photos:
            label = QLabel('Изображение не выбрано', self)
            label.move(20, 180 + 40 * len(self.photo_labels))
            label.setStyleSheet('color: red')
            screen = app.primaryScreen()
            screen_width = screen.size().width()
            label.setFixedWidth(screen_width - 40)
            label.hide()
            self.photo_labels.append(label)

    def post_on_wall(self):
        if  len(self.user_token_edit.text())==0:
            # Если сообщение не выбрано
            QMessageBox.warning(self, 'Ошибка', 'Введите токен пользователя')
            return
        # Авторизуемся на странице
        # token = 'vk1.a.TQhKgXu-fyMn1P6VGm2PsJAZf91v2k_el41PhMluvvGM9u7xCuSU-MM5mucj6Ogs1UerGf0OfxTRlsPAtkinCohPT_QctIPz8mwbHSP_FakYT2pWAF4ou4_Zk5j1P-9nOr8qyaObdt4C9mkDz2SXqIEet04qY0kZJaguzfsYW8Gkdvzr_teQiz4IZYQ9J4jHYYNawTqpLgIFs2swL7tWFw'
        # token = '8d32f31f8d32f31f8d32f31fcc8e26524888d328d32f31fe9a31a1d45ce3bfa0036fa87'
        vk_session = vk_api.VkApi(token=self.user_token_edit.text())

        # Получаем объект для загрузки изображений
        upload = VkUpload(vk_session)

        # Получаем объект для работы с API
        vk = vk_session.get_api()

        # Получаем текст сообщения
        message = self.message_edit.toPlainText()

        # Получаем ID группы
        group_id = self.group_id_edit.text()

        if not message and len(self.photo_paths) == 0:
            if not message:
                # Если сообщение не выбрано
                QMessageBox.warning(self, 'Ошибка', 'Выберите текст сообщения')
                return

            if len(self.photo_paths) == 0:
                # Если сообщение не выбрано
                QMessageBox.warning(self, 'Ошибка', 'Выберите картинки')
                return

        if not group_id:
            # Если ID группы не выбран
            QMessageBox.warning(self, 'Ошибка', 'Выберите ID группы')
            return

        # Проверяем, существует ли файл с изображением
        photo_data_list = []
        for photo_path in self.photo_paths:
            if os.path.exists(photo_path):
                # Открываем файл с изображением
                with open(photo_path, 'rb') as photo_file:
                    # Загружаем изображение на сервер ВКонтакте
                    photo_data = upload.photo_wall(photos=photo_file)[0]
                    photo_data_list.append(photo_data)
            else:
                # Если файл с изображением не выбран
                photo_data_list.append(None)

        # Проверяем, что количество изображений не превышает максимальное
        photo_data_list = photo_data_list[:self.max_photos]
        if len(photo_data_list) > self.max_photos:
            QMessageBox.warning(self, 'Ошибка', 'Выберите не более 2 изображений')
            return

        # Получаем информацию о группе
        group_info = vk.groups.getById(group_id=group_id)

        # Получаем наименование группы
        group_name = group_info[0]['name']

        # Отправляем пост на стену группы
        attachments = ''
        for photo_data in photo_data_list:
            if photo_data:
                attachments += f"photo{photo_data['owner_id']}_{photo_data['id']},"
        if photo_data_list:
            attachments = attachments[:-1]
        if attachments:
            # Если нужно прикрепить изображение
            response = vk.wall.post(owner_id='-' + str(group_id), message=message,
                                    from_group=1,
                                    attachments=attachments)
        else:
            # Если изображение не нужно прикреплять
            response = vk.wall.post(owner_id='-' + str(group_id), message=message,
                                    from_group=1)

    def send_message(self):
        # Авторизуемся на странице
        token = 'vk1.a.3e1v1mrf-VlrGw6xSAqv7BBASfmUUKIWik7wjPDwJICsnTo16G_al_wBn2rh3TUdNee9Qap0VckxVmWQWTAM5LP8uetvVbpyhgFS0V-TQI7pooJCWp-sOEjZJ2k8BkQ31897CAqmhjBADLGPw_9fWZCkm-HKFIbPj5G4kiSMFjiDvQw9-tAQLNmEZMx-yNh-Yn2xDqt96vFQk-WBe19I7A'
        vk_session = vk_api.VkApi(token=token)

        # Получаем объект для загрузки изображений
        upload = VkUpload(vk_session)

        # Получаем объект для работы с API
        vk = vk_session.get_api()

        # Получаем текст сообщения
        message = self.message_edit.toPlainText()

        # Получаем ID группы
        group_id = self.group_id_edit.text()

        if not message and len(self.photo_paths) == 0:
            if not message:
                # Если сообщение не выбрано
                QMessageBox.warning(self, 'Ошибка', 'Выберите текст сообщения')
                return

            if len(self.photo_paths) == 0:
                # Если сообщение не выбрано
                QMessageBox.warning(self, 'Ошибка', 'Выберите картинки')
                return

        if not group_id:
            # Если ID группы не выбран
            QMessageBox.warning(self, 'Ошибка', 'Выберите ID группы')
            return

        # Проверяем, существует ли файл с изображением
        photo_data_list = []
        for photo_path in self.photo_paths:
            if os.path.exists(photo_path):
                # Открываем файл с изображением
                with open(photo_path, 'rb') as photo_file:
                    # Загружаем изображение на сервер ВКонтакте
                    photo_data = upload.photo_wall(photos=photo_file)[0]
                    photo_data_list.append(photo_data)
            else:
                # Если файл с изображением не выбран
                photo_data_list.append(None)

        # Проверяем, что количество изображений не превышает максимальное
        photo_data_list = photo_data_list[:self.max_photos]
        if len(photo_data_list) > self.max_photos:
            QMessageBox.warning(self, 'Ошибка', 'Выберите не более 2 изображений')
            return

        # Получаем список участников группы
        members = set(map(lambda x: str(x), vk.groups.getMembers(group_id=group_id)['items']))

        # Отправляем сообщение каждому участнику группы с прикрепленным изображением
        members_string = str.join(",", members)
        attachments = ''
        for photo_data in photo_data_list:
            if photo_data:
                attachments += f"photo{photo_data['owner_id']}_{photo_data['id']},"
        if photo_data_list:
            attachments = attachments[:-1]
        if attachments:
            vk.messages.send(peer_ids=members_string, message=message,
                             attachment=attachments, random_id=0)
        else:
            vk.messages.send(peer_ids=members_string, message=message, random_id=0)

    def upload_photo(self):
        # Открываем диалог выбора файлов
        options = QFileDialog.Options()
        options |= QFileDialog.DontUseNativeDialog
        file_names, _ = QFileDialog.getOpenFileNames(self, "Выбрать изображения", "",
                                                     "All Files (*);;Image Files (*.png *.jpg *.bmp)", options=options)
        if file_names:
            # Объединяем пути к файлам в одну строку, разделяя их запятой
            self.photo_paths.extend(file_names)
            self.photo_paths = self.photo_paths[-2:]
            if len(self.photo_labels) == 0:
                self.add_photo_label()
            self.photo_labels[0].setText(str.join(",", self.photo_paths))
            self.photo_labels[0].setStyleSheet('color: black')
            self.photo_labels[0].show()

            # Предупреждение, если выбрано больше 2 файлов

        else:
            self.photo_paths = []
            for label in self.photo_labels:
                label.setText('Изображение не выбрано')
                label.setStyleSheet('color: red')
                label.hide()
            self.add_photo_label()

    def send_to_some_members(self):
        # Авторизуемся на странице
        token = 'vk1.a.3e1v1mrf-VlrGw6xSAqv7BBASfmUUKIWik7wjPDwJICsnTo16G_al_wBn2rh3TUdNee9Qap0VckxVmWQWTAM5LP8uetvVbpyhgFS0V-TQI7pooJCWp-sOEjZJ2k8BkQ31897CAqmhjBADLGPw_9fWZCkm-HKFIbPj5G4kiSMFjiDvQw9-tAQLNmEZMx-yNh-Yn2xDqt96vFQk-WBe19I7A'
        vk_session = vk_api.VkApi(token=token)

        # Получаем объект для загрузки изображений
        upload = VkUpload(vk_session)

        # Получаем объект для работы с API
        vk = vk_session.get_api()

        # Получаем текст сообщения
        message = self.message_edit.toPlainText()

        # Получаем ID группы
        group_id = self.group_id_edit.text()

        if not message:
            # Если сообщение не выбрано
            QMessageBox.warning(self, 'Ошибка', 'Выберите текст сообщения')
            return

        if not group_id:
            # Если ID группы не выбран
            QMessageBox.warning(self, 'Ошибка', 'Выберите ID группы')
            return

        # Получаем список участников группы
        members = vk.groups.getMembers(group_id=group_id)['items']

        # Получаем информацию о пользователях
        users_info = vk.users.get(user_ids=members, fields='first_name,last_name')
        # Создаем словарь, где ключом будет id пользователя, а значением - его имя
        users_dict = {user['id']: f"{user['first_name']} {user['last_name']}" for user in users_info}

        # Открываем диалог выбора участников группы
        selected_members, ok = QInputDialog.getMultiLineText(self, "Выбрать участников", "Выберите участников:",
                                                             '\n'.join([f'{m}({users_dict[m]})' for m in members]))
        if not ok:
            return

        # Отправляем сообщение выбранным участникам группы
        attachments = ''
        for photo_path in self.photo_paths:
            if os.path.exists(photo_path):
                # Открываем файл с изображением
                with open(photo_path, 'rb') as photo_file:
                    # Загружаем изображение на сервер ВКонтакте
                    photo_data = upload.photo_messages(photos=photo_file)[0]
                    attachments += f"photo{photo_data['owner_id']}_{photo_data['id']},"
            else:
                # Если файл с изображением не выбран
                attachments += ','
        attachments = attachments[:-1]
        selected_members = str.join(',',
                                    set(map(
                                        lambda x: x.split('(')[0],
                                        selected_members.split('\n'))))

        vk.messages.send(peer_ids=selected_members, message=message, attachment=attachments, random_id=0)


if __name__ == '__main__':
    app = QApplication(sys.argv)
    ex = App()
    sys.exit(app.exec_())
