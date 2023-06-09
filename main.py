""" Необходимые модули """
import json
import os

from PyQt5.QtCore import Qt
from PyQt5.QtWidgets import (
    QApplication,
    QHBoxLayout,
    QInputDialog,
    QLabel,
    QLineEdit,
    QListWidget,
    QPushButton,
    QTextEdit,
    QVBoxLayout,
    QWidget,
)
from qt_material import apply_stylesheet


""" Заметка в json """
notes = {
    "Добро пожаловать": {
        "текст": "Это самое лучшее приложение для заметок в мире!",
        "теги": ["добро", "инструкция"],
    }
}

# если заметки не существует
if not os.path.exists("notes_data.json"):
    # сохраняем стартовую заметку в новый созданный json файл
    with open("notes_data.json", "w", encoding="utf-8") as file:
        json.dump(notes, file, sort_keys=True, ensure_ascii=False, indent=4)

# объект приложения
app = QApplication([])
apply_stylesheet(app, theme="light_blue.xml")  # тема для приложения
# объект окна
window = QWidget()
window.setWindowTitle("Умные заметки")
window.resize(900, 600)


# окно текста заметки
filed_text = QTextEdit()

# окно списка заметок
list_nouts = QListWidget()
list_nouts_label = QLabel("Умные заметки")

# кнопки для заметок
btn_create_note = QPushButton("Создать заметку")
btn_delete_note = QPushButton("Удалить заметку")
btn_save_note = QPushButton("Сохранить заметку")

# окно списка тегов заметки
list_tags = QListWidget()
list_tags_label = QLabel("Список тегов")

# окно ввода тега
field_tag = QLineEdit()
field_tag.setPlaceholderText("Введите тег...")

# кнопки для тегов
btn_add_tag = QPushButton("Добавить к заметке")
btn_delete_tag = QPushButton("Открепить от заметки")
btn_search_tag = QPushButton("Искать заметки по тегу")

# первый "столбец"-лэйаут
col1 = QVBoxLayout()
col1.addWidget(filed_text)

# второй "столбец"-лэйаут
col2 = QVBoxLayout()
col2.addWidget(list_nouts_label)
col2.addWidget(list_nouts)

# кнопки для работы с заметками
row1 = QHBoxLayout()
row1.addWidget(btn_create_note)
row1.addWidget(btn_delete_note)
row2 = QHBoxLayout()
row2.addWidget(btn_save_note)

# добавляем обе "линии"-лэйаута с кнопками
# на 2 столбец
col2.addLayout(row1)
col2.addLayout(row2)

# добавляем на 2 "столбец"-лэйаут
# список тегов и поле для ввода тега
col2.addWidget(list_tags_label)
col2.addWidget(list_tags)
col2.addWidget(field_tag)

# кнопки для работы с тегами
row3 = QHBoxLayout()
row3.addWidget(btn_add_tag)
row3.addWidget(btn_delete_tag)
row4 = QHBoxLayout()
row4.addWidget(btn_search_tag)

# добавляем обе "линии"-лэйаута с кнопками
# на 2 столбец
col2.addLayout(row3)
col2.addLayout(row4)

# главная "линия"-лэйаут окна
# на неё добавляются 2 "столбца"-лэйаута
layout_notes = QHBoxLayout()
layout_notes.addLayout(col1, stretch=2)
layout_notes.addLayout(col2, stretch=1)

# прикрепляем линию на окно
window.setLayout(layout_notes)

""" Функционал приложения """


# функция для отображения заметки
def show_note():
    key = list_nouts.selectedItems()[0].text()
    filed_text.setText(notes[key]["текст"])
    list_tags.clear()
    list_tags.addItems(notes[key]["теги"])


# функция для создания заметки
def add_note():
    note_name, ok = QInputDialog.getText(
        window, "Добавить заметку", "Название заметок:"
    )
    if ok and note_name != "":
        notes[note_name] = {"текст": "", "теги": []}
        list_nouts.addItem(note_name)
        list_tags.addItems(notes[note_name]["теги"])
        print(notes)


# функция для сохранения заметки
def save_note():
    if list_nouts.selectedItems():
        key = list_nouts.selectedItems()[0].text()
        notes[key]["текст"] = filed_text.toPlainText()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для сохранения не выбрана!")


# функция для удаления заметки
def del_note():
    if list_nouts.selectedItems():
        key = list_nouts.selectedItems()[0].text()
        del notes[key]
        list_tags.clear()
        filed_text.clear()
        list_nouts.clear()
        list_nouts.addItems(notes)
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для удаления не выбрана")


# функция для добавления тега
def add_tag():
    if list_nouts.selectedItems():
        key = list_nouts.selectedItems()[0].text()
        tag = field_tag.text()
        if not tag in notes[key]["теги"]:
            notes[key]["теги"].append(tag)
            list_tags.addItem(tag)
            field_tag.clear()
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Заметка для добавления не выбрана")


# функция для открепления тега
def del_tag():
    if list_tags.selectedItems():
        key = list_nouts.selectedItems()[0].text()
        tag = list_tags.selectedItems()[0].text()
        notes[key]["теги"].remove(tag)
        list_tags.clear()
        list_tags.addItems(notes[key]["теги"])
        with open("notes_data.json", "w", encoding="utf-8") as file:
            json.dump(notes, file, sort_keys=True, ensure_ascii=False)
        print(notes)
    else:
        print("Тег для удаления не выбран")


# функция для поиска по тегу
def search_tag():
    print(btn_search_tag.text())
    tag = field_tag.text()
    if btn_search_tag.text() == "Искать заметки по тегу" and tag:
        print(tag)
        notes_filtered = {}
        for note in notes:
            if tag in notes[note]["теги"]:
                notes_filtered[note] = notes[note]
        btn_search_tag.setText("Сбросить поиск")
        list_nouts.clear()
        list_tags.clear()
        filed_text.clear()
        list_nouts.addItems(notes_filtered)
        print(btn_search_tag.text())
    elif btn_search_tag.text() == "Сбросить поиск":
        list_nouts.clear()
        list_tags.clear()
        filed_text.clear()
        list_nouts.addItems(notes)
        print(btn_search_tag.text())
    else:
        pass


# # подключение функций к кнопками
# работа с заметками
list_nouts.itemClicked.connect(show_note)
btn_create_note.clicked.connect(add_note)
btn_delete_note.clicked.connect(del_note)
btn_save_note.clicked.connect(save_note)
btn_add_tag.clicked.connect(add_tag)
btn_delete_tag.clicked.connect(del_tag)
btn_search_tag.clicked.connect(search_tag)

# считываем файл с заметками и запоминаем в словарь notes
with open("notes_data.json", "r", encoding="utf-8") as file:
    notes = json.load(file)
# добавляем названия заметок в список заметок
list_nouts.addItems(notes)

# показываем окно
window.show()
# запускаем приложение
app.exec_()
