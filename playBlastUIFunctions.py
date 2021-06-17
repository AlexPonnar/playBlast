from maya import cmds
import os

def get_file_name():
    file_name = cmds.file(query=True, sceneName=True, shortName=True)
    return file_name


def get_camera_list():
    camera_names = []
    for each in cmds.ls(type='camera'):
        camera_name = cmds.listRelatives(each, parent=True)
        camera_names.append(camera_name[0])
    return camera_names


def get_artist_name():
    return os.getenv('USER')


def get_FOV_value(selected_camera_name):
    camera_names = []
    for each in cmds.ls(type='camera'):
        camera_name = cmds.listRelatives(each, parent=True)
        camera_names.append(camera_name[0])

    if selected_camera_name in camera_names:
        camera_shape = cmds.listRelatives(selected_camera_name, shapes=True)[0]
        FOV_value = cmds.getAttr(camera_shape+'.focalLength')

    return FOV_value


def start_time_changer(start_time_box_value):
    cmds.playbackOptions(minTime=start_time_box_value, edit=True)


def end_time_changer(end_time_box_value):
    cmds.playbackOptions(maxTime=end_time_box_value, edit=True)


def play_blast(current_resolution):
    file_name = get_file_name()
    file_name_split = file_name.split('.')
    file_name=file_name_split[0]
    cmds.playblast(filename=file_name+'_blast.avi',
                   forceOverwrite=True, format='avi', percent=100,
                   widthHeight=current_resolution)


def preview():
    file_name = get_file_name()
    file_name_split = file_name.split('.')
    file_name = file_name_split[0]
    cmds.playblast(format='avi', percent=100, widthHeight=[960, 540])


