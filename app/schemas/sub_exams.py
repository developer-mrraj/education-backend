# # schemas/sub_exam.py

# from pydantic import BaseModel
# from typing import Optional


# # -------------------------
# # Base Schema
# # -------------------------
# class SubExamBase(BaseModel):
#     title: str
#     subtitle: Optional[str] = None
#     # tagline: Optional[str] = None

#     total_tests: int

#     # logo_url: Optional[str] = None
#     thumbnail_url: Optional[str] = None

#     is_active: bool = True


# # -------------------------
# # Create Schema
# # -------------------------
# class SubExamCreate(SubExamBase):
#     pass


# # -------------------------
# # Update Schema
# # -------------------------
# class SubExamUpdate(BaseModel):
#     main_exam_id: Optional[int] = None

#     title: Optional[str] = None
#     subtitle: Optional[str] = None
   

#     total_tests: Optional[int] = None

  
#     thumbnail_url: Optional[str] = None

#     is_active: Optional[bool] = None


# # -------------------------
# # Response Schema
# # -------------------------
# class SubExamResponse(SubExamBase):
#     id: int
#     main_exam_id: int
    
#     class Config:
#         from_attributes = True


# schemas/sub_exam.py

from pydantic import BaseModel
from typing import Optional


# -------------------------
# Base Schema
# -------------------------
class SubExamBase(BaseModel):
    title: str
    subtitle: Optional[str] = None
    # tagline: Optional[str] = None

    total_tests: int

    # logo_url: Optional[str] = None
    thumbnail_url: Optional[str] = None

    is_active: bool = True


# -------------------------
# Create Schema
# -------------------------
class SubExamCreate(SubExamBase):
    pass


# -------------------------
# Update Schema
# -------------------------
class SubExamUpdate(BaseModel):
    main_exam_id: Optional[int] = None

    title: Optional[str] = None
    subtitle: Optional[str] = None
   

    total_tests: Optional[int] = None

  
    thumbnail_url: Optional[str] = None

    is_active: Optional[bool] = None


# -------------------------
# Response Schema
# -------------------------
class SubExamResponse(SubExamBase):
    id: int
    main_exam_id: int 

    class Config:
        from_attributes = True