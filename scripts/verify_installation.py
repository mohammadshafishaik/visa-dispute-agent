#!/usr/bin/env python3
"""Verify installation and dependencies"""
import sys
import importlib


def check_import(module_name: str, package_name: str = None) -> bool:
    """Check if a module can be imported"""
    try:
        importlib.import_module(module_name)
        print(f"✓ {package_name or module_name}")
        return True
    except ImportError as e:
        print(f"✗ {package_name or module_name}: {e}")
        return False


def main():
    """Main verification"""
    print("\n" + "="*60)
    print("Visa Dispute Agent - Installation Verification")
    print("="*60 + "\n")
    
    print("Checking Python version...")
    if sys.version_info < (3, 11):
        print(f"✗ Python 3.11+ required, found {sys.version_info.major}.{sys.version_info.minor}")
        return False
    print(f"✓ Python {sys.version_info.major}.{sys.version_info.minor}.{sys.version_info.micro}")
    
    print("\nChecking core dependencies...")
    dependencies = [
        ("fastapi", "FastAPI"),
        ("uvicorn", "Uvicorn"),
        ("langgraph", "LangGraph"),
        ("langchain", "LangChain"),
        ("langchain_openai", "LangChain OpenAI"),
        ("pydantic", "Pydantic"),
        ("chromadb", "ChromaDB"),
        ("asyncpg", "AsyncPG"),
        ("httpx", "HTTPX"),
    ]
    
    all_ok = True
    for module, name in dependencies:
        if not check_import(module, name):
            all_ok = False
    
    print("\nChecking test dependencies...")
    test_deps = [
        ("pytest", "Pytest"),
        ("hypothesis", "Hypothesis"),
    ]
    
    for module, name in test_deps:
        if not check_import(module, name):
            all_ok = False
    
    print("\nChecking application modules...")
    app_modules = [
        "app.agents.dispute_graph",
        "app.api.main",
        "app.config.settings",
        "app.db.connection",
        "app.schema.models",
        "app.tools.rag_retriever",
        "app.tools.transaction_enrichment",
        "app.tools.circuit_breaker",
        "app.api.security",
        "app.api.monitoring",
    ]
    
    for module in app_modules:
        if not check_import(module):
            all_ok = False
    
    print("\n" + "="*60)
    if all_ok:
        print("✓ All checks passed! Installation is complete.")
        print("="*60 + "\n")
        print("Next steps:")
        print("1. Configure .env file with your API keys")
        print("2. Start infrastructure: docker-compose up -d")
        print("3. Run migrations: poetry run alembic upgrade head")
        print("4. Seed database: poetry run python scripts/seed_chromadb.py")
        print("5. Start server: make run")
        print("6. Run tests: make test")
        return True
    else:
        print("✗ Some checks failed. Please install missing dependencies.")
        print("="*60 + "\n")
        print("Run: poetry install")
        return False


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)
