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
        Decrypt vault data using the official Vultisig algorithm from mobile-tss-lib
        
        Args:
            encrypted_data: The encrypted vault binary data
            password: Password string
            
        Returns:
            Decrypted data if successful, None if failed
        """
        
        # Use only the official Vultisig method (matches mobile-tss-lib exactly)
        try:
            result = self._vultisig_aes_gcm_sha256(encrypted_data, password)
            if result and self.validate_decrypted_data(result):
                if not self.silent:
                    print(f"✅ Decryption successful using official Vultisig method", file=sys.stderr)
                return result
        except Exception as e:
            if not self.silent:
                print(f"❌ Decryption failed: {e}", file=sys.stderr)
        
        return None
    
    def _vultisig_aes_gcm_sha256(self, data: bytes, password: str) -> Optional[bytes]:
        """
        Official Vultisig decryption method (exact match to mobile-tss-lib Go implementation):
        
        Go code equivalent:
        hash := sha256.Sum256([]byte(password))
        key := hash[:]
        block, err := aes.NewCipher(key)
        gcm, err := cipher.NewGCM(block)
        nonceSize := gcm.NonceSize()
        nonce, ciphertext := vault[:nonceSize], vault[nonceSize:]
        plaintext, err := gcm.Open(nil, nonce, ciphertext, nil)
        """
        
        # Hash the password to create a key (matches Go: hash := sha256.Sum256([]byte(password)))
        key = hashlib.sha256(password.encode()).digest()
        
        # Create a new AES cipher using the key (matches Go: aes.NewCipher(key))
        # Use GCM mode (matches Go: cipher.NewGCM(block))
        # Get the nonce size (matches Go: gcm.NonceSize())
        # Standard GCM nonce size is 12 bytes
        nonce_size = 12
        
        if len(data) < nonce_size:
            raise ValueError("ciphertext too short")
        
        # Extract the nonce from the vault (matches Go: nonce, ciphertext := vault[:nonceSize], vault[nonceSize:])
        nonce = data[:nonce_size]
        ciphertext = data[nonce_size:]
        
        # Decrypt the vault (Python equivalent of Go's gcm.Open)
        # In Go's GCM, the tag is automatically handled by gcm.Open
        # In Python's cryptography library, we need to separate the tag manually
        if len(ciphertext) < 16:
            raise ValueError("ciphertext too short for GCM tag")
            
        # The authentication tag is the last 16 bytes
        actual_ciphertext = ciphertext[:-16]
        tag = ciphertext[-16:]
        
        # Create cipher with GCM mode (this is the Python equivalent of Go's gcm.Open)
        cipher = Cipher(algorithms.AES(key), modes.GCM(nonce, tag), backend=default_backend())
        decryptor = cipher.decryptor()
        
        # Decrypt and verify (matches Go's gcm.Open behavior)
        plaintext = decryptor.update(actual_ciphertext) + decryptor.finalize()
        
        return plaintext
    
    
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
