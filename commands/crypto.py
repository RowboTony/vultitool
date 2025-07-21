"""
Cryptographic utilities for vultitool
Handles password-based decryption of .vult files
"""

import base64
import hashlib
import sys
from typing import Optional
from pathlib import Path

try:
    from cryptography.hazmat.primitives.ciphers import Cipher, algorithms, modes
    from cryptography.hazmat.primitives.kdf.pbkdf2 import PBKDF2HMAC
    from cryptography.hazmat.primitives.kdf.scrypt import Scrypt
    from cryptography.hazmat.primitives import hashes
    from cryptography.hazmat.backends import default_backend
    CRYPTO_AVAILABLE = True
except ImportError:
    CRYPTO_AVAILABLE = False


class VaultDecryptor:
    """Handles decryption of password-protected vault files"""
    
    def __init__(self, silent=False):
        if not CRYPTO_AVAILABLE:
            raise ImportError("cryptography library not available. Install with: pip install cryptography")
        self.silent = silent
    
    def decrypt_vault_data(self, encrypted_data: bytes, password: str) -> Optional[bytes]:
        """
        Decrypt vault data using the official VultIsig algorithm
        
        Args:
            encrypted_data: The encrypted vault binary data
            password: Password string
            
        Returns:
            Decrypted data if successful, None if failed
        """
        
        # Try the official VultIsig method first
        try:
            result = self._vultisig_aes_gcm_sha256(encrypted_data, password)
            if result and self.validate_decrypted_data(result):
                if not self.silent:
                    print(f"✅ Decryption successful using official VultIsig method", file=sys.stderr)
                return result
        except Exception as e:
            if not self.silent:
                print(f"🔄 Official VultIsig method failed: {e}", file=sys.stderr)
        
        # Try other common methods as fallback
        methods = [
            self._try_aes_cbc_pbkdf2,
            self._try_simple_aes_sha256,
        ]
        
        for method in methods:
            try:
                result = method(encrypted_data, password)
                if result and self.validate_decrypted_data(result):
                    if not self.silent:
                        print(f"✅ Decryption successful using {method.__name__}", file=sys.stderr)
                    return result
            except Exception as e:
                if not self.silent:
                    print(f"🔄 {method.__name__} failed: {e}", file=sys.stderr)
                continue
        
        return None
    
    def _vultisig_aes_gcm_sha256(self, data: bytes, password: str) -> Optional[bytes]:
        """
        Official VultIsig decryption method:
        - SHA256 hash of password as key
        - AES-GCM encryption
        - Nonce at beginning of data
        """
        
        # Create key by hashing password with SHA256
        key = hashlib.sha256(password.encode()).digest()
        
        # Get nonce size for GCM (typically 12 bytes)
        nonce_size = 12  # GCM standard nonce size
        
        if len(data) < nonce_size:
            raise ValueError("Ciphertext too short")
        
        # Extract nonce and ciphertext
        nonce = data[:nonce_size]
        ciphertext = data[nonce_size:]
        
        # In GCM, the authentication tag is usually the last 16 bytes of ciphertext
        if len(ciphertext) < 16:
            raise ValueError("Ciphertext too short for GCM tag")
            
        # Split ciphertext and tag
        actual_ciphertext = ciphertext[:-16]
        tag = ciphertext[-16:]
        
        # Create decryptor with the nonce and tag
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt
        plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        
        return plaintext
    
    def _try_aes_cbc_pbkdf2(self, data: bytes, password: str) -> Optional[bytes]:
        """Try AES-CBC with PBKDF2 key derivation"""
        
        if len(data) < 48:  # salt (16) + iv (16) + min ciphertext (16)
            return None
            
        salt = data[:16]
        iv = data[16:32]
        ciphertext = data[32:]
        
        # Derive key using PBKDF2
        kdf = PBKDF2HMAC(
            algorithm=hashes.SHA256(),
            length=32,
            salt=salt,
            iterations=10000,
            backend=default_backend()
        )
        key = kdf.derive(password.encode())
        
        # Decrypt
        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()
        
        # Remove PKCS7 padding
        padding_length = decrypted[-1]
        return decrypted[:-padding_length]
    
    def _try_simple_aes_sha256(self, data: bytes, password: str) -> Optional[bytes]:
        """Try simple AES with SHA256 password hashing (less secure but sometimes used)"""
        
        if len(data) < 32:  # iv (16) + min ciphertext (16)
            return None
            
        iv = data[:16]
        ciphertext = data[16:]
        
        # Simple key derivation
        key = hashlib.sha256(password.encode()).digest()

        # Pad ciphertext if necessary
        padding_needed = len(ciphertext) % 16
        if padding_needed != 0:
            ciphertext += bytes([0] * (16 - padding_needed))

        cipher = Cipher(algorithms.AES(key), modes.CBC(iv), backend=default_backend())
        decryptor = cipher.decryptor()
        decrypted = decryptor.update(ciphertext) + decryptor.finalize()

        # Try to remove padding
        try:
            padding_length = decrypted[-1]
            if padding_length <= 16:
                return decrypted[:-padding_length]
        except:
            pass

        return decrypted
    
    def validate_decrypted_data(self, data: bytes) -> bool:
        """
        Validate that decrypted data looks like a valid protobuf Vault message
        """
        if not data or len(data) < 10:
            return False
        
        # Check if it starts with protobuf field markers
        # Vault messages typically start with field tags
        first_byte = data[0]
        if first_byte in [0x08, 0x0A, 0x10, 0x12, 0x18, 0x1A, 0x20, 0x22]:
            return True
        
        # Check for JSON-like structure (some vault data is JSON)
        try:
            text = data.decode('utf-8')
            if text.strip().startswith('{'):
                return True
        except:
            pass
            
        return False
