from PySide2 import QtGui, QtCore, QtWidgets
from bakeConstraint import playBlastUIFunctions
reload(playBlastUIFunctions)
from maya import cmds


class playBlastUI(QtWidgets.QDialog):

    def __init__(self, parent=None):
        super(playBlastUI, self).__init__(parent)
        self.setWindowTitle('PlayBlastUI')
        self.resize(150, 250)
        self.__init_layout()

    def __init_layout(self):
        main_layout = QtWidgets.QVBoxLayout()
        resolution_camera_layout = QtWidgets.QHBoxLayout()
        file_name_layout = QtWidgets.QFormLayout()
        artist_name_layout = QtWidgets.QHBoxLayout()
        details_layout = QtWidgets.QVBoxLayout()
        FOV_layout = QtWidgets.QFormLayout()
        start_end_frame_layout = QtWidgets.QHBoxLayout()
        buttons_layout = QtWidgets.QVBoxLayout()
        notes_layout = QtWidgets.QHBoxLayout()
        resolution_camera_fileName_artistName_layout = QtWidgets.QVBoxLayout()
        resolution_camera_fileName_artistName_group = QtWidgets.QGroupBox()
        details_group = QtWidgets.QGroupBox()
        notes_group = QtWidgets.QGroupBox()
        buttons_group = QtWidgets.QGroupBox()

        self.resolution_label = QtWidgets.QLabel()
        self.resolution_label.setText('Resolution')
        self.resolution_label.setMaximumWidth(60)

        self.resolution_button = QtWidgets.QComboBox()
        self.resolution_button.addItem('HD1080')
        self.resolution_button.addItem('HD720')
        self.resolution_button.addItem('HD540')
        self.resolution_dict = {'HD540': [960, 540], 'HD1080': [1920, 1080],
                                'HD720': [1280, 720]}
        self.current_resolution = \
            self.resolution_dict[self.resolution_button.currentText()]
        self.resolution_button.activated.connect(self.get_resolution)

        self.camera_label = QtWidgets.QLabel()
        self.camera_label.setText('Camera')
        self.camera_label.setMaximumWidth(60)

        self.camera_button = QtWidgets.QComboBox()
        self.camera_list = playBlastUIFunctions.get_camera_list()
        for each in self.camera_list:
            self.camera_button.addItem(each)
        self.camera_button.activated.connect(self.current_FOV_value)
        self.camera_button.activated.connect(self.camera_changer)

        self.file_name_label = 'File Name'
        self.file_name_input = QtWidgets.QLineEdit(playBlastUIFunctions.
                                                   get_file_name())
        file_name_layout.addRow(self.file_name_label, self.file_name_input)

        self.artist_name_label = QtWidgets.QLabel()
        self.artist_name_label.setText('Artist Name')
        self.artist_name_label.setMaximumWidth(60)

        self.artist_name_button = QtWidgets.QComboBox()
        self.artist_name_button.addItem(playBlastUIFunctions.get_artist_name())

        self.selected_camera_name = str(self.camera_button.currentText())

        self.FOV_label = 'FOV'
        self.FOV_input = QtWidgets.QLineEdit()
        self.FOV_input.setEnabled(False)
        self.FOV_input.setText(str(playBlastUIFunctions.get_FOV_value(
            self.camera_button.currentText())))
        FOV_layout.addRow(self.FOV_label, self.FOV_input)

        self.start_frame_label = QtWidgets.QLabel()
        self.start_frame_label.setText('Start Frame')
        self.start_frame_label.setMaximumWidth(60)

        self.start_frame_input = QtWidgets.QSpinBox()
        self.start_frame_input.setMinimum(1)
        self.start_frame_input.valueChanged.connect(self.start_frame_changer)


        self.end_frame_label = QtWidgets.QLabel()
        self.end_frame_label.setText('End Frame')
        self.end_frame_label.setMaximumWidth(60)

        self.end_frame_input = QtWidgets.QSpinBox()
        self.end_frame_input.setMaximum(1000)
        self.end_frame_input.setMinimum(10)
        self.end_frame_input.setValue(cmds.playbackOptions(maxTime=200,
                                                           query=True))
        self.end_frame_input.valueChanged.connect(self.end_frame_changer)

        notes_group.setTitle('Notes')

        self.notes_input = QtWidgets.QTextEdit()
        notes_layout.addWidget(self.notes_input)
        notes_group.setLayout(notes_layout)

        self.preview_button = QtWidgets.QPushButton('Preview')
        self.preview_button.clicked.connect(playBlastUIFunctions.preview)

        self.publish_button = QtWidgets.QPushButton('Publish')
        self.publish_button.clicked.connect(self.publish)

        details_group.setTitle('Details')

        resolution_camera_layout.addWidget(self.resolution_label)
        resolution_camera_layout.addWidget(self.resolution_button)
        resolution_camera_layout.addWidget(self.camera_label)
        resolution_camera_layout.addWidget(self.camera_button)

        artist_name_layout.addWidget(self.artist_name_label)
        artist_name_layout.addWidget(self.artist_name_button)

        resolution_camera_fileName_artistName_layout.\
            addLayout(resolution_camera_layout)
        resolution_camera_fileName_artistName_layout.\
            addLayout(file_name_layout)
        resolution_camera_fileName_artistName_layout.\
            addLayout(artist_name_layout)
        resolution_camera_fileName_artistName_group.\
            setLayout(resolution_camera_fileName_artistName_layout)

        start_end_frame_layout.addWidget(self.start_frame_label)
        start_end_frame_layout.addWidget(self.start_frame_input)
        start_end_frame_layout.addWidget(self.end_frame_label)
        start_end_frame_layout.addWidget(self.end_frame_input)

        details_layout.addLayout(FOV_layout)
        details_layout.addLayout(start_end_frame_layout)
        details_group.setLayout(details_layout)

        buttons_layout.addWidget(self.preview_button)
        buttons_layout.addWidget(self.publish_button)

        buttons_group.setLayout(buttons_layout)

        main_layout.addWidget(resolution_camera_fileName_artistName_group)
        main_layout.addWidget(details_group)
        main_layout.addWidget(notes_group)
        main_layout.addWidget(buttons_group)

        self.setLayout(main_layout)

    def current_FOV_value(self):
        self.FOV_input.setText(str(playBlastUIFunctions.get_FOV_value(
            self.camera_button.currentText())))

    def start_frame_changer(self):
        self.start_time_box_value = self.start_frame_input.value()
        playBlastUIFunctions.start_time_changer(self.start_time_box_value)

    def end_frame_changer(self):
        self.end_time_box_value = self.end_frame_input.value()
        playBlastUIFunctions.end_time_changer(self.end_time_box_value)

    def camera_changer(self):
        cmds.select(self.camera_button.currentText())

    def get_resolution(self):
        self.current_resolution = self.resolution_dict[
            self.resolution_button.currentText()]

        return self.current_resolution

    def publish(self):
        playBlastUIFunctions.play_blast(self.current_resolution)




def main():
    my_window = playBlastUI()
    my_window.show()


if __name__ == '__main__':
    main()