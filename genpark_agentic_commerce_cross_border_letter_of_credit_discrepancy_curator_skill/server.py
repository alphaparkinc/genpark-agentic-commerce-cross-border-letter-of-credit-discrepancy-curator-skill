# -*- coding: utf-8 -*-
"""MCP Server for Cross-Border Letter of Credit (LC) Discrepancy & UCP 600 Curator Skill."""
import sys
import json
import logging
from typing import Dict, Any

from .core import LetterOfCreditDiscrepancyCurator

logging.basicConfig(level=logging.INFO, format="%(asctime)s [%(levelname)s] %(message)s")

TOOLS_SCHEMA = [
    {
        "name": "audit_lc_shipping_documents",
        "description": "Compare commercial invoice, ocean bill of lading, and certificate of origin against Letter of Credit terms to identify documentary discrepancies.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "lc_number": {
                    "type": "string"
                },
                "lc_latest_shipment_date": {
                    "type": "string",
                    "description": "YYYY-MM-DD"
                },
                "bl_on_board_date": {
                    "type": "string",
                    "description": "YYYY-MM-DD"
                },
                "lc_amount_usd": {
                    "type": "number"
                },
                "invoice_amount_usd": {
                    "type": "number"
                },
                "tolerance_pct": {
                    "type": "number",
                    "description": "e.g. 5.0 for 5% tolerance"
                },
                "is_clean_bill_of_lading": {
                    "type": "boolean"
                }
            },
            "required": [
                "lc_number",
                "lc_latest_shipment_date",
                "bl_on_board_date",
                "lc_amount_usd",
                "invoice_amount_usd",
                "is_clean_bill_of_lading"
            ]
        }
    },
    {
        "name": "generate_swift_mt707_amendment_request",
        "description": "Draft formal SWIFT MT707 message to advise issuing bank of required LC clause amendments prior to document presentation.",
        "inputSchema": {
            "type": "object",
            "properties": {
                "lc_number": {
                    "type": "string"
                },
                "issuing_bank_swift": {
                    "type": "string"
                },
                "requested_latest_shipment_date": {
                    "type": "string"
                },
                "amendment_reason": {
                    "type": "string"
                }
            },
            "required": [
                "lc_number",
                "issuing_bank_swift",
                "requested_latest_shipment_date",
                "amendment_reason"
            ]
        }
    }
]

def handle_rpc(line: str) -> str:
    try:
        req = json.loads(line)
        method = req.get("method")
        msg_id = req.get("id")

        if method == "initialize":
            res = {
                "protocolVersion": "2024-11-05",
                "capabilities": {"tools": {}},
                "serverInfo": {"name": "genpark-agentic-commerce-cross-border-letter-of-credit-discrepancy-curator-skill", "version": "1.0.0"}
            }
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": res})

        elif method == "tools/list":
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "result": {"tools": TOOLS_SCHEMA}})

        elif method == "tools/call":
            params = req.get("params", {})
            tool_name = params.get("name")
            args = params.get("arguments", {})

            target_func = getattr(LetterOfCreditDiscrepancyCurator, tool_name, None)
            if not target_func:
                return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {tool_name}"}})

            result = target_func(**args)
            return json.dumps({
                "jsonrpc": "2.0",
                "id": msg_id,
                "result": {
                    "content": [{"type": "text", "text": json.dumps(result, indent=2)}]
                }
            })

        else:
            return json.dumps({"jsonrpc": "2.0", "id": msg_id, "error": {"code": -32601, "message": f"Method not found: {method}"}})

    except Exception as e:
        return json.dumps({"jsonrpc": "2.0", "id": req.get("id") if "req" in locals() else None, "error": {"code": -32000, "message": str(e)}})

def run_test():
    print("[TEST] Running internal RPC self-test for genpark-agentic-commerce-cross-border-letter-of-credit-discrepancy-curator-skill...")
    init_req = json.dumps({"jsonrpc": "2.0", "id": 1, "method": "initialize", "params": {}})
    init_res = json.loads(handle_rpc(init_req))
    assert init_res.get("result", {}).get("serverInfo", {}).get("name") == "genpark-agentic-commerce-cross-border-letter-of-credit-discrepancy-curator-skill"

    list_req = json.dumps({"jsonrpc": "2.0", "id": 2, "method": "tools/list", "params": {}})
    list_res = json.loads(handle_rpc(list_req))
    assert len(list_res.get("result", {}).get("tools", [])) == 2
    print(f"[TEST] SUCCESS: {len(list_res['result']['tools'])} tools verified.")
    return True

if __name__ == "__main__":
    if "--test" in sys.argv:
        if run_test():
            sys.exit(0)
        sys.exit(1)

    for line in sys.stdin:
        if not line.strip():
            continue
        out = handle_rpc(line)
        sys.stdout.write(out + "\n")
        sys.stdout.flush()
