from abc import ABC, abstractmethod
from typing import Optional
from app.domain.entities.upload_csv import UploadCsv

class IUploadCsvRepository(ABC):

    @abstractmethod
    def salvar(self, upload: UploadCsv) -> UploadCsv:
        pass

    @abstractmethod
    def atualizar(self, upload: UploadCsv) -> UploadCsv:
        pass

    @abstractmethod
    def buscar_por_id(self, id: int) -> Optional[UploadCsv]:
        pass