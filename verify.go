package main

import (
	"fmt"
	"log"

	vault "github.com/vultisig/commondata/go/vultisig/vault/v1"
	keygen "github.com/vultisig/commondata/go/vultisig/keygen/v1"
)

// verifyCommondataAccess verifies we can import official Vultisig protobuf definitions
func verifyCommondataAccess() {
	fmt.Println("✅ Official Vultisig commondata protobuf access verified!")
	
	// Verify we can access the main protobuf types
	var v vault.Vault
	var k keygen.KeygenMessage
	
	fmt.Printf("   - Vault protobuf type: %T\n", v)
	fmt.Printf("   - Keygen protobuf type: %T\n", k)
	
	log.Println("Ready to use official Vultisig data structures")
}
