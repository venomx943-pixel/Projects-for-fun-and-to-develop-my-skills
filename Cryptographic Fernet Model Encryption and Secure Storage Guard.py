from cryptography.fernet import Fernet
import os
from typing import Tuple

class SecureModelEncryptionGuard:
    """
    Encrypts and decrypts machine learning model files at rest using Fernet symmetric encryption
    to prevent unauthorized model theft and data exfiltration from servers.
    """
    def __init__(self, encryption_key: bytes = None):
        # Generate or accept a secure Fernet master key
        self.key = encryption_key if encryption_key else Fernet.generate_key()
        self.cipher_suite = Fernet(self.key)

    def get_master_key(self) -> bytes:
        """Exports the master key for secure environment storage."""
        return self.key

    def encrypt_model_file(self, target_file_path: str, output_encrypted_path: str) -> Tuple[bool, str]:
        """
        Encrypts a raw model file into a secure cipher-text file.
        """
        if not os.path.exists(target_file_path):
            raise FileNotFoundError(f"Critical error: Target model file '{target_file_path}' not found.")
        
        if os.path.getsize(target_file_path) == 0:
            raise ValueError("Critical error: Target model file is empty.")

        try:
            with open(target_file_path, "rb") as f:
                raw_data = f.read()

            # Encrypt model binary bytes securely
            encrypted_data = self.cipher_suite.encrypt(raw_data)

            with open(output_encrypted_path, "wb") as f:
                f.write(encrypted_data)

            return True, f"Model file successfully encrypted and saved to '{output_encrypted_path}'."

        except Exception as e:
            raise RuntimeError(f"Encryption failed: {str(e)}")

    def decrypt_model_file(self, encrypted_file_path: str) -> bytes:
        """
        Decrypts an encrypted model file securely in-memory for model loading.
        """
        if not os.path.exists(encrypted_file_path):
            raise FileNotFoundError(f"Critical error: Encrypted model file '{encrypted_file_path}' not found.")

        try:
            with open(encrypted_file_path, "rb") as f:
                encrypted_data = f.read()

            # Decrypt back into original raw binary model data
            decrypted_data = self.cipher_suite.decrypt(encrypted_data)
            return decrypted_data

        except Exception as e:
            raise RuntimeError(f"Security Alert: Decryption failed. Invalid key or tampered model file! Details: {str(e)}")

if __name__ == "__main__":
    raw_model_file = "raw_model_weights.bin"
    encrypted_model_file = "secure_encrypted_model.enc"

    try:
        # Create a dummy model weights file for simulation
        with open(raw_model_file, "wb") as f:
            f.write(b"confidential_neural_network_weights_v2.0")

        # Initialize encryption guard
        guard = SecureModelEncryptionGuard()
        print("Initialized Secure Encryption Guard.")

        # Encrypt the model file
        is_success, msg = guard.encrypt_model_file(raw_model_file, encrypted_model_file)
        print(msg)

        # Decrypt safely in memory
        restored_weights = guard.decrypt_model_file(encrypted_model_file)
        print(f"Successfully decrypted model weights in-memory: {restored_weights}")

    except Exception as error:
        print(f"Execution failed: {error}")