from typing import Literal

from fastapi import APIRouter, Depends, File, Form, HTTPException, UploadFile
from pydantic import BaseModel
from sqlalchemy.orm import Session

from models.database import get_db
from models.entities import Avatar, Clothes, TryOnResult, User
from services.image_generator import save_base64_image, save_upload_file
from services.openai_service import OpenAIService

router = APIRouter()
openai_service = OpenAIService()


class TryOnRequest(BaseModel):
    avatar_image_url: str
    clothes_image_url: str


class PoseRequest(BaseModel):
    avatar_image_url: str
    pose_type: Literal["standing", "walking", "side view"]


@router.post("/generate-avatar")
async def generate_avatar(
    user_image: UploadFile = File(...),
    height: float = Form(...),
    weight: float = Form(...),
    gender: str = Form(...),
    db: Session = Depends(get_db),
):
    user = User()
    db.add(user)
    db.commit()
    db.refresh(user)

    image_bytes = await user_image.read()
    image_b64 = openai_service.to_base64(image_bytes)
    prompt = (
        "根据用户照片生成一个完整的模特形象，保持用户面部特征，生成全身人物。"
        f"身高:{height}cm，体重:{weight}kg，性别:{gender}，照片风格真实自然。"
    )

    try:
        output_b64 = openai_service.generate_image_from_prompt(prompt, image_b64)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    image_url = save_base64_image(output_b64, "avatar")
    avatar = Avatar(user_id=user.id, image_url=image_url, height=height, weight=weight, gender=gender)
    db.add(avatar)
    db.commit()
    db.refresh(avatar)

    return {"avatar_image_url": image_url, "avatar_id": avatar.id}


@router.post("/upload-clothes")
async def upload_clothes(clothes_image: UploadFile = File(...), db: Session = Depends(get_db)):
    image_bytes = await clothes_image.read()
    ext = clothes_image.filename.split(".")[-1] if clothes_image.filename and "." in clothes_image.filename else "png"
    image_url = save_upload_file(image_bytes, ext, "clothes")

    clothes = Clothes(image_url=image_url)
    db.add(clothes)
    db.commit()
    db.refresh(clothes)

    return {"clothes_image_url": image_url, "clothes_id": clothes.id}


@router.post("/try-on")
def try_on(payload: TryOnRequest, db: Session = Depends(get_db)):
    avatar = db.query(Avatar).filter(Avatar.image_url == payload.avatar_image_url).first()
    clothes = db.query(Clothes).filter(Clothes.image_url == payload.clothes_image_url).first()
    if not avatar or not clothes:
        raise HTTPException(status_code=404, detail="Avatar or clothes not found")

    prompt = (
        "将第二张图里的服装自然穿到第一张图人物身上，保持人物面部一致、体型比例一致，"
        "输出真实自然的全身试穿效果图。"
    )

    try:
        avatar_b64 = openai_service.local_image_url_to_base64(payload.avatar_image_url)
        clothes_b64 = openai_service.local_image_url_to_base64(payload.clothes_image_url)
        output_b64 = openai_service.generate_image_from_prompt(prompt, avatar_b64, clothes_b64)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    result_url = save_base64_image(output_b64, "tryon")
    result = TryOnResult(avatar_id=avatar.id, clothes_id=clothes.id, result_url=result_url)
    db.add(result)
    db.commit()

    return {"result_image_url": result_url}


@router.post("/generate-pose")
def generate_pose(payload: PoseRequest):
    prompt = (
        f"将该模特改为 {payload.pose_type} 姿势，保持同一人脸和体型，"
        "保留原有穿搭风格，输出真实自然的全身图。"
    )

    try:
        avatar_b64 = openai_service.local_image_url_to_base64(payload.avatar_image_url)
        output_b64 = openai_service.generate_image_from_prompt(prompt, avatar_b64)
    except Exception as exc:
        raise HTTPException(status_code=500, detail=str(exc)) from exc

    image_url = save_base64_image(output_b64, "pose")
    return {"pose_image_url": image_url}


@router.get("/history")
def history(db: Session = Depends(get_db)):
    rows = db.query(TryOnResult).order_by(TryOnResult.created_at.desc()).all()
    return [
        {
            "id": row.id,
            "avatar_id": row.avatar_id,
            "clothes_id": row.clothes_id,
            "result_url": row.result_url,
            "created_at": row.created_at,
        }
        for row in rows
    ]


@router.get("/avatars")
def list_avatars(db: Session = Depends(get_db)):
    rows = db.query(Avatar).order_by(Avatar.created_at.desc()).all()
    return [{"id": row.id, "image_url": row.image_url} for row in rows]


@router.get("/clothes")
def list_clothes(db: Session = Depends(get_db)):
    rows = db.query(Clothes).order_by(Clothes.created_at.desc()).all()
    return [{"id": row.id, "image_url": row.image_url} for row in rows]
