# PACER Token Cache

Status: SHELL_ONLY
Authority: false
Implementation: NOT_YET

Reserved for persistent PACER session/token state across process and cron restarts.

Required properties:
- encrypted-at-rest or delegated secret-store backing
- no token value in receipts or logs
- atomic replacement on reissue/invalidation
- explicit environment partitioning (qa vs production)
- fail closed on unreadable/corrupt cache
- cache existence does not imply token validity
