from pydantic import BaseModel
from typing import List, Optional
from enum import Enum


class Language(str, Enum):
    ENGLISH = "English"
    SPANISH = "Spanish"
    FRENCH = "French"
    GERMAN = "German"


class Genre(str, Enum):
    FICTION = "Fiction"
    NON_FICTION = "Non-Fiction"
    SCIENCE_FICTION = "Science Fiction"
    FANTASY = "Fantasy"
    MYSTERY = "Mystery"
    ROMANCE = "Romance"
    HORROR = "Horror"
    BIOGRAPHY = "Biography"
    HISTORY = "History"
    SELF_HELP = "Self Help"


class Book(BaseModel):
    title: str
    desc: str
    genre: Genre
    author: str
    publisher: str
    published_date: str
    page_count: int
    language: Language
    average_rating: Optional[float] = 0
    price: float
    currency: Optional[str] = "USD"
    tags: Optional[List[str]] = []
    edition: Optional[str] = None


class UpdateBook(BaseModel):
    title: Optional[str] = None
    desc: Optional[str] = None
    genre: Optional[Genre] = None
    author: Optional[str] = None
    publisher: Optional[str] = None
    published_date: Optional[str] = None
    page_count: Optional[int] = None
    language: Optional[Language] = None
    average_rating: Optional[float] = None
    price: Optional[float] = None
    currency: Optional[str] = None
    tags: Optional[List[str]] = None
    edition: Optional[str] = None
