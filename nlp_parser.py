import re
from typing import Dict, Optional

class CommandParser:
    """Natural language command parser for email sending instructions"""
    
    def __init__(self):
        self.email_pattern = r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b'
        self.command_keywords = ['send', 'email', 'mail']
    
    def parse_command(self, text: str) -> Dict[str, Optional[str]]:
        if not text or not isinstance(text, str):
            return self._default_response()
        
        text_lower = text.lower().strip()
        intent = 'send_email' if any(kw in text_lower for kw in self.command_keywords) else 'unknown'
        
        if intent != 'send_email':
            return self._default_response()
        
        to_email = self._extract_email(text)
        subject = self._extract_subject(text)
        body = self._extract_body(text, to_email)
        
        return {
            "intent": intent,
            "to": to_email,
            "subject": subject or "No Subject",
            "body": body or "",
            "language": self._detect_language(text)
        }
    
    def _extract_email(self, text: str) -> Optional[str]:
        matches = re.findall(self.email_pattern, text)
        return matches[0] if matches else None
    
    def _extract_subject(self, text: str) -> Optional[str]:
        patterns = [
            r'subject[:\s]+(.+?)(?:\bbody[:\s]+|$)',
            r'title[:\s]+(.+?)(?:\bmessage[:\s]+|$)',
        ]
        for pattern in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip()
        return None
    
    def _extract_body(self, text: str, email: Optional[str]) -> Optional[str]:
        patterns = [
            (r'body[:\s]+(.+)$', True),
            (r'message[:\s]+(.+)$', True),
            (r'content[:\s]+(.+)$', True),
            (r'saying\s+(.+)$', True),
        ]
        for pattern, use_group in patterns:
            match = re.search(pattern, text, flags=re.IGNORECASE)
            if match:
                return match.group(1).strip() if use_group else match.group(0)
        
        if email:
            parts = text.split(email, 1)
            if len(parts) > 1 and parts[1].strip():
                return parts[1].strip()
        return None
    
    def _detect_language(self, text: str) -> str:
        return 'english'
    
    def _default_response(self):
        return {
            "intent": "unknown",
            "to": None,
            "subject": None,
            "body": None,
            "language": "unknown"
        }
