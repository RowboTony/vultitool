package main

import (
	"fmt"
	"os"
)

func main() {
	fmt.Println("VultiTool - Vault decryption utility")
	
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}
	
	command := os.Args[1]
	
	switch command {
	case "decrypt":
		// TODO: Implement decrypt command
		fmt.Println("Decrypt command not yet implemented")
	case "help", "-h", "--help":
		printUsage()
	default:
		fmt.Printf("Unknown command: %s\n", command)
		printUsage()
		os.Exit(1)
	}
}

func printUsage() {
	fmt.Println("Usage: vultitool <command> [options]")
	fmt.Println("")
	fmt.Println("Commands:")
	fmt.Println("  decrypt    Decrypt a vault file")
	fmt.Println("  help       Show this help message")
	fmt.Println("")
	fmt.Println("Examples:")
	fmt.Println("  vultitool decrypt vault.json")
	fmt.Println("  vultitool help")
}
