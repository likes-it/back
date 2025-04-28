from abc import ABC, abstractmethod
from typing import BinaryIO

class ImageUploader(ABC):
    @abstractmethod
    def upload(self, file: BinaryIO, filename: str) -> str:
        """Upload a file and return its accessible URL"""
        pass

    @abstractmethod
    def delete(self, object_key: str) -> None:
        """Delete a file from the storage"""
        pass