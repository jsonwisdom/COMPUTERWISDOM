<!DOCTYPE html>
<html lang="en">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Compute Wisdom · Claim Parser Badge (KP-001) · Candidate</title>
    <style>
        * {
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }

        /* Cybernetic courtroom aesthetic — warm gold paper, black monospace */
        .badge-container {
            display: flex;
            justify-content: center;
            align-items: center;
            min-height: 100vh;
            background: #1a1a1a; /* dark courtroom walls */
            padding: 2rem;
        }

        .kp-badge {
            max-width: 480px;
            width: 100%;
            background: #fef9e8; /* warm gold paper */
            border-left: 8px solid #d97706;
            font-family: 'Courier New', 'SF Mono', monospace;
            box-shadow: 12px 12px 0 rgba(0,0,0,0.15);
            transition: all 0.2s ease;
        }

        /* Merkle branch motif — visual hash tree in border/background */
        .kp-badge {
            position: relative;
            background-image: 
                repeating-linear-gradient(90deg, 
                    rgba(217, 119, 6, 0.08) 0px, 
                    rgba(217, 119, 6, 0.08) 2px,
                    transparent 2px,
                    transparent 8px);
        }

        /* Merkle nodes as subtle pseudo-elements */
        .kp-badge::before {
            content: '';
            position: absolute;
            top: 20px;
            right: 20px;
            width: 80px;
            height: 80px;
            background-image: radial-gradient(circle at center, #d97706 1px, transparent 1px);
            background-size: 8px 8px;
            opacity: 0.3;
            pointer-events: none;
        }

        .badge-header {
            padding: 1.5rem 1.5rem 0.75rem 1.5rem;
            border-bottom: 1px solid #e2dccd;
        }

        .badge-title {
            font-size: 1.2rem;
            font-weight: 700;
            letter-spacing: -0.5px;
            color: #1a1a1a;
            display: flex;
            align-items: center;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin-bottom: 0.75rem;
        }

        .badge-icon {
            font-size: 1.6rem;
        }

        .badge-sub {
            font-size: 0.7rem;
            color: #6b5e3a;
            text-transform: uppercase;
            letter-spacing: 1px;
        }

        .proof-link {
            display: inline-flex;
            align-items: center;
            gap: 0.35rem;
            background: #1a1a1a;
            color: #fef9e8;
            font-size: 0.65rem;
            padding: 0.2rem 0.6rem;
            border-radius: 0px;
            margin-top: 0.5rem;
            font-family: monospace;
            text-decoration: none;
        }

        .badge-body {
            padding: 1.25rem 1.5rem;
        }

        .status-row {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 1rem;
            flex-wrap: wrap;
            gap: 0.75rem;
        }

        .status-badge {
            font-size: 0.7rem;
            padding: 0.25rem 0.75rem;
            font-weight: bold;
            font-family: monospace;
            border-left: 3px solid currentColor;
            background: rgba(0,0,0,0.03);
        }

        .status-verified { color: #1a7f3a; border-left-color: #1a7f3a; }
        .status-held { color: #b45309; border-left-color: #b45309; }
        .status-pending { color: #7c6e3c; border-left-color: #7c6e3c; }
        .status-rejected { color: #9b1c1c; border-left-color: #9b1c1c; }

        .claim-tag-row {
            display: flex;
            gap: 0.5rem;
            flex-wrap: wrap;
            margin: 1rem 0;
        }

        .claim-tag {
            font-size: 0.65rem;
            background: #e9e5d8;
            padding: 0.2rem 0.6rem;
            border-radius: 0px;
            font-family: monospace;
            font-weight: normal;
            letter-spacing: 0.5px;
        }

        .badge-data {
            background: #f5f0e3;
            padding: 0.75rem;
            margin: 1rem 0;
            font-size: 0.7rem;
            font-family: monospace;
            border: 1px dashed #d6cfa5;
            word-break: break-all;
        }

        .badge-footer {
            padding: 0.75rem 1.5rem;
            background: #f3efdf;
            font-size: 0.65rem;
            color: #4a3f28;
            border-top: 1px solid #e2dccd;
            text-align: center;
        }

        hr {
            margin: 0.5rem 0;
            border: none;
            border-top: 1px dotted #d6cfa5;
        }

        /* No JavaScript, no backend claims */
    </style>
</head>
<body>
<div class="badge-container">
    <!-- 
        ⚠️ CANDIDATE BADGE — NOT LIVE
        Portal.html mutation: FORBIDDEN
        Public display: NOT AUTHORIZED WITHOUT JAY APPROVAL + PROMOTION RECEIPT
        Proof linkage required: Knowledge Proof object must exist
    -->
    <div class="kp-badge"
         data-badge-name="Compute Wisdom Claim Parser"
         data-badge-version="KP-001-candidate"
         data-status="VERIFIED"
         data-proof-hash="PENDING_VERIFICATION"
         data-proof-link="HELD"
         data-issuer="jaywisdom.base.eth"
         data-candidate-only="true"
    >
        <div class="badge-header">
            <div class="badge-title">
                <span class="badge-icon">⚙️🧾</span>
                <span>Claim Parser · KP-001</span>
            </div>
            <div class="badge-sub">Compute Wisdom · Knowledge Proof Module</div>
            <div class="status-row">
                <span class="status-badge status-verified">VERIFIED (CANDIDATE PROOF)</span>
                <span class="proof-link">📎 Proof: HELD_PENDING_RECEIPT</span>
            </div>
        </div>

        <div class="badge-body">
            <div class="claim-tag-row">
                <span class="claim-tag">PUBLIC: Badge design</span>
                <span class="claim-tag">HELD: Live attestation</span>
                <span class="claim-tag">PENDING: Promotion receipt</span>
                <span class="claim-tag">REJECTED: None (no false claims)</span>
            </div>

            <div class="badge-data">
                <strong>📋 Machine-readable claims</strong><br>
                badge_name: Compute_Wisdom_Claim_Parser<br>
                status: VERIFIED_WITH_LIMITATION<br>
                proof_required: true<br>
                linked_proof: receipts/deep_seek_session_002_receipt.json <span class="claim-tag">HELD</span><br>
                portal_mutation: false<br>
                public_badge_granted: false
            </div>

            <div class="badge-data">
                <strong>🌿 Merkle branch motif (hash tree anchor)</strong><br>
                merkle_root: ff55a1fb6ef07adbeea057aed4997a61<br>
                session_hash: PENDING_AFTER_CAPTURE
            </div>

            <hr>

            <div style="font-size: 0.7rem; margin-top: 0.5rem;">
                ⚖️ <strong>Zero Trust Checkpoint</strong><br>
                - No live attestation (EAS/ENS)<br>
                - No portal mutation<br>
                - No public badge claim<br>
                - Requires Knowledge Proof object + Jay approval
            </div>
        </div>

        <div class="badge-footer">
            🧾 Knowledge Proof required for display · Badge without proof = decoration · Skill is proven, not asserted
        </div>
    </div>
</div>
</body>
</html>
