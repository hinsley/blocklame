Block members:
- Message: 1024 byte fixed-length binary.
- Block index (0-indexed)
- Salt
- Timestamp (msec epoch time)
- Previous hash

Hash algorithm: SHA256

Mining function: Number of 0s at beginning of hash should be floor(log_2(block index))
