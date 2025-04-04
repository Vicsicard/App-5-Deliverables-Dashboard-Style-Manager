from setuptools import setup, find_packages

setup(
    name="deliverables_dashboard",
    version="0.1.0",
    packages=find_packages(),
    install_requires=[
        "supabase>=2.0.0",
        "python-dotenv>=1.0.0"
    ],
)
