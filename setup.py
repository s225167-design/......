from setuptools import setup, find_packages

setup(
    name="forum-v5",
    version="5.0.0",
    description="企业级全栈论坛",
    author="Your Name",
    author_email="your@email.com",
    packages=find_packages(),
    install_requires=[
        "Flask>=3.0.0",
        "Flask-CORS>=4.0.0",
        "PyJWT>=2.8.0",
        "bcrypt>=4.1.2",
        "python-dotenv>=1.0.0",
        "redis>=5.0.1",
    ],
    python_requires=">=3.11",
)
