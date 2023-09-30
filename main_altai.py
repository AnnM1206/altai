from fastapi import FastAPI, File, UploadFile, Response
import uvicorn
from fastapi.responses import FileResponse
from starlette.middleware.cors import CORSMiddleware
from ultralytics import YOLO
from yaDisk import *
import os

model = YOLO('Nano_best.pt')

disk = Storage()

def get_classes(photos: list or tuple):
    return {photo: result.names[result.probs.top1] for
                photo, result in zip(photos, model(photos))}


app = FastAPI()
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)


def move_files_to_root(directory, photo):
    # Проверяем каждую папку внутри корневой папки
    for folder in os.listdir(directory):
        # Если папка является директорией, рекурсивно вызываем функцию
        if os.path.isdir(os.path.join(directory, folder)):
            move_files_to_root(os.path.join(directory, folder), photo)
        else:
            photo.append(os.path.join(directory, folder))


@app.get("/image")
async def im_get(url):
    file_name = disk.download_files(url)
    current_directory = os.getcwd()
    path = f'{current_directory}/predict/{file_name}'

    photos = []
    move_files_to_root(path, photos)
    print(photos)

    predict = get_classes(photos)
    print(predict)
    link = disk.mak_upload_file(predict)
    return {"link": link[0], "download" : link[1]}



if __name__ == '__main__':
    # current_directory = os.getcwd()
    # path = f'{current_directory}/predict/p'


    uvicorn.run(app, port=8000)