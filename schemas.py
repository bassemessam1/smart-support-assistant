# schemas.py
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, Dict, Any


class ActionArgs(BaseModel):
    """
    Strict object for action arguments.
    Users cannot provide unknown fields unless you add them here.
    """
    model_config = ConfigDict(extra="forbid")  # No additional properties


class AIResponse(BaseModel):
    """
    The main response schema validated against LLM output.
    """
    model_config = ConfigDict(extra="forbid")  # Forbid additional fields at root

    response_type: str = Field(..., description="Type of response: action or final")
    final_answer: str = Field(..., description="Message to show to the user")
    action_name: Optional[str] = Field(None, description="Name of the requested action")
    action_args: Optional[Dict[str, Any]] = Field(None, description="Arguments for the action. Must be an object.")


    @classmethod
    def json_schema(cls) -> dict:
        """
        Returns the strict JSON Schema with additionalProperties disabled.
        """
        schema = cls.model_json_schema()
        schema["additionalProperties"] = False
        schema["properties"]["action_args"]["additionalProperties"] = True
        return schema
