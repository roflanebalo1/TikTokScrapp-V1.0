from dataclasses import dataclass


@dataclass
class CookieDTO:
    name: str
    value: str


@dataclass
class CookieFileORMDTO:
    cookies: list[CookieDTO]
