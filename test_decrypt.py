#!/usr/bin/env python3
"""
Test script for decrypting password-protected vault files
"""

import base64
import sys
from pathlib import Path

# Add generated protobuf path and commands path
sys.path.insert(0, str(Path(__file__).parent / "generated"))
sys.path.insert(0, str(Path(__file__).parent / "commands"))

from vultisig.vault.v1.vault_container_pb2 import VaultContainer
from vultisig.vault.v1.vault_pb2 import Vault
from crypto_fixed import VaultDecryptor

def test_decrypt_vault(vault_path: str, password: str):
    """Test decrypting a vault file"""
    
    print(f"🔓 Testing decryption of {vault_path}")
    print(f"🔑 Using password: {password}")
    print()
    
    # Load the vault container
    try:
        with open(vault_path, 'r') as f:
            base64_content = f.read().strip()
        
        binary_data = base64.b64decode(base64_content)
        
        container = VaultContainer()
        container.ParseFromString(binary_data)
        
        print(f"📦 Container info:")
        print(f"   Version: {container.version}")
        print(f"   Is Encrypted: {container.is_encrypted}")
        print(f"   Vault data length: {len(container.vault)} characters")
        print()
        
        if not container.is_encrypted:
            print("⚠️  Vault is not encrypted - no decryption needed")
            return
            
        # Get encrypted vault data
        encrypted_vault_data = base64.b64decode(container.vault)
        print(f"🔒 Encrypted vault binary length: {len(encrypted_vault_data)} bytes")
        print(f"🔒 First 32 bytes (hex): {encrypted_vault_data[:32].hex()}")
        print()
        
        # Try to decrypt
        print("🔄 Attempting decryption...")
        decryptor = VaultDecryptor()
        
        decrypted_data = decryptor.decrypt_vault_data(encrypted_vault_data, password)
        
        if decrypted_data:
            print(f"✅ Decryption successful!")
            print(f"📊 Decrypted data length: {len(decrypted_data)} bytes")
            print(f"📊 First 32 bytes (hex): {decrypted_data[:32].hex()}")
            print()
            
            # Validate the decrypted data
            if decryptor.validate_decrypted_data(decrypted_data):
                print("✅ Decrypted data appears valid")
                
                # Try to parse as Vault protobuf
                try:
                    vault = Vault()
                    vault.ParseFromString(decrypted_data)
                    
                    print(f"🎉 Successfully parsed decrypted vault!")
                    print(f"   Name: {vault.name}")
                    print(f"   Public Key ECDSA: {vault.public_key_ecdsa}")
                    print(f"   Signers: {len(vault.signers)}")
                    print(f"   Key Shares: {len(vault.key_shares)}")
                    
                except Exception as e:
                    print(f"❌ Failed to parse as Vault protobuf: {e}")
                    
            else:
                print("❌ Decrypted data validation failed")
        else:
            print("❌ Decryption failed - none of the methods worked")
            print("💡 This might indicate:")
            print("   - Wrong password")
            print("   - Unknown encryption scheme")
            print("   - Data corruption")
        
    except Exception as e:
        print(f"❌ Error processing vault: {e}")

if __name__ == "__main__":
    # Test with the known encrypted vault
    vault_path = "tests/fixtures/vulticli01-share2of2.vult"
    password = "vulticli01"
    
    test_decrypt_vault(vault_path, password)
