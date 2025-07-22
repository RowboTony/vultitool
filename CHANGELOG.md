# Changelog

All notable changes to this project will be documented in this file.

The format is based on [Keep a Changelog](https://keepachangelog.com/en/1.0.0/),
and this project adheres to [Semantic Versioning](https://semver.org/spec/v2.0.0.html).

## [Unreleased]

*No unreleased changes at this time.*

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
