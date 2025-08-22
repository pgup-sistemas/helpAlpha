#!/usr/bin/env python3
"""
Script para gerar uma SECRET_KEY segura para produção
"""

import secrets

def generate_secret_key():
    """Gera uma chave secreta segura"""
    return secrets.token_urlsafe(32)

if __name__ == '__main__':
    key = generate_secret_key()
    print(f"SECRET_KEY={key}")
    print(f"\nChave gerada: {key}")
    print("\nAdicione esta chave ao seu arquivo .env:")
    print(f"SECRET_KEY={key}")
