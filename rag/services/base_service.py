"""
Base API service for the Physical AI RAG Chatbot.
"""
from typing import Any, Dict, Optional
import logging
from datetime import datetime


class BaseAPIService:
    """
    Base class for API services providing common functionality.
    """
    def __init__(self):
        self.logger = logging.getLogger(self.__class__.__name__)
        self.created_at = datetime.now()

    def handle_error(self, error: Exception, context: str = "") -> Dict[str, Any]:
        """
        Standardized error handling for API services.

        Args:
            error: The exception that occurred
            context: Additional context about where the error occurred

        Returns:
            Dictionary with error information formatted for API responses
        """
        error_msg = str(error)
        self.logger.error(f"Error in {context}: {error_msg}", exc_info=True)

        return {
            "status": "error",
            "message": error_msg,
            "timestamp": datetime.now().isoformat(),
            "context": context
        }

    def validate_input(self, data: Dict[str, Any], required_fields: list) -> Optional[Dict[str, Any]]:
        """
        Validate input data contains required fields.

        Args:
            data: Input data dictionary
            required_fields: List of required field names

        Returns:
            Error response if validation fails, None if validation passes
        """
        missing_fields = []
        for field in required_fields:
            if field not in data or data[field] is None:
                missing_fields.append(field)

        if missing_fields:
            return {
                "status": "error",
                "message": f"Missing required fields: {', '.join(missing_fields)}",
                "missing_fields": missing_fields
            }

        return None

    def format_response(self, data: Any, success: bool = True, message: str = "") -> Dict[str, Any]:
        """
        Standardized response formatting.

        Args:
            data: Response data
            success: Whether the operation was successful
            message: Optional message to include in response

        Returns:
            Formatted response dictionary
        """
        response = {
            "status": "success" if success else "error",
            "data": data,
            "timestamp": datetime.now().isoformat()
        }

        if message:
            response["message"] = message

        return response