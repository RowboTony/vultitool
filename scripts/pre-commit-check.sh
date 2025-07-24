#!/bin/bash
# Pre-commit validation script for vultitool
# Ensures clean, dependency-consistent state before commits

set -euo pipefail

# Colors for output
RED='\033[31m'
GREEN='\033[32m'
YELLOW='\033[33m'
BLUE='\033[34m'
RESET='\033[0m'

echo -e "${BLUE}🔍 vultitool Pre-Commit Validation${RESET}"
echo -e "${BLUE}===================================${RESET}"
echo ""

# Function to check if we're in git repo
check_git_repo() {
    if ! git rev-parse --git-dir > /dev/null 2>&1; then
        echo -e "${RED}❌ Not in a git repository${RESET}"
        exit 1
    fi
}

# Function to check for uncommitted changes
check_uncommitted_changes() {
    if git diff --cached --quiet; then
        echo -e "${YELLOW}⚠️  No staged changes found. Run 'git add .' first if you want to commit changes.${RESET}"
    else
        echo -e "${GREEN}✅ Staged changes detected${RESET}"
    fi
}

# Function to run clean slate test
run_clean_test() {
    echo -e "${BLUE}🧹 Running clean slate validation...${RESET}"
    echo -e "${YELLOW}This will rebuild everything from scratch${RESET}"
    
    if ! make test-clean; then
        echo -e "${RED}❌ Clean slate validation FAILED${RESET}"
        echo -e "${RED}This indicates dependency issues or environment problems${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Clean slate validation PASSED${RESET}"
}

# Function to check version consistency
check_version_consistency() {
    echo -e "${BLUE}🏷️  Checking version consistency...${RESET}"
    
    # Get version from VERSION file
    if [ ! -f "VERSION" ]; then
        echo -e "${RED}❌ VERSION file not found${RESET}"
        exit 1
    fi
    
    version=$(cat VERSION)
    echo -e "   Version file: ${version}"
    
    # Check CHANGELOG
    if ! grep -q "^## \[${version}\]" CHANGELOG.md; then
        echo -e "${RED}❌ Version ${version} not found in CHANGELOG.md${RESET}"
        exit 1
    fi
    
    # Check CLI version output
    cli_version=$(./vultitool --version 2>/dev/null || echo "FAILED")
    if [[ "$cli_version" != "vultitool ${version}" ]]; then
        echo -e "${RED}❌ CLI version mismatch: expected 'vultitool ${version}', got '${cli_version}'${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Version consistency verified${RESET}"
}

# Function to check naming conventions
check_naming_conventions() {
    echo -e "${BLUE}📝 Checking naming conventions...${RESET}"
    
    # Check for incorrect naming (excluding documentation and this script)
    # Use direct pattern to avoid variable name false positives
    if grep -r "VultiTool\|VultItool" --include="*.py" --include="*.go" . --exclude-dir=.git --exclude="CHANGELOG.md" --exclude="*/pre-commit-check.sh" > /dev/null 2>&1; then
        echo -e "${RED}❌ Incorrect naming conventions found:${RESET}"
        grep -r "VultiTool\|VultItool" --include="*.py" --include="*.go" . --exclude-dir=.git --exclude="CHANGELOG.md" --exclude="*/pre-commit-check.sh"
        echo -e "${RED}Use 'vultitool' (lowercase) for the tool name${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Naming conventions correct${RESET}"
}

# Function to check for protobuf warnings
check_protobuf_warnings() {
    echo -e "${BLUE}🔧 Checking for protobuf warnings...${RESET}"
    
    # Test a simple operation and capture stderr
    if ./vultitool vault parse tests/fixtures/testGG20-part1of2.vult --json >/dev/null 2>warnings.tmp; then
        if [ -s warnings.tmp ]; then
            echo -e "${RED}❌ Protobuf warnings detected:${RESET}"
            cat warnings.tmp
            rm -f warnings.tmp
            echo -e "${RED}Run 'make setup-protobuf' to fix version mismatches${RESET}"
            exit 1
        else
            echo -e "${GREEN}✅ No protobuf warnings${RESET}"
            rm -f warnings.tmp
        fi
    else
        echo -e "${RED}❌ Basic vault parsing failed${RESET}"
        rm -f warnings.tmp
        exit 1
    fi
}

# Function to verify self-tests pass
verify_self_tests() {
    echo -e "${BLUE}🧪 Verifying self-tests...${RESET}"
    
    if ! ./vultitool doctor selftest >/dev/null 2>&1; then
        echo -e "${RED}❌ Self-tests failed${RESET}"
        echo -e "${RED}Run './vultitool doctor selftest' to see details${RESET}"
        exit 1
    fi
    
    echo -e "${GREEN}✅ Self-tests pass${RESET}"
}

# Main execution
main() {
    check_git_repo
    check_uncommitted_changes
    
    echo ""
    echo -e "${BLUE}Starting validation checks...${RESET}"
    echo ""
    
    # Quick checks first (fast failures)
    check_version_consistency
    check_naming_conventions
    
    # Build and environment checks (slower)
    run_clean_test
    check_protobuf_warnings
    verify_self_tests
    
    echo ""
    echo -e "${GREEN}🎉 All pre-commit checks PASSED!${RESET}"
    echo ""
    echo -e "${YELLOW}💡 Ready to commit:${RESET}"
    echo -e "   git commit -m \"Your commit message\""
    echo ""
}

# Handle script arguments
case "${1:-check}" in
    "check")
        main
        ;;
    "quick")
        echo -e "${BLUE}🔍 Quick Pre-Commit Validation${RESET}"
        echo -e "${BLUE}===============================${RESET}"
        check_git_repo
        check_uncommitted_changes
        echo ""
        check_version_consistency
        check_naming_conventions
        check_protobuf_warnings
        verify_self_tests
        echo -e "${GREEN}🎉 Quick validation PASSED!${RESET}"
        echo -e "${YELLOW}💡 Run './scripts/pre-commit-check.sh' for full clean-slate validation${RESET}"
        ;;
    "setup")
        echo -e "${BLUE}Setting up pre-commit hook...${RESET}"
        if [ -d ".git/hooks" ]; then
            cp "$0" .git/hooks/pre-commit
            chmod +x .git/hooks/pre-commit
            echo -e "${GREEN}✅ Pre-commit hook installed${RESET}"
            echo -e "${YELLOW}Now 'git commit' will automatically run validation${RESET}"
        else
            echo -e "${RED}❌ Not in a git repository${RESET}"
            exit 1
        fi
        ;;
    "help")
        echo "vultitool Pre-Commit Validation Script"
        echo ""
        echo "Usage:"
        echo "  $0 [check|quick|setup|help]"
        echo ""
        echo "Commands:"
        echo "  check   Run full validation with clean slate rebuild (default)"
        echo "  quick   Run fast validation checks only (no rebuild)"
        echo "  setup   Install as git pre-commit hook"
        echo "  help    Show this help message"
        ;;
    *)
        echo "Unknown command: $1"
        echo "Run '$0 help' for usage information"
        exit 1
        ;;
esac
