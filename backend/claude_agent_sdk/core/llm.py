import os
from typing import Literal, Optional

class ModelRouter:
    """
    Routing logic for Hybrid Model Strategy.
    """
    
    def get_model_name(self, task_type: Literal["reasoning", "coding", "fast"]) -> str:
        """
        Returns the appropriate model name string for Claude Agent SDK.
        """
        if task_type == "reasoning":
            # Complex reasoning/planning -> Claude 3.5 Sonnet (or Opus if available)
            return "claude-3-5-sonnet-20240620"
            
        elif task_type == "coding":
            # Coding/Editing -> Claude 3.5 Sonnet
            return "claude-3-5-sonnet-20240620"
            
        elif task_type == "fast":
            # Fast completion -> Claude 3 Haiku
            return "claude-3-haiku-20240307"
            
        else:
            return "claude-3-5-sonnet-20240620"
