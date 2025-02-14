from setuptools import setup, find_packages

setup(
    name="funciones",
    version="0.1",
    packages=find_packages(),
    description="Paquete con funciones personalizadas",
    author="Roberto",
    author_email="porsche@live.com.ar",
    license="MIT",
    install_requires=[
        "matplotlib",  # Librerías necesarias
        "numpy"
    ],
)
