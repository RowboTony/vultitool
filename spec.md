# spec.md — Vultisig CLI & Ecosystem Analysis Project (Codename: vultitool)

---

## Project Title

**Vultisig CLI & Ecosystem Test Suite (Codename: vultitool)**

---

## Project Vision & Purpose

> *Become the definitive source of technical truth for Vultisig—starting with a foundational CLI tool and comprehensive ecosystem analysis. Enable better documentation, developer onboarding, and automated testing for the next phase of Vultisig’s growth.*

- **Primary goal:**  
  Understand Vultisig at the deepest level (“O’Reilly book” depth) to enable better contribution, documentation, and tooling.
- **Secondary goal:**  
  Build a cross-platform CLI (“vultitool”) as the reference implementation for Vultisig vault, transaction, and swap functions.
- **Long-term:**  
  Establish a knowledge base for both humans and AI, and lay the foundation for an automated, test-driven Vultisig ecosystem.

---

## Background

- Vultisig is a novel, seedless crypto wallet leveraging MPC TSS (GG20/DKLS, ECDSA/EdDSA) for transaction signing.  
- Core innovation: No seed phrases—vault “parts” (`.vult` files) instead.
- Supports hot (2-of-2) and secure (2-of-3) vaults.
- Primary codebase split: iOS, Windows, Android, Web (browser extension).
- Swapping powered by ThorChain and LiFi.

---

## Project Goals & Deliverables

1. **Authoritative Understanding**
   - Write the “definitive technical book” on Vultisig’s architecture, protocols, and usage.
   - Gather and synthesize all public Vultisig information (docs, code, Discord, blogs).

