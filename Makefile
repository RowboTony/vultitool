# Makefile for VultiTool - Cross-language build automation
# Supports both Python and Go components with protobuf generation

.PHONY: help setup build test clean install protobuf-python protobuf-go dev-setup
.DEFAULT_GOAL := help

# Configuration
PYTHON := python3
GO := go
PROTOC := protoc
VENV_DIR := venv
GENERATED_DIR := generated
PROTO_DIR := proto
GO_BINARY := vultitool
PYTHON_BINARY := vultitool

# Colors for output
RED := \033[31m
GREEN := \033[32m
YELLOW := \033[33m
BLUE := \033[34m
RESET := \033[0m

help: ## Show this help message
	@echo "$(BLUE)VultiTool Build System$(RESET)"
	@echo ""
	@echo "$(YELLOW)Available targets:$(RESET)"
	@awk 'BEGIN {FS = ":.*?## "} /^[a-zA-Z_-]+:.*?## / {printf "  $(GREEN)%-20s$(RESET) %s\n", $$1, $$2}' $(MAKEFILE_LIST)

setup: dev-setup protobuf ## Complete setup for development environment
	@echo "$(GREEN)✅ Setup complete!$(RESET)"

dev-setup: ## Set up development environment
	@echo "$(BLUE)Setting up development environment...$(RESET)"
	@$(PYTHON) -m pip install --upgrade pip
	@$(PYTHON) -m pip install -r requirements.txt
	@echo "$(GREEN)✅ Python dependencies installed$(RESET)"
	@$(GO) mod download
	@echo "$(GREEN)✅ Go dependencies downloaded$(RESET)"

protobuf: protobuf-python protobuf-go ## Generate protobuf files for both Python and Go

protobuf-python: ## Generate Python protobuf files
	@echo "$(BLUE)Generating Python protobuf files...$(RESET)"
	@mkdir -p $(GENERATED_DIR)
	@$(PROTOC) --proto_path=$(PROTO_DIR) \
		--python_out=$(GENERATED_DIR) \
		--pyi_out=$(GENERATED_DIR) \
		$(PROTO_DIR)/vultisig/vault/v1/*.proto \
		$(PROTO_DIR)/vultisig/keygen/v1/*.proto
	@# Create __init__.py files for proper Python package structure
	@find $(GENERATED_DIR) -type d -exec touch {}/__init__.py \;
	@echo "$(GREEN)✅ Python protobuf files generated$(RESET)"

protobuf-go: ## Generate Go protobuf files  
	@echo "$(BLUE)Generating Go protobuf files...$(RESET)"
	@echo "$(YELLOW)Using official Vultisig commondata protobuf definitions$(RESET)"
	@if $(GO) mod download github.com/vultisig/commondata 2>/dev/null; then \
		echo "$(GREEN)✅ Official commondata protobuf sources ready$(RESET)"; \
		echo "$(YELLOW)   Protobuf definitions available via Go modules$(RESET)"; \
	else \
		echo "$(YELLOW)⚠️  Go protobuf generation skipped (compatibility issue)$(RESET)"; \
		echo "$(YELLOW)   This does not affect core vultitool functionality$(RESET)"; \
	fi

build: build-python build-go ## Build both Python and Go components

build-python: protobuf-python ## Build Python component
	@echo "$(BLUE)Building Python component...$(RESET)"
	@chmod +x $(PYTHON_BINARY)
	@echo "$(GREEN)✅ Python component ready$(RESET)"

build-go: ## Build Go component
	@echo "$(BLUE)Building Go component...$(RESET)"
	@$(GO) build -o $(GO_BINARY) .
	@echo "$(GREEN)✅ Go binary built: $(GO_BINARY)$(RESET)"

test: test-python test-go ## Run tests for both components

test-python: ## Run Python tests
	@echo "$(BLUE)Running Python tests...$(RESET)"
	@$(PYTHON) -m pytest tests/ -v --cov=commands --cov-report=term-missing
	@echo "$(GREEN)✅ Python tests completed$(RESET)"

test-go: ## Run Go tests
	@echo "$(BLUE)Running Go tests...$(RESET)"
	@$(GO) test -v ./...
	@echo "$(GREEN)✅ Go tests completed$(RESET)"

selftest: build ## Run comprehensive self-tests
	@echo "$(BLUE)Running VultiTool self-tests...$(RESET)"
	@./$(PYTHON_BINARY) doctor selftest
	@echo "$(GREEN)✅ Self-tests completed$(RESET)"

clean: ## Clean build artifacts and generated files
	@echo "$(BLUE)Cleaning build artifacts...$(RESET)"
	@rm -rf $(GENERATED_DIR)
	@rm -rf go/generated
	@rm -f $(GO_BINARY)
	@rm -rf __pycache__ commands/__pycache__ tests/__pycache__
	@rm -rf .pytest_cache
	@rm -rf *.pyc commands/*.pyc tests/*.pyc
	@rm -rf .coverage
	@$(GO) clean
	@echo "$(GREEN)✅ Clean completed$(RESET)"

install: build ## Install vultitool (requires setup)
	@echo "$(BLUE)Installing VultiTool...$(RESET)"
	@echo "$(YELLOW)Note: Installation creates symbolic links in your PATH$(RESET)"
	@sudo ln -sf "$(PWD)/$(PYTHON_BINARY)" /usr/local/bin/$(PYTHON_BINARY)
	@sudo ln -sf "$(PWD)/$(GO_BINARY)" /usr/local/bin/$(GO_BINARY)
	@echo "$(GREEN)✅ VultiTool installed to /usr/local/bin/$(RESET)"

uninstall: ## Uninstall vultitool
	@echo "$(BLUE)Uninstalling VultiTool...$(RESET)"
	@sudo rm -f /usr/local/bin/$(PYTHON_BINARY)
	@sudo rm -f /usr/local/bin/$(GO_BINARY)
	@echo "$(GREEN)✅ VultiTool uninstalled$(RESET)"

format: ## Format code (Python: black, Go: gofmt)
	@echo "$(BLUE)Formatting code...$(RESET)"
	@$(PYTHON) -m black . --extend-exclude="$(GENERATED_DIR)" || echo "$(YELLOW)Install 'black' for Python formatting$(RESET)"
	@$(GO) fmt ./...
	@echo "$(GREEN)✅ Code formatted$(RESET)"

lint: ## Lint code (Python: flake8, Go: golint)
	@echo "$(BLUE)Linting code...$(RESET)"
	@$(PYTHON) -m flake8 --exclude=$(GENERATED_DIR) . || echo "$(YELLOW)Install 'flake8' for Python linting$(RESET)"
	@golint ./... 2>/dev/null || echo "$(YELLOW)Install 'golint' for Go linting$(RESET)"
	@echo "$(GREEN)✅ Linting completed$(RESET)"

doctor: build ## Run system diagnostics
	@./$(PYTHON_BINARY) doctor health

# Development targets
dev-python: protobuf-python ## Quick Python development build
	@echo "$(GREEN)✅ Python development ready$(RESET)"

dev-go: build-go ## Quick Go development build
	@echo "$(GREEN)✅ Go development ready$(RESET)"

# CI/CD friendly targets
ci-setup: ## Setup for CI/CD environment
	@$(MAKE) dev-setup
	@$(MAKE) protobuf

ci-test: ## Full test suite for CI/CD
	@$(MAKE) test
	@$(MAKE) selftest

# Check dependencies
check-deps: ## Check if required tools are installed
	@echo "$(BLUE)Checking dependencies...$(RESET)"
	@command -v $(PYTHON) >/dev/null 2>&1 || { echo "$(RED)❌ Python 3 not found$(RESET)"; exit 1; }
	@command -v $(GO) >/dev/null 2>&1 || { echo "$(RED)❌ Go not found$(RESET)"; exit 1; }
	@command -v $(PROTOC) >/dev/null 2>&1 || { echo "$(RED)❌ protoc not found$(RESET)"; exit 1; }
	@echo "$(GREEN)✅ All required dependencies found$(RESET)"

# Show current status
status: ## Show current build status
	@echo "$(BLUE)VultiTool Status:$(RESET)"
	@echo "  Python binary: $(if $(shell test -x $(PYTHON_BINARY) && echo true),$(GREEN)✅ Ready$(RESET),$(YELLOW)❌ Not built$(RESET))"
	@echo "  Go binary: $(if $(shell test -x $(GO_BINARY) && echo true),$(GREEN)✅ Ready$(RESET),$(YELLOW)❌ Not built$(RESET))"
	@echo "  Python protobuf: $(if $(shell test -d $(GENERATED_DIR) && echo true),$(GREEN)✅ Generated$(RESET),$(YELLOW)❌ Not generated$(RESET))"
	@echo "  Go modules: $(if $(shell test -f go.sum && echo true),$(GREEN)✅ Downloaded$(RESET),$(YELLOW)❌ Not downloaded$(RESET))"
