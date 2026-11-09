CREATE TABLE payment_exceptions (
  id TEXT PRIMARY KEY,
  risk_score INTEGER NOT NULL,
  received_at TEXT NOT NULL,
  resolution TEXT
);
