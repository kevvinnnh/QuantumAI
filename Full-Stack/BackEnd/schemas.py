from typing import List, Optional
from pydantic import BaseModel

class Option(BaseModel):
    text: str

class Question(BaseModel):
    index: int
    question: str
    options: List[Option]
    answer: str

class ChatMessage(BaseModel):
    role: str  # "user" or "assistant"
    content: str

class ChatHistory(BaseModel):
    question_index: int
    messages: List[ChatMessage]
