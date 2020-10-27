from django import template
from django.core.files.storage import default_storage, FileSystemStorage
import os

BASE_DIR = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), '..')

register = template.Library()

#That function is custom filter that check if file exists
@register.filter(name='file_exists')
def file_exists(path):
    filepath = BASE_DIR + path
    if default_storage.exists(filepath):
        return path
    else:
        new_filepath = '/media/Avatars/blankAvatar/blankAvatar.png'
        return new_filepath