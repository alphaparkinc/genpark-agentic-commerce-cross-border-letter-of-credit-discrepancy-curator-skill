# -*- coding: utf-8 -*-
"""Cross-Border Letter of Credit (LC) Discrepancy & UCP 600 Curator for GenPark Agentic Commerce."""
import json
from typing import Dict, Any, List

class LetterOfCreditDiscrepancyCurator:
    """ICC UCP 600 documentary credit compliance and bill of lading audit engine."""

    @staticmethod
    def audit_lc_shipping_documents(lc_number: str, lc_latest_shipment_date: str, bl_on_board_date: str, lc_amount_usd: float, invoice_amount_usd: float, is_clean_bill_of_lading: bool, tolerance_pct: float = 5.0) -> Dict[str, Any]:
        """Audit shipping documents for critical bank refusal discrepancies under UCP 600."""
        discrepancies = []
        
        # 1. Late shipment check
        if bl_on_board_date > lc_latest_shipment_date:
            discrepancies.append(f"LATE_SHIPMENT: Bill of Lading onboard date {bl_on_board_date} exceeds latest shipment date {lc_latest_shipment_date} (UCP 600 Art 14).")

        # 2. Overdrawn / Underdrawn tolerance check
        max_allowed = lc_amount_usd * (1.0 + tolerance_pct / 100.0)
        min_allowed = lc_amount_usd * (1.0 - tolerance_pct / 100.0)
        if invoice_amount_usd > max_allowed:
            discrepancies.append(f"EXCESS_DRAWING: Invoice ${invoice_amount_usd:,.2f} exceeds LC maximum ${max_allowed:,.2f} with {tolerance_pct}% tolerance.")
        elif invoice_amount_usd < min_allowed:
            discrepancies.append(f"UNDER_DRAWING: Invoice ${invoice_amount_usd:,.2f} below allowed minimum ${min_allowed:,.2f}.")

        # 3. Claused BL check
        if not is_clean_bill_of_lading:
            discrepancies.append("CLAUSED_BILL_OF_LADING: Marine transport document contains notation indicating defective packaging or cargo (UCP 600 Art 27).")

        has_fatal_discrepancy = len(discrepancies) > 0

        return {
            "lc_number": lc_number,
            "discrepancies_detected_count": len(discrepancies),
            "is_clean_presentation": not has_fatal_discrepancy,
            "bank_rejection_risk": "CRITICAL_REJECTION_GUARANTEED" if has_fatal_discrepancy else "CLEAN_COMPLIANT",
            "discrepancy_list": discrepancies,
            "recommended_action": "Request immediate SWIFT MT707 LC amendment from buyer before presenting documents to negotiating bank." if has_fatal_discrepancy else "Proceed with documentary presentation to nominated bank."
        }

    @staticmethod
    def generate_swift_mt707_amendment_request(lc_number: str, issuing_bank_swift: str, requested_latest_shipment_date: str, amendment_reason: str) -> Dict[str, Any]:
        """Generate structured SWIFT MT707 Amendment template."""
        swift_body = (
            f":20: TRANSFERRING BANK REF\n"
            f":21: {lc_number}\n"
            f":52A: {issuing_bank_swift}\n"
            f":31E: {requested_latest_shipment_date}\n"
            f":79: AMENDMENT DETAILS: Extension of latest shipment date to {requested_latest_shipment_date} due to {amendment_reason}. All other terms remain unchanged."
        )

        return {
            "swift_message_type": "MT707",
            "issuing_bank": issuing_bank_swift,
            "lc_number": lc_number,
            "raw_swift_payload": swift_body,
            "status": "READY_FOR_TRANSMISSION"
        }
