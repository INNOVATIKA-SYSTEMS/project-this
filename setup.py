from setuptools import setup, find_packages

setup(
    name="project-this",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "fastapi",
        "uvicorn",
        "python-dotenv",
        "psycopg2-binary",
        # добавьте другие зависимости из requirements.txt если они есть
    ],
    author="Alan",
    description="for import",
    python_requires=">=3.7",
)