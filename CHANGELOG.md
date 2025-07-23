# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

*No unreleased changes at this time.*

## [v0.3.6] - 2025-07-23 🍎 macOS Developer Experience Enhancement

### Changed
- **Improved macOS installation UX**: Updated README to promote automated bootstrap script (`./bootstrap-macos.sh`) as "Quick Start" option, with manual installation as alternative
- **Enhanced developer onboarding**: macOS users can now get started with just 3 commands instead of navigating through detailed setup documentation

## [v0.3.5] - 2025-07-23 🔧 Developer Experience & Testing Improvements

### Added
- **Version information in doctor health**: `doctor health` command now displays version number for better diagnostics
- **Improved make test**: `make test` now uses the reliable `doctor selftest` system (48/48 tests passing)
- **Professional onboarding workflow**: New contributors can now `make setup && make test` immediately after cloning

### Changed
- **Enhanced doctor health output**: Now shows `Version: vultitool 0.3.5` alongside timestamp and health checks
- **Fixed make test reliability**: Replaced broken pytest integration with working selftest system
- **Improved Makefile test target**: `make test` now auto-builds and runs comprehensive tests

### Fixed
- **Test system reliability**: Resolved pytest discovery issues by leveraging existing selftest infrastructure
- **Developer onboarding**: Fixed `make test` to work immediately after fresh clone and setup

