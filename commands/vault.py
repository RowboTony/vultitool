"""
Vault command implementations for vultitool
Handles all vault-related operations: parse, inspect, validate, export
"""

import base64
import sys
import json
import yaml
from pathlib import Path
from datetime import datetime

# Add generated protobuf path
sys.path.insert(0, str(Path(__file__).parent.parent / "generated"))

from vultisig.vault.v1.vault_container_pb2 import VaultContainer
from vultisig.vault.v1.vault_pb2 import Vault
from vultisig.keygen.v1.lib_type_message_pb2 import LibType

class VaultCommands:
    @staticmethod
    def setup_parser(parser):
        """Setup vault command parser with subcommands"""
        subparsers = parser.add_subparsers(dest='vault_action', help='Vault operations')
        
        # Parse command
        parse_parser = subparsers.add_parser('parse', help='Parse and display vault contents')
        parse_parser.add_argument('file', help='Path to .vult file')
        parse_parser.add_argument('--json', action='store_true', help='Output as JSON')
        parse_parser.add_argument('--summary', action='store_true', help='Brief summary only')
        parse_parser.add_argument('--verbose', '-v', action='store_true', help='Verbose output')
        
        # Inspect command  
        inspect_parser = subparsers.add_parser('inspect', help='Detailed vault inspection')
        inspect_parser.add_argument('file', help='Path to .vult file')
        inspect_parser.add_argument('--show-keyshares', action='store_true', help='Show key share data (sensitive!)')
        
        # Validate command
        validate_parser = subparsers.add_parser('validate', help='Validate vault format')
        validate_parser.add_argument('file', help='Path to .vult file')
        validate_parser.add_argument('--strict', action='store_true', help='Strict validation')
        
        # Export command
        export_parser = subparsers.add_parser('export', help='Export vault data')
        export_parser.add_argument('file', help='Path to .vult file')
        export_parser.add_argument('output', help='Output file path')
        export_parser.add_argument('--format', choices=['json', 'yaml'], default='json', help='Output format')
    
    @staticmethod
    def handle(args):
        """Route vault commands to appropriate handlers"""
        if args.vault_action == 'parse':
            return VaultCommands.parse(args)
        elif args.vault_action == 'inspect':
            return VaultCommands.inspect(args)
        elif args.vault_action == 'validate':
            return VaultCommands.validate(args)
        elif args.vault_action == 'export':
            return VaultCommands.export(args)
        else:
            print("No vault action specified. Use --help for usage.")
            return 1
    
    @staticmethod
    def parse(args):
        """Parse and display vault contents"""
        try:
            vault_data = VaultCommands._load_vault(args.file)
            if not vault_data:
                return 1
                
            if args.json:
                print(json.dumps(vault_data, indent=2))
            elif args.summary:
                VaultCommands._print_summary(vault_data)
            else:
                VaultCommands._print_detailed(vault_data, args.verbose)
            
            return 0
        except Exception as e:
            print(f"Error parsing vault: {e}")
            return 1
    
    @staticmethod
    def inspect(args):
        """Detailed vault inspection"""
        try:
            vault_data = VaultCommands._load_vault(args.file)
            if not vault_data:
                return 1
            
            VaultCommands._print_detailed(vault_data, verbose=True)
            
            if args.show_keyshares:
                print("\n⚠️  KEY SHARE DATA (SENSITIVE!) ⚠️")
                for i, share in enumerate(vault_data.get('key_shares', [])):
                    print(f"Share {i+1} Data: {share.get('keyshare_data', '[encrypted]')}")
            
            return 0
        except Exception as e:
            print(f"Error inspecting vault: {e}")
            return 1
    
    @staticmethod
    def validate(args):
        """Validate vault format"""
        try:
            vault_data = VaultCommands._load_vault(args.file)
            if not vault_data:
                return 1
            
            issues = []
            
            # Basic validation
            if not vault_data.get('vault', {}).get('name'):
                issues.append("Missing vault name")
            
            if not vault_data.get('vault', {}).get('public_key_ecdsa'):
                issues.append("Missing ECDSA public key")
            
            if not vault_data.get('vault', {}).get('signers'):
                issues.append("No signers found")
            
            if not vault_data.get('vault', {}).get('key_shares'):
                issues.append("No key shares found")
            
            # Strict validation
            if args.strict:
                vault = vault_data.get('vault', {})
                if vault.get('lib_type') not in ['GG20', 'DKLS']:
                    issues.append("Unknown lib_type")
                
                if len(vault.get('signers', [])) != len(vault.get('key_shares', [])):
                    issues.append("Mismatch between signers and key shares count")
            
            if issues:
                print("❌ Validation failed:")
                for issue in issues:
                    print(f"  - {issue}")
                return 1
            else:
                print("✅ Vault validation passed")
                return 0
                
        except Exception as e:
            print(f"Error validating vault: {e}")
            return 1
    
    @staticmethod
    def export(args):
        """Export vault data to file"""
        try:
            vault_data = VaultCommands._load_vault(args.file)
            if not vault_data:
                return 1
            
            output_path = Path(args.output)
            
            if args.format == 'json':
                with open(output_path, 'w') as f:
                    json.dump(vault_data, f, indent=2)
            elif args.format == 'yaml':
                with open(output_path, 'w') as f:
                    yaml.dump(vault_data, f, default_flow_style=False)
            
            print(f"Exported vault data to {output_path} ({args.format})")
            return 0
            
        except Exception as e:
            print(f"Error exporting vault: {e}")
            return 1
    
    @staticmethod
    def _load_vault(file_path):
        """Load and parse vault file, return structured data"""
        path = Path(file_path)
        
        if not path.exists():
            print(f"Error: File {file_path} does not exist")
            return None
        
        try:
            # Read and decode file
            with open(path, 'r') as f:
                base64_content = f.read().strip()
            
            binary_data = base64.b64decode(base64_content)
            
            # Parse container
            container = VaultContainer()
            container.ParseFromString(binary_data)
            
            result = {
                'file_info': {
                    'path': str(path),
                    'size_chars': len(base64_content),
                    'size_bytes': len(binary_data)
                },
                'container': {
                    'version': container.version,
                    'is_encrypted': container.is_encrypted,
                    'vault_data_length': len(container.vault)
                }
            }
            
            # Parse inner vault if present
            if container.vault:
                vault_binary = base64.b64decode(container.vault)
                vault = Vault()
                vault.ParseFromString(vault_binary)
                
                # Convert lib_type enum to string
                lib_type_name = "UNKNOWN"
                if vault.lib_type == LibType.LIB_TYPE_GG20:
                    lib_type_name = "GG20"
                elif vault.lib_type == LibType.LIB_TYPE_DKLS:
                    lib_type_name = "DKLS"
                
                # Extract key shares
                key_shares = []
                for share in vault.key_shares:
                    share_data = {
                        'public_key': share.public_key,
                        'keyshare_length': len(share.keyshare)
                    }
                    
                    # Try to decode keyshare data
                    if share.keyshare:
                        try:
                            decoded_keyshare = base64.b64decode(share.keyshare)
                            decoded_str = decoded_keyshare.decode('utf-8')
                            keyshare_json = json.loads(decoded_str)
                            share_data['keyshare_data'] = keyshare_json
                        except:
                            share_data['keyshare_data'] = '[binary/encrypted]'
                    
                    key_shares.append(share_data)
                
                result['vault'] = {
                    'name': vault.name,
                    'public_key_ecdsa': vault.public_key_ecdsa,
                    'public_key_eddsa': vault.public_key_eddsa,
                    'local_party_id': vault.local_party_id,
                    'hex_chain_code': vault.hex_chain_code,
                    'reshare_prefix': vault.reshare_prefix,
                    'lib_type': lib_type_name,
                    'signers': list(vault.signers),
                    'key_shares': key_shares
                }
                
                # Add timestamp if present
                if vault.HasField('created_at'):
                    result['vault']['created_at'] = {
                        'seconds': vault.created_at.seconds,
                        'nanos': vault.created_at.nanos,
                        'datetime': datetime.fromtimestamp(vault.created_at.seconds).isoformat()
                    }
            
            return result
            
        except Exception as e:
            print(f"Error loading vault: {e}")
            return None
    
    @staticmethod
    def _print_summary(vault_data):
        """Print brief vault summary"""
        vault = vault_data.get('vault', {})
        print(f"📁 Vault: {vault.get('name', 'Unnamed')}")
        print(f"🔐 Type: {vault.get('lib_type', 'Unknown')}")
        print(f"👥 Signers: {len(vault.get('signers', []))}")
        print(f"🗝️  Shares: {len(vault.get('key_shares', []))}")
        if vault.get('created_at'):
            print(f"📅 Created: {vault['created_at']['datetime']}")
    
    @staticmethod
    def _print_detailed(vault_data, verbose=False):
        """Print detailed vault information"""
        file_info = vault_data.get('file_info', {})
        container = vault_data.get('container', {})
        vault = vault_data.get('vault', {})
        
        print(f"=== Vault Analysis: {file_info.get('path', 'Unknown')} ===")
        print(f"File Size: {file_info.get('size_chars', 0)} chars → {file_info.get('size_bytes', 0)} bytes")
        print(f"Container Version: {container.get('version', 'Unknown')}")
        print(f"Encrypted: {'Yes' if container.get('is_encrypted') else 'No'}")
        
        if vault:
            print(f"\n📁 Vault Name: '{vault.get('name', 'Unnamed')}'")
            print(f"🔐 Crypto Type: {vault.get('lib_type', 'Unknown')}")
            print(f"🔑 ECDSA Public Key: {vault.get('public_key_ecdsa', 'None')}")
            
            if vault.get('public_key_eddsa'):
                print(f"🔑 EdDSA Public Key: {vault.get('public_key_eddsa')}")
            
            print(f"🆔 Local Party ID: {vault.get('local_party_id', 'None')}")
            
            if vault.get('hex_chain_code'):
                print(f"🔗 Chain Code: {vault.get('hex_chain_code')}")
            
            if vault.get('created_at'):
                print(f"📅 Created: {vault['created_at']['datetime']}")
            
            # Signers
            signers = vault.get('signers', [])
            print(f"\n👥 Signers ({len(signers)}):")
            for i, signer in enumerate(signers):
                print(f"  {i+1}. {signer}")
            
            # Key Shares
            shares = vault.get('key_shares', [])
            print(f"\n🗝️  Key Shares ({len(shares)}):")
            for i, share in enumerate(shares):
                print(f"  Share {i+1}:")
                print(f"    Public Key: {share.get('public_key', 'None')}")
                print(f"    Data Length: {share.get('keyshare_length', 0)} chars")
                
                if verbose and 'keyshare_data' in share:
                    data = share['keyshare_data']
                    if isinstance(data, dict):
                        print(f"    Data Keys: {list(data.keys())}")
                    else:
                        print(f"    Data: {data}")
