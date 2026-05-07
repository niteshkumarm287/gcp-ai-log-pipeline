from setuptools import setup, find_packages

setup(
    name="rag-pipeline",
    version="0.1.0",
    description="RAG Pipeline - Log ingestion for Vertex AI",
    author="Your Name",
    python_requires=">=3.11",
    packages=find_packages(),
    install_requires=[
        "flask>=3.0.3",
        "google-cloud-storage>=2.16.0",
        "gunicorn>=22.0.0",
        "functions-framework>=3.8.1",
        "google-cloud-aiplatform>=1.73.0",
    ],
    classifiers=[
        "Development Status :: 3 - Alpha",
        "Intended Audience :: Developers",
        "Programming Language :: Python :: 3.11",
    ],
)
