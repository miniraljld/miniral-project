from setuptools import setup, find_packages

setup(
    name="water-supply-monitoring-platform",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "fastapi==0.115.0",
        "uvicorn[standard]==0.32.0",
        "sqlalchemy==2.0.35",
        "psycopg2-binary==2.9.9",
        "python-jose[cryptography]==3.3.0",
        "passlib[bcrypt]==1.7.4",
        "python-multipart==0.0.12",
        "pydantic==2.9.2",
        "pydantic-settings==2.6.1",
        "alembic==1.13.3",
        "python-dotenv==1.0.1",
        "cryptography==43.0.1",
        "requests==2.32.3",
        "click==8.1.7"
    ],
    author="MNIRAL Team",
    description="Веб-платформа мониторинга и управления системами водоснабжения",
    python_requires=">=3.8",
)