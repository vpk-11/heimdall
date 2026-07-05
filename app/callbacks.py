import re
from typing import Optional
from google.adk.agents.callback_context import CallbackContext
from google.adk.models.llm_request import LlmRequest
from google.adk.models.llm_response import LlmResponse
from google.genai import types

# Regex patterns for PII detection
EMAIL_REGEX = re.compile(r'[a-zA-Z0-9_.+-]+@[a-zA-Z0-9-]+\.[a-zA-Z0-9-.]+')
PHONE_REGEX = re.compile(r'\b(?:\+?\d{1,3}[-.\s]?)?\(?\d{3}\)?[-.\s]?\d{3}[-.\s]?\d{4}\b')
ADDRESS_REGEX = re.compile(
    r'\b\d+[ \t]+[A-Za-z0-9][A-Za-z0-9 \t\.,]{0,40}(?:Street|St|Avenue|Ave|Road|Rd|Highway|Hwy|Boulevard|Blvd|Drive|Dr|Lane|Ln|Court|Ct|Circle|Cir|Way|Suite|Ste|Apt)\b',
    re.IGNORECASE
)
NAME_PATTERNS = [
    re.compile(r'\bmy name is\s+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', re.IGNORECASE),
    re.compile(r'\bcontact:\s*([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', re.IGNORECASE),
    re.compile(r'\b(?:Sincerely|Regards|Best|Best regards|Thanks|Thank you|From),?\s*\n+([A-Z][a-z]+(?:\s+[A-Z][a-z]+)?)\b', re.IGNORECASE)
]

# Injection patterns
INJECTION_KEYWORDS = [
    "ignore previous instructions",
    "ignore system instructions",
    "ignore the system prompt",
    "system override",
    "you must now",
    "ignore the above",
    "jailbreak",
    "new instructions:",
    "do not look up"
]

def redact_text(text: str) -> str:
    """Redacts PII (email, phone, address, and name patterns) from text."""
    if not text:
        return text
    
    # Redact email
    text = EMAIL_REGEX.sub("[EMAIL_REDACTED]", text)
    
    # Redact phone
    text = PHONE_REGEX.sub("[PHONE_REDACTED]", text)
    
    # Redact address
    text = ADDRESS_REGEX.sub("[ADDRESS_REDACTED]", text)
    
    # Redact common name signature patterns
    for pattern in NAME_PATTERNS:
        match = pattern.search(text)
        if match:
            # We replace only the name group
            name = match.group(1)
            text = text.replace(name, "[NAME_REDACTED]")
            
    return text

def detect_injection(text: str) -> bool:
    """Detects common prompt injection keyword phrases."""
    if not text:
        return False
    lower_text = text.lower()
    for kw in INJECTION_KEYWORDS:
        if kw in lower_text:
            return True
    return False

def before_model_callback(
    *, callback_context: CallbackContext, llm_request: LlmRequest
) -> Optional[LlmResponse]:
    """Runs before the LLM call.
    
    Redacts PII from the raw inquiry text before it reaches the LLM.
    Screens for prompt-injection patterns. If injection is detected,
    short-circuits and returns a flagged/rejected response.
    """
    _ = callback_context
    
    for content in llm_request.contents:
        for part in content.parts:
            text = getattr(part, "text", None)
            if text:
                if detect_injection(text):
                    # Short-circuit by returning a security failure response
                    return LlmResponse(
                        content=types.Content(
                            parts=[
                                types.Part(
                                    text="[SECURITY ALERT] Inquiry rejected due to security policy violation: potential prompt injection detected."
                                )
                            ],
                            role="model"
                        )
                    )
                # Mutate in-place to redact PII
                part.text = redact_text(text)
                
    return None

def after_model_callback(
    *,
    callback_context: CallbackContext,
    llm_response: LlmResponse,
) -> Optional[LlmResponse]:
    """Runs after the LLM call.
    
    Checks the drafted response for leaked PII or policy violations (e.g., auto-acting).
    Ensures output is clean and formatted as a draft.
    """
    _ = callback_context
    
    if not llm_response or not llm_response.content or not llm_response.content.parts:
        return llm_response

    updated_parts = []
    for part in llm_response.content.parts:
        text = getattr(part, "text", None)
        if text:
            # Make sure no PII leaked into the output
            cleaned_text = redact_text(text)
            
            # Policy guardrail: ensure model doesn't imply it executed any action directly
            # e.g., "I have sent the email" -> replace or warn
            auto_action_phrases = ["sent the email", "emailed the customer", "sent the response", "updated the crm"]
            flagged = False
            for phrase in auto_action_phrases:
                if phrase in cleaned_text.lower():
                    flagged = True
                    break
            
            if flagged:
                cleaned_text = "[POLICY WARNING] The draft response was flagged for attempting to execute an automatic external action. Re-evaluating...\n\n" + cleaned_text
            
            updated_parts.append(types.Part(text=cleaned_text))
        else:
            updated_parts.append(part)

    llm_response.content = types.Content(
        parts=updated_parts,
        role=llm_response.content.role
    )
    return llm_response
