import secrets
 
key = secrets.token_hex(32)
print(f"\nYour SECRET_KEY:\n\n{key}\n")
print(f"SECRET_KEY={key}\n")