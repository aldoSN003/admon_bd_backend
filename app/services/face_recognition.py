import cv2
import numpy as np
from deepface import DeepFace
import faiss
from app.database import get_db
from app.models import Guardian
import requests
from PIL import Image
from io import BytesIO
from sqlalchemy.orm import Session
import os

# Ruta absoluta: Asegúrate de que esta ruta sea correcta para tu servidor
INDEX_PATH = os.path.join(os.getcwd(), "indice_faiss.bin")

#FUNCION QUE GENERA LOS EMBEDDINGS
def generar_embedding(img):
    #img_norm = normalizar_imagen(img, mostrar=True)
    emb = DeepFace.represent(
        img_path=img,
        model_name="Facenet512",
        enforce_detection=True
    )[0]["embedding"]
    #print(f"Tipo del embedding: {type(emb)}")
    return emb

#FUNCION QUE OBTIENE LOS VECTORES NORMALIZADOS
def obtener_vectores_normalizados(embedding):
    v = np.array(embedding).astype("float32")

    # Normalizar vector (opcional pero recomendable)
    v = v / np.linalg.norm(v)
    v = v.reshape(1, -1) # Asegurar que es 2D
    #print(f"Tipo del vector normalizado: {type(v)}")
    #print(f"Tamaño del vector normalizado: {v.shape}")
    return v

#FUNCION QUE DEVUELVE EL OBJETO INDEX (CARGADO DESDE DISCO O CREADO NUEVO)
def cargar_index():
    d = 512  # Dimensionalidad de los embeddings Facenet
    try:
        index_with_ids = faiss.read_index(INDEX_PATH)
        #print(f"Indice FAISS cargado desde: {INDEX_PATH}")
    except:
        index = faiss.IndexFlatL2(d)
        index_with_ids = faiss.IndexIDMap(index)
        #print("indice nuevo")
        #print(INDEX_PATH)

    return index_with_ids

#FUNCION QUE INSERTA EMBEDDINGS EN EL INDEX
def insertar_embedding(index, v, id):
    ids = np.array([id], dtype='int64')
    index.add_with_ids(v, ids)
    faiss.write_index(index, INDEX_PATH)

#FUNCION QUE CONSULTA EMBEDDINGS EN EL INDEX
def consultar_embedding(index, v, k=1):
    D, I = index.search(v, k)
    return D, I

def load_image_from_url(url: str) -> Image.Image:
    response = requests.get(url)
    response.raise_for_status()  # Lanza error si falla la descarga
    return Image.open(BytesIO(response.content)).convert("RGB")


def process_guardians_without_embeddings(db: Session = get_db()):
    index = cargar_index()
    tutores = db.query(Guardian).filter(Guardian.hasEmbedding == 0).all()

    for tutor in tutores:
        if not tutor.photographUrl:
            print(f"Tutor {tutor.guardianId} no tiene URL de imagen, se omite.")
            continue

        try:
            img = load_image_from_url(tutor.imagen_url)
            emb = generar_embedding(img)
            emb_n = obtener_vectores_normalizados(emb)
            insertar_embedding(index, emb_n, tutor.guardianId)

            # Actualizar la bandera
            tutor.hasEmbedding = 1
            db.commit()

        except Exception as e:
            print(f"Error procesando tutor {tutor.id}: {e}")
            db.rollback()

def cargar_imagenes_prueba():
    pass