### Documentation
- **Added proper attribution**: README now credits `testGG20` and `testDKLS` files from [SxMShaDoW/Vultisig-Share-Decoder](https://github.com/SxMShaDoW/Vultisig-Share-Decoder)
- **Enhanced professional standards**: Improved project setup documentation and workflows

### Technical
- **Build system improvements**: `make test` now has proper dependency resolution (depends on `build`)
- **Quality assurance**: Full clean-build-test cycle now works reliably from fresh environment
- **Version consistency**: All version displays now pull from single VERSION file source

## [v0.3.4] - 2025-07-22 🏛️ Canonical Vultisig Integration

### Added
- **Official Vultisig protobuf integration**: Now uses `github.com/vultisig/commondata` directly via Go modules
- **Version alignment**: Matches exact dependency versions from `vultisig-go` for maximum compatibility
- **Canonical source guarantee**: All protobuf definitions sourced from official Vultisig repositories (no local copies)
- **Go module integration**: Added proper Go workspace with official Vultisig dependencies

### Changed  
- **Eliminated local protobuf files**: Replaced with direct imports from `github.com/vultisig/commondata`
- **Updated go.mod**: Now includes official Vultisig commondata and protobuf dependencies
- **Enhanced Makefile**: Improved protobuf generation with official source validation
- **Updated documentation**: README now emphasizes canonical source integration and compatibility

### Technical
- **Dependencies aligned**:
  - `github.com/vultisig/commondata v0.0.0-20250710214228-61d9ed8f7778` (official protobuf schemas)
  - `google.golang.org/protobuf v1.34.2` (compatible with commondata)
  - `go 1.24` (matching vultisig-go requirements)
- **Build reliability**: Go binary builds successfully with official protobuf access
- **Unified architecture**: Single `vultitool` binary (removed obsolete `vultitool-go`)

### Documentation
- **README enhanced**: Added "Official Vultisig Integration" section highlighting canonical sources
- **Technical accuracy**: All documentation now reflects official integration approach
- **Developer confidence**: Clear guarantee of 100% compatibility with official Vultisig applications

## [v0.3.2] - 2025-07-22

### Fixed
- Go module version format compatibility (changed from '1.23.2' to '1.24')
- Build system alignment with vultisig-go project dependencies
- Added Go toolchain specification for proper version handling
- Excluded compiled binaries from git tracking (added 'vultitool' to .gitignore)
- Resolved protobuf generation errors and module parsing issues

### Changed
- Successfully established clean build environment with working CLI interface
- Improved build system reliability and cross-platform compatibility

## [v0.3.0] - 2025-07-22 🎉 First Public Release

### Added
- Comprehensive build system with `Makefile` automation
- One-command setup process (`make setup && make build`)
- Go compatibility layer scaffolding for future multi-language support
- Go module integration for future cryptographic operations
- Enhanced Go module dependency management
- Integration with official [Vultisig mobile-tss-lib](https://github.com/vultisig/mobile-tss-lib/)
- Expanded test coverage to 48 comprehensive tests
- 3-part Secure Vault test files for thorough validation
- Improved `.gitignore` for Go and Python artifacts
- Enhanced `README` with improved developer experience
- Detailed setup instructions with system prerequisites
- Build system documentation and quick reference
- Manual setup options for advanced users
- Python `requirements.txt` for dependency management
- Protobuf generation automation from official [Vultisig `commondata` sources](https://github.com/vultisig/commondata)
- Cross-platform compatibility improvements

### Changed
- Aligned decryption implementation with official Vultisig mobile-tss-lib (AES-GCM/SHA256)
- Renamed test vault files for better clarity:
  - GG20 files: `testGG20-part1of2.vult`, `testGG20-part2of2.vult`
  - DKLS files: `testDKLS-1of2.vult`, `testDKLS-2of2.vult`
  - QA files: `qa-fast-share1of2.vult`, `qa-fast-share2of2.vult`
  - `testGG20` and `testDKLS` files sourced from [SxMShaDoW
Vultisig-Share-Decoder](https://github.com/SxMShaDoW/Vultisig-Share-Decoder/)
- Simplified fixtures `README` table by removing redundant columns
- Restructured `README.md` for better user flow (installation → usage → advanced topics)
- Fixed Unicode encoding issues in documentation
- Improved command formatting and examples throughout documentation
- Added `commit.md` to `.gitignore` for cleaner repository

### Security
- Enhanced password validation testing in self-test suite

### Documentation
- Added Go compatibility layer section to `spec.md`
- Enhanced vault testing documentation

## [v0.2.4] - 2025-07-21

### Added
- Comprehensive password validation in self-test suite
- Automatic handling of encrypted vault testing
- Enhanced test output showing 100% pass rate capability

### Fixed
- Password decryption reliability improvements
- Test suite robustness for edge cases

### Documentation
- Updated `README` with `--password` usage examples
- Enhanced help output documentation

## [v0.2.3] - 2025-07-21

### Added
- Password decryption support for encrypted `.vult` files
- `--password` command-line option for secure vault access
- Comprehensive password handling in CLI interface

### Security
- Implemented secure password input handling
- Added encryption/decryption validation

## [v0.2.2] - 2025-07-21

### Added
- Comprehensive self-test system (`vultitool doctor`)
- Robust test fixtures for automated validation
- Self-diagnostic capabilities for installation verification
- Test coverage for multiple vault types (GG20, DKLS)

### Enhanced
- Doctor commands for system health checks
- Automated testing infrastructure

## [v0.2.1] - 2025-07-21

### Documentation
- Clarified differences between `parse` and `inspect` commands in `README`
- Improved command usage examples
- Enhanced CLI help documentation

### Fixed
- Command interface consistency improvements

## [v0.2.0] - 2025-07-21

### Added
- Professional CLI tool with comprehensive documentation
- Enhanced vault parser using proper Vultisig protobuf schema definitions
- Structured command-line interface with subcommands
- JSON and summary output formats
- Vault validation functionality
- Export capabilities for vault metadata

### Changed
- Complete CLI architecture overhaul from basic parser
- Implemented proper protobuf integration
- Professional command structure and help system

### Removed
- Legacy `parse_vult_enhanced.py` (consolidated into main parser)

## [v0.1.0] - 2025-07-21

### Added
- Initial Vultisig `.vult` file parser (MVP)
- Basic protobuf-based vault file interpretation
- Test files for GG20 and DKLS vault formats
- Initial analysis summary and documentation
- Living specification document (`spec.md`)
- Basic vault file structure understanding

### Documentation
- Project foundation and goals
- Initial reverse engineering findings
- Basic usage instructions

---

## Release Notes

### Version Naming Convention
- Major (x.0.0): Breaking changes, major architecture shifts
- Minor (0.x.0): New features, enhanced functionality
- Patch (0.0.x): Bug fixes, documentation improvements, minor enhancements

### Supported Platforms
- Linux (Ubuntu 22.04+, tested on WSL2)
- macOS (with Homebrew dependencies)
- Windows (via WSL2 or native with proper tooling)

### Dependencies
- Python 3.8+
- Go 1.19+ (for future features)
- Protocol Buffers Compiler (protoc)
- Git, rsync, and standard build tools

### Contributing
See [README.md](README.md) for setup instructions and [spec.md](spec.md) for technical details.

For questions or contributions, please refer to the project documentation or open an issue.
