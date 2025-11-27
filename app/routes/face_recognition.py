from fastapi import APIRouter, Depends, HTTPException, status, UploadFile
from sqlalchemy.orm import Session
from typing import List
from datetime import datetime
from app.services import generar_embedding, obtener_vectores_normalizados, cargar_index, consultar_embedding, insertar_embedding
from app.database import get_db
from app.models import Guardian
from app.schemas import GuardianResponse
import numpy as np
import cv2


router = APIRouter(prefix="/face", tags=["Face Recognition"])

# FACE RECOGNITION - Recognize guardian by face image
@router.post("/recognize")
async def create_guardian(file: UploadFile, db: Session = Depends(get_db), index = Depends(cargar_index)):
    contenido = await file.read()
    np_arr = np.frombuffer(contenido, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    vector = generar_embedding(img)
    vector_n = obtener_vectores_normalizados(vector)
    dist, persona_id = consultar_embedding(index, vector_n)
    
    if dist[0][0] > 0.9:  # Umbral de distancia para considerar una coincidencia
        raise HTTPException(status_code=404, detail="La imagen no coincide con ningún tutor registrado.")
    #return {"message": f"Distancia de coincidencia: {dist}"}
    guardian_db = db.query(Guardian).filter(Guardian.guardianId == persona_id[0][0]).first()

    if not guardian_db:
        raise HTTPException(status_code=404, detail="No se encontro ningun tutor con el ID obtenido.")
    
    return guardian_db

#LOAD A NEW IMAGE AND INSERT IT INTO THE INDEX
@router.post("/enroll/{guardian_id}", status_code=status.HTTP_201_CREATED)
async def enroll_guardian(guardian_id: int, file: UploadFile, db: Session = Depends(get_db), index = Depends(cargar_index)):
    guardian_db = db.query(Guardian).filter(Guardian.guardianId == guardian_id).first()

    if not guardian_db:
        raise HTTPException(status_code=404, detail="Tutor no encontrado.")

    contenido = await file.read()
    np_arr = np.frombuffer(contenido, np.uint8)
    img = cv2.imdecode(np_arr, cv2.IMREAD_COLOR)
    img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)

    vector = generar_embedding(img)
    vector_n = obtener_vectores_normalizados(vector)
    insertar_embedding(index, vector_n, guardian_id)

    return {"message": "Imagen del tutor registrada exitosamente."}