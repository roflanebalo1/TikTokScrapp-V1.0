from abc import ABC, abstractmethod
from src.applications.dto import CookieFileORMDTO



class ITiktokSessionRepository(ABC):

    @abstractmethod
    def load_cookies_from_db(self) -> CookieFileORMDTO:
        pass
    
