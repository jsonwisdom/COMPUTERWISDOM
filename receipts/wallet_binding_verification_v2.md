# Wallet Binding Verification V2

Run:

```bash
sha256sum receipts/wallet_binding_message_v2.txt
wc -c receipts/wallet_binding_message_v2.txt
cat receipts/wallet_binding_message_v2.txt
```

Expected SHA256:

```text
2c86524411ec74eee1c5a393148461eb65a1f3f9b6ea4f52ca90ba10b5a2fccc
```

Expected bytes:

```text
772
```

Required recovered signer:

```text
0xa380552a27b0a5a2874ea7aa52cac09f542002e8
```

Gate remains pending until signature recovery proves the signer.
