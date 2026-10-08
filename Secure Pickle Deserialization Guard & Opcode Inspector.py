import pickletools
import io
import os
from typing import Tuple

class SecurePickleGuard:
    """
    Inspects Python pickle byte streams for dangerous opcodes (like GLOBAL system calls)
    to prevent Remote Code Execution (RCE) via insecure model deserialization.
    """
    def __init__(self, blocked_modules: list = None):
        if blocked_modules is None:
            # Dangerous modules often exploited in AI model deserialization attacks
            self.blocked_modules = [
                b'os', 
                b'subprocess', 
                b'sys', 
                b'builtins', 
                b'eval', 
                b'exec'
            ]

    def scan_and_validate(self, file_path: str) -> Tuple[bool, str]:
        """
        Reads a pickle file stream and analyzes its opcodes for malicious patterns.
        """
        # Security check: Ensure file exists
        if not os.path.exists(file_path):
            raise FileNotFoundError(f"Critical error: File '{file_path}' not found.")
        
        # Security check: Prevent zero-byte file exploitation
        if os.path.getsize(file_path) == 0:
            raise ValueError("Critical error: Pickle file is empty.")

        try:
            with open(file_path, "rb") as f:
                payload = f.read()

            # Disassemble pickle stream to inspect internal opcodes safely without executing them
            opcodes = list(pickletools.genops(payload))

            for opcode, arg, pos in opcodes:
                # Check if the opcode attempts to reference external global objects/modules
                if opcode.name in ('GLOBAL', 'STACK_GLOBAL') and isinstance(arg, str):
                    module_name = arg.split('.')[0].encode('utf-8')
                    if module_name in self.blocked_modules:
                        return False, f"Security Alert: Malicious RCE attempt detected! Blocked module reference: '{arg}' at position {pos}"

            return True, "Pickle file structure verified. No malicious global calls found."

        except Exception as e:
            raise RuntimeError(f"Error analyzing pickle file: {str(e)}")

if __name__ == "__main__":
    # Example execution: Simulate testing a safe object vs inspecting file structure
    safe_file = "safe_model_weights.pkl"
    try:
        # Create a safe pickled dictionary
        safe_data = {"weights": [0.1, 0.5, 0.9], "version": "1.0"}
        with open(safe_file, "wb") as f:
            pickle.dump(safe_data, f)

        guard = SecurePickleGuard()
        print(f"Evaluating pickle file: '{safe_file}'")
        is_safe, message = guard.scan_and_validate(safe_file)
        print(f"Verification Status - Is Safe: {is_safe}")
        print(f"Details: {message}")

    except Exception as error:
        print(f"Execution failed: {error}")