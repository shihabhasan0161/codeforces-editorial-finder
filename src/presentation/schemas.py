"""Pydantic schemas for API request/response models."""

from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, field_validator


class EditorialRequest(BaseModel):
    """Request schema for editorial endpoint."""

    url: str = Field(..., description="Codeforces problem URL")

    @field_validator("url")
    @classmethod
    def validate_url(cls, v: str) -> str:
        """Validate URL format."""
        if not v.startswith(("http://", "https://")):
            raise ValueError("URL must start with http:// or https://")
        if "codeforces.com" not in v and "codeforces.ru" not in v:
            raise ValueError("URL must be a Codeforces URL")
        return v


class CodeSnippetSchema(BaseModel):
    """Schema for code snippet."""

    language: str = Field(..., description="Programming language")
    code: str = Field(..., description="Code content")
    description: Optional[str] = Field(None, description="Code description")


class EditorialSchema(BaseModel):
    """Schema for editorial data."""

    problem_id: str = Field(..., description="Problem ID")
    solution_text: str = Field(..., description="Full solution text (original editorial)")
    approach: Optional[str] = Field(None, description="Solution approach")
    algorithm: Optional[str] = Field(None, description="Algorithm used")
    time_complexity: Optional[str] = Field(None, description="Time complexity")
    space_complexity: Optional[str] = Field(None, description="Space complexity")
    code_snippets: list[CodeSnippetSchema] = Field(
        default_factory=list, description="Code examples"
    )
    hints: list[str] = Field(default_factory=list, description="Progressive hints")
    notes: Optional[str] = Field(None, description="Additional notes")
    source_url: Optional[str] = Field(None, description="Editorial source URL")
    extracted_at: datetime = Field(..., description="When editorial was extracted")
    ai_model: Optional[str] = Field(None, description="AI model used for extraction")


class ProblemSchema(BaseModel):
    """Schema for problem metadata."""

    contest_id: str = Field(..., description="Contest ID")
    problem_id: str = Field(..., description="Problem ID (letter)")
    title: str = Field(..., description="Problem title")
    url: str = Field(..., description="Problem URL")
    contest_name: Optional[str] = Field(None, description="Contest name")
    tags: list[str] = Field(default_factory=list, description="Problem tags")
    time_limit: Optional[str] = Field(None, description="Time limit")
    memory_limit: Optional[str] = Field(None, description="Memory limit")


class EditorialResponse(BaseModel):
    """Response schema for editorial endpoint."""

    problem: ProblemSchema = Field(..., description="Problem metadata")
    editorial: EditorialSchema = Field(..., description="Editorial content")


class ErrorResponse(BaseModel):
    """Error response schema."""

    status_code: int = Field(..., description="HTTP status code")
    detail: str = Field(..., description="Error message")
    error_type: str = Field(..., description="Error type")
