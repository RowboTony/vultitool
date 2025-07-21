#!/usr/bin/env python3
"""
VultIsig .vult File Parser using Official Protobuf Schema
Parses .vult files using the exact protobuf definitions from VultIsig's commondata repo
"""

import base64
import sys
import json
from pathlib import Path

# Add generated protobuf path
sys.path.insert(0, str(Path(__file__).parent / "generated"))

from vultisig.vault.v1.vault_container_pb2 import VaultContainer
from vultisig.vault.v1.vault_pb2 import Vault
from vultisig.keygen.v1.lib_type_message_pb2 import LibType

def parse_vult_file(file_path):
    """Parse a .vult file using proper protobuf definitions"""
    
    print(f"=== Parsing {file_path} ===")
    
    # Read and decode the file
    try:
        with open(file_path, 'r') as f:
            base64_content = f.read().strip()
        
        print(f"Base64 content length: {len(base64_content)} characters")
        
        # Decode base64
        binary_data = base64.b64decode(base64_content)
        print(f"Decoded binary length: {len(binary_data)} bytes")
        
    except Exception as e:
        print(f"ERROR reading/decoding file: {e}")
        return False
    
    # Try to parse as VaultContainer first (this is the outer wrapper)
    try:
        container = VaultContainer()
        container.ParseFromString(binary_data)
        
        print("\n=== VaultContainer ===")
        print(f"Version: {container.version}")
        print(f"Is Encrypted: {container.is_encrypted}")
        print(f"Vault data length: {len(container.vault)} characters")
        
        # The vault field contains another base64-encoded protobuf (the actual Vault)
        if container.vault:
            try:
                vault_binary = base64.b64decode(container.vault)
                print(f"Vault binary length: {len(vault_binary)} bytes")
                
                # Parse the inner Vault message
                vault = Vault()
                vault.ParseFromString(vault_binary)
                
                print("\n=== Vault Details ===")
                print(f"Name: '{vault.name}'")
                print(f"Public Key ECDSA: {vault.public_key_ecdsa}")
                print(f"Public Key EdDSA: {vault.public_key_eddsa}")
                print(f"Local Party ID: {vault.local_party_id}")
                print(f"Hex Chain Code: {vault.hex_chain_code}")
                print(f"Reshare Prefix: {vault.reshare_prefix}")
                
                # Lib Type
                lib_type_name = "UNKNOWN"
                if vault.lib_type == LibType.LIB_TYPE_GG20:
                    lib_type_name = "GG20"
                elif vault.lib_type == LibType.LIB_TYPE_DKLS:
                    lib_type_name = "DKLS"
                print(f"Lib Type: {lib_type_name} ({vault.lib_type})")
                
                # Signers
                print(f"Signers ({len(vault.signers)}):")
                for i, signer in enumerate(vault.signers):
                    print(f"  {i+1}: {signer}")
                
                # Created timestamp
                if vault.HasField('created_at'):
                    timestamp = vault.created_at
                    print(f"Created: {timestamp.seconds}.{timestamp.nanos}")
                
                # Key Shares
                print(f"Key Shares ({len(vault.key_shares)}):")
                for i, key_share in enumerate(vault.key_shares):
                    print(f"  Share {i+1}:")
                    print(f"    Public Key: {key_share.public_key}")
                    print(f"    Key Share Length: {len(key_share.keyshare)} chars")
                    
                    # Try to decode the keyshare if it looks like base64/JSON
                    if key_share.keyshare:
                        try:
                            decoded_keyshare = base64.b64decode(key_share.keyshare)
                            decoded_str = decoded_keyshare.decode('utf-8')
                            # Try to parse as JSON
                            keyshare_data = json.loads(decoded_str)
                            print(f"    Key Share Data: {json.dumps(keyshare_data, indent=2)[:200]}...")
                        except:
                            print(f"    Key Share Data: [binary/encrypted data]")
                
                return True
                
            except Exception as e:
                print(f"ERROR parsing inner Vault: {e}")
                return False
        
    except Exception as e:
        print(f"ERROR parsing VaultContainer: {e}")
        return False

def main():
    if len(sys.argv) != 2:
        print("Usage: python3 parse_vult_protobuf.py <file.vult>")
        sys.exit(1)
    
    file_path = sys.argv[1]
    
    if not Path(file_path).exists():
        print(f"ERROR: File {file_path} does not exist")
        sys.exit(1)
    
    success = parse_vult_file(file_path)
    
    if not success:
        sys.exit(1)

if __name__ == "__main__":
    main()
