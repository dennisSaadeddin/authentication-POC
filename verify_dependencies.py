import sys
import platform

def check_dependencies():
    print("Python Environment Check")
    print("-" * 30)
    
    # Python version
    print(f"Python Version: {platform.python_version()}")
    
    # Dependency versions
    dependencies = [
        "pydantic",
        "pydantic_settings",
        "fastapi",
        "sqlalchemy",
        "alembic"
    ]
    
    for dep in dependencies:
        try:
            module = __import__(dep)
            print(f"{dep}: {module.__version__}")
        except (ImportError, AttributeError):
            print(f"{dep}: Not installed")
    
    # Environment variables
    from app.core.config import get_settings
    settings = get_settings()
    print("\nConfiguration Check:")
    print(f"Secret Key: {'✓' if settings.SECRET_KEY else '✗'}")
    print(f"Database URL: {settings.DATABASE_URL}")

if __name__ == "__main__":
    check_dependencies() 