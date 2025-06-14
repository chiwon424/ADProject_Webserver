# library/utils.py

from django.conf import settings
from pybo.exceptions import FileTooLargeException

def validate_uploaded_files(files):
    file = files.get('file')  # 'file'은 QuestionForm의 파일 필드명
    if file and file.size > settings.MAX_UPLOAD_SIZE:
        raise FileTooLargeException(
            f"파일 '{file.name}'은 너무 큽니다. 최대 크기는 {settings.MAX_UPLOAD_SIZE // 1024}KB입니다."
        )