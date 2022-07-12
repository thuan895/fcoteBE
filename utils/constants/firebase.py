
import pyrebase
from django.core.files.storage import default_storage
from os.path import exists
from Account.serializers import GetImageSerializer


class FirebaseConfig():
    config = {
        'apiKey': "AIzaSyDOtGh7iVmfOONu58TKLIigP_IzmTbPQL0",
        'authDomain': "fcote-backend.firebaseapp.com",
        'databaseURL': "https://fcote-backend-default-rtdb.asia-southeast1.firebasedatabase.app",
        'projectId': "fcote-backend",
        'storageBucket': "fcote-backend.appspot.com",
        'messagingSenderId': "275862896649",
        'appId': "1:275862896649:web:bbfaa8a00079a00ed078d8"
    }


def uploadFile(file, path):

    try:
        extension = file.name.split(".")[-1]
        path = path + "." + extension
        firebase = pyrebase.initialize_app(FirebaseConfig.config)
        storage = firebase.storage()
        file_save = default_storage.save(path, file)
        storage.child(path).put(path)
        return path
    except Exception as e:
        return None


def downloadImage(path):
    if exists(path):
        return True
    else:
        try:
            firebase = pyrebase.initialize_app(FirebaseConfig.config)
            storage = firebase.storage()
            storage.child(path).download(
                path.replace(path.split("/")[-1], ""), path)
            return True
        except Exception as e:
            return False
