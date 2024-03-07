from typing import Any


IMAGE_FILETYPE = (
    "jpg",
    "jpeg",
    "png",
    "gif",
    "tiff",
    "svg+xml",
    "x-icon",
)

TXT_FILETYPE = (
    "css",
    "csv",
    "html",
    "javascript",
    "plain",
    "xml",
)

VIDEO_FILETYPE = (
    "mpeg",
    "mp4",
    "quicktime",
    "webm",
    "x-ms-wmv",
    "x-msvideo",
    "x-flv",
)

AUDIO_FILETYPE = (
    "mpeg",
    "x-ms-wma",
    "vnd.rn-realaudio",
    "x-wav",
)


class StaticFiles:
    response: Any  # Response
    mimetypes: str

    def __init__(self, response: Any, mimetype: str):
        self.response = response
        self.mimetype = mimetype

    def set_headers(self, file_type: str) -> None:
        self.response.set_headers({"Content-Type": f"{self.mimetype}/{file_type}"})
