import re
from colorama import Fore, Style
import string
from collections import Counter
import math

class PasswordStrengthChecker:
    def __init__(self):
        # Common password patterns to check against
        self.common_patterns = [
            r'123[45678]',
            r'password',
            r'qwerty',
            r'admin',
            r'letmein',
            r'welcome',
            r'abc[123456789]',
        ]
        
        # Load common passwords list
        self.common_passwords = {
            'password123',
            'admin123',
            '12345678',
            'qwerty123',
            # Add more common passwords here
        }
        
        # Minimum requirements
        self.MIN_LENGTH = 8
        self.MIN_UNIQUE_CHARS = 5
        
    def print_colored(self, message, color):
        """Print messages with specified colors."""
        print(color + message + Style.RESET_ALL)

    def calculate_entropy(self, password):
        """Calculate password entropy (randomness)."""
        char_frequencies = Counter(password)
        length = len(password)
        entropy = 0
        
        for count in char_frequencies.values():
            probability = count / length
            if probability > 0:
                entropy -= probability * math.log2(probability)
        
        return entropy
    def check_sequential_characters(self, password):
        """Check for sequential characters (e.g., 'abc', '123')."""
        # Check numbers
        for i in range(len(password) - 2):
            if password[i:i+3].isdigit():
                if int(password[i+1]) == int(password[i]) + 1 and int(password[i+2]) == int(password[i]) + 2:
                    return True
                
        # Check letters
        alpha = string.ascii_lowercase
        password_lower = password.lower()
        for i in range(len(password) - 2):
            if password_lower[i:i+3] in alpha:
                return True
                
        return False

    def check_repeating_characters(self, password):
        """Check for repeating characters (e.g., 'aaa', '111')."""
        for i in range(len(password) - 2):
            if password[i] == password[i+1] == password[i+2]:
                return True
        return False

    def check_keyboard_patterns(self, password):
        """Check for keyboard patterns (e.g., 'qwerty', 'asdfgh')."""
        keyboard_rows = [
            'qwertyuiop',
            'asdfghjkl',
            'zxcvbnm'
        ]
        
        password_lower = password.lower()
        for row in keyboard_rows:
            for i in range(len(row) - 2):
                if row[i:i+3] in password_lower:
                    return True
        return False

    def check_password_strength(self, password):
        """Check the strength of the password with enhanced criteria."""
        strength = 0
        feedback = []
        
        # Basic checks
        if len(password) >= self.MIN_LENGTH:
            strength += 1
        else:
            feedback.append(f"Password should be at least {self.MIN_LENGTH} characters long.")

        # Character diversity checks
        has_upper = bool(re.search(r'[A-Z]', password))
        has_lower = bool(re.search(r'[a-z]', password))
        has_digit = bool(re.search(r'\d', password))
        has_special = bool(re.search(r'[!@#$%^&*(),.?":{}|<>]', password))
        
        if has_upper and has_lower:
            strength += 1
        else:
            feedback.append("Password should include both uppercase and lowercase letters.")
            
        if has_digit:
            strength += 1
        else:
            feedback.append("Password should include at least one number.")
            
        if has_special:
            strength += 1
        else:
            feedback.append("Password should include at least one special character.")

        # Advanced checks
        if len(set(password)) >= self.MIN_UNIQUE_CHARS:
            strength += 1
        else:
            feedback.append(f"Password should have at least {self.MIN_UNIQUE_CHARS} unique characters.")

        # Check for common patterns
        for pattern in self.common_patterns:
            if re.search(pattern, password.lower()):
                strength -= 1
                feedback.append("Password contains a common pattern.")
                break

        # Check for sequential characters
        if self.check_sequential_characters(password):
            strength -= 1
            feedback.append("Password contains sequential characters.")

        # Check for repeating characters
        if self.check_repeating_characters(password):
            strength -= 1
            feedback.append("Password contains repeating characters.")

        # Check for keyboard patterns
        if self.check_keyboard_patterns(password):
            strength -= 1
            feedback.append("Password contains keyboard patterns.")

        # Check if password is in common passwords list
        if password.lower() in self.common_passwords:
            strength = 0
            feedback.append("Password is too common.")

        # Calculate entropy bonus
        entropy = self.calculate_entropy(password)
        if entropy > 3:
            strength += 1

        # Determine overall strength
        if strength >= 5:
            return "Strong password! Great job!", feedback
        elif strength >= 3:
            return "Moderate password. Consider improving it.", feedback
        else:
            return "Weak password. You should change it.", feedback

def main():
    checker = PasswordStrengthChecker()
    
    while True:
        print("\nPassword Strength Checker")
        print("-" * 25)
        user_password = input("Enter a password to check its strength (or 'q' to quit): ")
        
        if user_password.lower() == 'q':
            break
            
        result, suggestions = checker.check_password_strength(user_password)
        
        # Print password strength with color
        if "Strong" in result:
            checker.print_colored("\nPassword Strength: " + result, Fore.GREEN)
        elif "Moderate" in result:
            checker.print_colored("\nPassword Strength: " + result, Fore.YELLOW)
        else:
            checker.print_colored("\nPassword Strength: " + result, Fore.RED)
        
        # Provide suggestions if available
        if suggestions:
            print("\nSuggestions to improve your password:")
            for tip in suggestions:
                print("- " + tip)

if __name__ == "__main__":
    main()