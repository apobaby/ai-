import base64
import uuid
from pathlib import Path

UPLOAD_DIR = Path("uploads")
UPLOAD_DIR.mkdir(exist_ok=True)


def save_base64_image(base64_image: str, prefix: str) -> str:
    file_name = f"{prefix}_{uuid.uuid4().hex}.png"
    file_path = UPLOAD_DIR / file_name
    file_path.write_bytes(base64.b64decode(base64_image))
    return f"/uploads/{file_name}"


def save_upload_file(file_bytes: bytes, extension: str = "png", prefix: str = "file") -> str:
    file_name = f"{prefix}_{uuid.uuid4().hex}.{extension}"
    file_path = UPLOAD_DIR / file_name
    file_path.write_bytes(file_bytes)
    return f"/uploads/{file_name}"
