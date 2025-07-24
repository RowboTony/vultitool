package main

import (
	"fmt"
	"io"
	"os"
	"strings"
)

func getVersion() string {
	file, err := os.Open("VERSION")
	if err != nil {
		return "unknown"
	}
	defer file.Close()
	
	data, err := io.ReadAll(file)
	if err != nil {
		return "unknown"
	}
	
	return strings.TrimSpace(string(data))
}

func main() {
	fmt.Println("vultitool - Vault decryption utility")
	
	if len(os.Args) < 2 {
		printUsage()
		os.Exit(1)
	}
	
	command := os.Args[1]
	
	switch command {
	case "decrypt":
		// TODO: Implement decrypt command
		fmt.Println("Decrypt command not yet implemented")
	case "version", "-v", "--version":
		fmt.Printf("vultitool-go %s\n", getVersion())
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
	fmt.Println("  version    Show version information")
	fmt.Println("  help       Show this help message")
	fmt.Println("")
	fmt.Println("Examples:")
	fmt.Println("  vultitool decrypt vault.json")
	fmt.Println("  vultitool version")
	fmt.Println("  vultitool help")
}
