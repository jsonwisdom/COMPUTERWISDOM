from app.csv_ingest import ingest_csv
from app.report import save_report

events = ingest_csv("examples/sample_coinbase_export.csv")
save_report(events, "examples/sample_report.json")
print("WROTE examples/sample_report.json")
