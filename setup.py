from setuptools import setup, find_packages

setup(
    name="your-app-name",
    version="1.0.0",
    packages=find_packages(),
    install_requires=[
        "Flask==2.3.3",
        "Flask-Login==0.6.3", 
        "SQLAlchemy==2.0.23",
        "python-dotenv==1.0.0",
        "gunicorn==21.2.0",
        "Werkzeug==2.3.7"
    ],
)