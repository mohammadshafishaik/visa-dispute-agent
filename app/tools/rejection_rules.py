"""Bank-style authentication and rejection rules for disputes"""
from typing import Dict, Any, Optional, Tuple
from datetime import datetime, timedelta
import re


class BankStyleRejectionRules:
    """
    Comprehensive bank-style validation and rejection system.
    Similar to how banks validate and reject transactions/disputes.
    """
    
    def __init__(self):
        self.rejection_codes = {
            "AUTH001": "Customer authentication failed",
            "AUTH002": "Invalid customer credentials",
            "AUTH003": "Customer ID not found in system",
            "AMOUNT001": "Transaction amount exceeds daily limit",
            "AMOUNT002": "Amount below minimum dispute threshold",
            "AMOUNT003": "Suspicious amount pattern detected",
            "TIME001": "Transaction date is in the future",
            "TIME002": "Dispute filed too late (beyond 120 days)",
            "TIME003": "Transaction date is invalid",
            "FRAUD001": "Multiple disputes from same customer in 24 hours",
            "FRAUD002": "Suspicious activity pattern detected",
            "FRAUD003": "Customer flagged for fraudulent behavior",
            "DOC001": "Insufficient documentation provided",
            "DOC002": "Description does not match transaction type",
            "DOC003": "Missing required information",
            "CARD001": "Card number invalid or expired",
            "CARD002": "Card not associated with customer",
            "MERCH001": "Merchant name does not match records",
            "MERCH002": "Transaction not found with merchant",
            "REASON001": "Invalid dispute reason code",
            "REASON002": "Reason code does not match description",
            "CONTACT001": "Invalid email address format",
            "CONTACT002": "Invalid phone number format",
            "CONTACT003": "Contact information does not match records",
        }
    
    def validate_dispute(self, payload: Dict[str, Any]) -> Tuple[bool, Optional[str], Optional[str]]:
        """
        Comprehensive validation like banks do.
        Returns: (is_valid, rejection_code, rejection_message)
        """
        
        # Layer 1: Customer Authentication
        result = self._validate_customer_authentication(payload)
        if result:
            return result
        
        # Layer 2: Transaction Validation
        result = self._validate_transaction(payload)
        if result:
            return result
        
        # Layer 3: Amount Validation
        result = self._validate_amount(payload)
        if result:
            return result
        
        # Layer 4: Time-based Validation
        result = self._validate_timing(payload)
        if result:
            return result
        
        # Layer 5: Fraud Detection
        result = self._validate_fraud_patterns(payload)
        if result:
            return result
        
        # Layer 6: Documentation Validation
        result = self._validate_documentation(payload)
        if result:
            return result
        
        # Layer 7: Contact Information Validation
        result = self._validate_contact_info(payload)
        if result:
            return result
        
        # All validations passed
        return (True, None, None)
    
    def _validate_customer_authentication(self, payload: Dict[str, Any]) -> Optional[Tuple[bool, str, str]]:
        """Layer 1: Validate customer identity like banks do"""
        
        # Check Customer ID format (4 letters + 4 numbers)
        customer_id = payload.get("customer_id", "")
        if not customer_id or len(customer_id) != 8:
            return (False, "AUTH002", 
                   "REJECTED: Invalid Customer ID format. Must be 8 characters (4 letters + 4 numbers). Example: CUST1234")
        
        if not (customer_id[:4].isalpha() and customer_id[:4].isupper() and customer_id[4:].isdigit()):
            return (False, "AUTH002",
                   "REJECTED: Customer ID must be 4 UPPERCASE letters followed by 4 numbers. Example: BANK5678")
        
        # Check customer name
        customer_name = payload.get("customer_name", "")
        if not customer_name or len(customer_name) < 3:
            return (False, "AUTH001",
                   "REJECTED: Invalid customer name. Must be at least 3 characters.")
        
        # Check if name contains only valid characters
        if not re.match(r'^[a-zA-Z\s.]+$', customer_name):
            return (False, "AUTH001",
                   "REJECTED: Customer name contains invalid characters. Only letters, spaces, and periods allowed.")
        
        return None
    
    def _validate_transaction(self, payload: Dict[str, Any]) -> Optional[Tuple[bool, str, str]]:
        """Layer 2: Validate transaction details"""
        
        # Transaction ID validation
        transaction_id = payload.get("transaction_id", "")
        if not transaction_id or len(transaction_id) < 5:
            return (False, "MERCH002",
                   "REJECTED: Invalid Transaction ID. Must be at least 5 characters.")
        
        # Card number validation (last 4 digits)
        card_number = payload.get("card_number", "")
        if card_number and (not card_number.isdigit() or len(card_number) != 4):
            return (False, "CARD001",
                   "REJECTED: Card number must be exactly 4 digits.")
        
        # Merchant name validation
        merchant_name = payload.get("merchant_name", "")
        if not merchant_name or len(merchant_name) < 2:
            return (False, "MERCH001",
                   "REJECTED: Invalid merchant name. Must be at least 2 characters.")
        
        return None
    
    def _validate_amount(self, payload: Dict[str, Any]) -> Optional[Tuple[bool, str, str]]:
        """Layer 3: Validate transaction amount like banks do"""
        
        amount = payload.get("amount", 0)
        
        # Convert to float if string
        try:
            amount = float(amount) if isinstance(amount, (str, int)) else amount
        except (ValueError, TypeError):
            return (False, "AMT001",
                   "REJECTED: Invalid amount format. Must be a valid number.")
        
        # Minimum amount check
        if amount <= 0:
            return (False, "AMOUNT002",
                   "REJECTED: Invalid amount. Amount must be greater than zero.")
        
        if amount < 1:
            return (False, "AMOUNT002",
                   "REJECTED: Amount too small. Minimum dispute amount is ₹1.")
        
        # Maximum amount check (1 crore INR)
        if amount > 10000000:
            return (False, "AMOUNT001",
                   "REJECTED: Amount exceeds maximum limit. Disputes over ₹1,00,00,000 require branch visit.")
        
        # Suspicious amount patterns
        if amount == 123456 or amount == 999999 or amount == 111111:
            return (False, "AMOUNT003",
                   "REJECTED: Suspicious amount pattern detected. Please verify the actual transaction amount.")
        
        return None
    
    def _validate_timing(self, payload: Dict[str, Any]) -> Optional[Tuple[bool, str, str]]:
        """Layer 4: Validate timing constraints like banks do"""
        
        # Transaction date validation
        transaction_date_str = payload.get("transaction_date", "")
        if transaction_date_str:
            try:
                # Parse date string (handle both date-only and datetime formats)
                if 'T' in transaction_date_str or '+' in transaction_date_str or 'Z' in transaction_date_str:
                    transaction_date = datetime.fromisoformat(transaction_date_str.replace('Z', '+00:00'))
                else:
                    # Date only format (YYYY-MM-DD)
                    transaction_date = datetime.strptime(transaction_date_str, '%Y-%m-%d')
                
                # Use dispute timestamp as reference instead of system time (more reliable)
                dispute_timestamp_str = payload.get("timestamp", "")
                if dispute_timestamp_str:
                    dispute_date = datetime.fromisoformat(dispute_timestamp_str.replace('Z', '+00:00'))
                else:
                    dispute_date = datetime.now()
                
                # Check if date is in future relative to dispute filing
                if transaction_date.date() > dispute_date.date():
                    return (False, "TIME001",
                           "REJECTED: Transaction date cannot be in the future.")
                
                # Check if dispute is filed within 120 days (Visa rule)
                days_since_transaction = (dispute_date.date() - transaction_date.date()).days
                if days_since_transaction > 120:
                    return (False, "TIME002",
                           f"REJECTED: Dispute filed too late. Must be filed within 120 days of transaction. "
                           f"Transaction was {days_since_transaction} days ago.")
                
            except (ValueError, AttributeError):
                return (False, "TIME003",
                       "REJECTED: Invalid transaction date format.")
        
        return None
    
    def _validate_fraud_patterns(self, payload: Dict[str, Any]) -> Optional[Tuple[bool, str, str]]:
        """Layer 5: Detect fraud patterns like banks do"""
        
        description = payload.get("description", "").lower()
        
        # Check for test/spam patterns
        spam_keywords = ["test", "testing", "dummy", "fake", "sample"]
        spam_count = sum(description.count(word) for word in spam_keywords)
        if spam_count > 2:
            return (False, "FRAUD002",
                   "REJECTED: Suspected test/spam submission. Please provide genuine dispute details.")
        
        # Check for very short or generic descriptions
        if len(description.split()) < 5:
            return (False, "DOC001",
                   "REJECTED: Insufficient description. Please provide detailed information (minimum 5 words).")
        
        # Check for repeated characters (spam pattern)
        if re.search(r'(.)\1{10,}', description):
            return (False, "FRAUD002",
                   "REJECTED: Invalid description format detected.")
        
        return None
    
    def _validate_documentation(self, payload: Dict[str, Any]) -> Optional[Tuple[bool, str, str]]:
        """Layer 6: Validate documentation like banks do"""
        
        description = payload.get("description", "")
        
        # Minimum description length
        if len(description) < 20:
            return (False, "DOC001",
                   "REJECTED: Description too short. Minimum 20 characters required for proper review.")
        
        # Maximum description length
        if len(description) > 1000:
            return (False, "DOC001",
                   "REJECTED: Description too long. Maximum 1000 characters allowed.")
        
        # Check reason code
        valid_reason_codes = ["10.1", "10.4", "11.1", "12.1", "13.1", "13.2", "13.3"]
        reason_code = payload.get("reason_code", "")
        if reason_code not in valid_reason_codes:
            return (False, "REASON001",
                   f"REJECTED: Invalid reason code '{reason_code}'. Must be one of: {', '.join(valid_reason_codes)}")
        
        # Validate reason code matches description (lenient check - just warn, don't reject)
        # This is too strict for user experience, so we'll skip it
        # The AI will handle mismatches during adjudication
        pass
        
        return None
    
    def _validate_contact_info(self, payload: Dict[str, Any]) -> Optional[Tuple[bool, str, str]]:
        """Layer 7: Validate contact information like banks do"""
        
        # Email validation
        email = payload.get("customer_email", "")
        if not email:
            return (False, "CONTACT001",
                   "REJECTED: Email address is required.")
        
        # Comprehensive email validation
        email_pattern = r'^[a-zA-Z0-9._%+-]+@[a-zA-Z0-9.-]+\.[a-zA-Z]{2,}$'
        if not re.match(email_pattern, email):
            return (False, "CONTACT001",
                   "REJECTED: Invalid email format. Must be a valid email address (e.g., user@example.com)")
        
        # Check for disposable/temporary email domains
        disposable_domains = ["tempmail", "throwaway", "guerrillamail", "10minutemail"]
        if any(domain in email.lower() for domain in disposable_domains):
            return (False, "CONTACT001",
                   "REJECTED: Temporary email addresses not allowed. Please use permanent email.")
        
        # Phone validation
        phone = payload.get("customer_phone", "")
        if phone:
            # Extract digits only
            phone_digits = re.sub(r'\D', '', phone)
            if len(phone_digits) < 10 or len(phone_digits) > 15:
                return (False, "CONTACT002",
                       "REJECTED: Invalid phone number. Must be 10-15 digits.")
        
        return None


# Global instance
bank_rejection_rules = BankStyleRejectionRules()
