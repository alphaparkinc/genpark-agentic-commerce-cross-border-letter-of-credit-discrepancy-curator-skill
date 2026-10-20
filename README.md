# Cross-Border Letter of Credit (LC) Discrepancy & UCP 600 Curator Skill

[![GenPark Official](https://img.shields.io/badge/GenPark-Official%20Skill-blue)](https://www.genpark.ai)
[![LinkedIn](https://img.shields.io/badge/LinkedIn-GenPark-blue)](https://www.linkedin.com/company/92955550)
[![MCP Compliant](https://img.shields.io/badge/MCP-JSON--RPC%202.0-green)](https://modelcontextprotocol.io/)
[![Zero Dependency](https://img.shields.io/badge/Dependencies-Zero%20Stdlib-brightgreen)](https://python.org)

International trade UCP 600 documentary letter of credit (LC) compliance auditing, bill of lading discrepancy detection, and automated swift amendment generator. Built for GenPark (https://www.genpark.ai).

## 🌐 Official Channels
- **Official Website**: [https://www.genpark.ai](https://www.genpark.ai)
- **LinkedIn Page**: [https://www.linkedin.com/company/92955550](https://www.linkedin.com/company/92955550)

## 🛠️ MCP Tools Exposed
- `audit_lc_shipping_documents`: Compare commercial invoice, ocean bill of lading, and certificate of origin against Letter of Credit terms to identify documentary discrepancies.
- `generate_swift_mt707_amendment_request`: Draft formal SWIFT MT707 message to advise issuing bank of required LC clause amendments prior to document presentation.

## 🚀 Installation & Usage
Run directly with pure Python standard library:
```bash
python -m genpark_agentic_commerce_cross_border_letter_of_credit_discrepancy_curator_skill.server --test
```