2. **Ecosystem Reverse Engineering**
   - Analyze Vultisig’s main repositories, with special focus on [commondata](https://github.com/vultisig/commondata).
   - Document protocols, file formats (`.vult`), flows, and infrastructure (esp. Vultiserver).

3. **CLI Reference Implementation ("vultitool")**
   - **Hybrid Architecture**: Python CLI for tooling/analysis, Go backend for cryptographic operations
   - **Python Components**:
     - Primary CLI interface and user experience
     - Vault parsing, inspection, validation, and export
     - Test automation and diagnostics ("doctor" commands)
     - Human-readable output and reporting
   - **Go Components**:
     - Cryptographic operations (encryption/decryption, key derivation)
     - TSS library integration (using official mobile-tss-lib)
     - Transaction building and signing
     - Performance-critical operations
   - **Interoperability**:
     - Go library bindings accessible from Python
     - Cross-validation between implementations
     - Shared test fixtures and protocol buffers
   - Support at minimum:  
     - Vault creation/import/export (Python + Go)
     - .vult parsing and inspection (Python)
     - Password-protected vault decryption (Go crypto, Python interface)
     - Transaction signing simulation (Go)
     - Multi-signature vault coordination (Go)
     - Basic swap (simulated, then real if possible)  
   - Output: Production-ready CLI with secure crypto backend

4. **Test & Audit Suite**
   - Use the CLI as a baseline for test automation (unit/integration/CI).
   - Compare against UI/UX flows for parity and bug reproduction.

5. **Vultiserver Deep Dive**
   - Understand Vultiserver’s signing, backup, and key management.
   - Document or run a local Vultiserver if feasible.
   - Security audit for potential vulnerabilities.

6. **Documentation Overhaul**
   - Refactor or create Vultisig developer docs with clarity, accuracy, and “teachability” in mind.
   - Document both high-level concepts and low-level interfaces.

7. **Future: vultitool Dashboard**
   - Prototype a dashboard for Vultisig/Vultiserver system status (like ThorChain).
   - Potential: exploit/vulnerability scanner, SDK reference, and live test matrix.

---

## Constraints & Philosophy

- **Step-by-step:** Start simple (parse `.vult` → sign → swap), add features iteratively.
- **Transparency:** All findings, docs, and code to be public and open-source.
- **Teaching-first:** All tools, tests, and docs should be approachable for non-experts.
- **Cross-platform ideal:** Prioritize Unix/mac/WSL shell for MVP, but design with portability in mind.
- **Not a language expert:** Assume you (the project owner) are tech-proficient but need clear code explanations, language recommendations, and best-practice guidance.

---

## Key Open Questions & Research Tasks

1. **.vult File Spec:**
   - What is the minimum viable parser for both GG20 and DKLS formats?
   - Are there existing libraries or tools (see: mobile-tss-lib, SxMShaDoW’s decoder) that can be leveraged for this?

2. **Vault Creation & Signing Flow:**
   - Document (in code and words) the step-by-step keygen, vault join, and signing ceremony for both Fast and Secure Vaults.

3. **Swap Infrastructure:**
   - Which SDKs power swaps? (ThorChain, LiFi, others?)
   - Is there a common abstraction/interface across all app platforms?

4. **Vultiserver Details:**
   - What APIs, protocols, and key management approaches does it use?
   - Can it be run locally? Is it open source?

5. **Testing State:**
   - Are there *any* existing test suites or CI pipelines for Vultisig?  
   - If not, what’s the minimal set to bootstrap (using the new CLI as foundation)?

6. **Developer Experience:**
   - Is there a more unified way (Rust, Go, Node, Electron, Python) to build across iOS, Windows, Android, Web?
   - What are the tradeoffs for re-architecting Vultisig for better cross-platform parity?

7. **Emergency Recovery:**
   - What are the current best tools for reconstructing keys from `.vult` files for both GG20 and DKLS?
   - Can this process be reliably automated/tested via CLI?

---

## Implementation Roadmap

### Repository Structure
```
vultitool/
├── python/          # Current Python CLI and tooling
│   ├── vultitool/
│   ├── tests/
│   └── requirements.txt
├── go/              # New Go module for crypto operations
│   ├── go.mod
│   ├── go.sum
│   ├── cmd/         # Go CLI binaries
│   ├── pkg/         # Go packages
│   └── internal/    # Internal Go code
├── shared/          # Shared resources
│   ├── protos/      # Protocol buffer definitions
│   └── fixtures/    # Test files used by both
└── scripts/         # Build and integration scripts
```

### Phase 1: Go Foundation
- [x] **Python MVP Complete**: Full `.vult` parsing, validation, export, password support
- [ ] **Initialize Go module** in `go/` directory
- [ ] **Port crypto operations** from Python to Go (using official mobile-tss-lib patterns)
- [ ] **Create Go CLI proof-of-concept** for vault decryption
- [ ] **Add integration tests** verifying Python and Go produce identical results
- [ ] **Cross-validation suite** to ensure both implementations agree

### Phase 2: Interoperability
- [ ] **Go library bindings** for Python (via subprocess or shared library)
- [ ] **Update Python CLI** to optionally use Go crypto backend
- [ ] **Maintain backward compatibility** with pure Python fallback
- [ ] **Performance benchmarking** between Python and Go crypto
- [ ] **Security audit** of interop layer

### Phase 3: Advanced TSS Features
- [ ] **TSS operations** in Go using official libraries
- [ ] **Multi-signature vault reconstruction** from 2-of-3 key shares
- [ ] **Transaction building** and signing simulation
- [ ] **Swap transaction construction** with ThorChain/LiFi integration
- [ ] **End-to-end workflow validation**

## First Steps / Milestones

1. **Set up local dev environment and clone the main Vultisig repos:**
    - [commondata](https://github.com/vultisig/commondata)
    - [mobile-tss-lib](https://github.com/vultisig/mobile-tss-lib)
    - [vultisig-ios](https://github.com/vultisig/vultisig-ios)
    - [vultisig-windows](https://github.com/vultisig/vultisig-windows)
    - [vultisig-android](https://github.com/vultisig/vultisig-android)
    - [vultisig-web](https://github.com/vultisig/vultisig-web)
    - [vultiserver](https://github.com/vultisig/vultiserver)
    - [vultisig-go](https://github.com/vultisig/vultisig-go)
2. **Write "hello world" CLI to parse and print `.vult` file data.**
3. **Document findings in both `spec.md` and project documentation.**
4. **Incrementally build and test further CLI capabilities, updating documentation as you learn.**

---

## Out-of-Scope

- Vultisig Airdrop evaluation (airdrop.vultisig.com) is *not* included.
- Social/community aspects unless critical to core dev workflows.

---

## Collaboration & Communication

- All project state and docs will live in the repo for easy sharing and collaboration.
- Regular check-ins with Vultisig team as needed (preferably async).
- Questions and ambiguities should always be logged for resolution.

---

