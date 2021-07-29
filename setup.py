from setuptools import setup, find_packages

# with open("readme.md", "r", encoding="utf-8") as fh:
#     long_description = fh.read()

setup(
    name="secyan_gen",
    version="0.2.0",
    author="Qiwei Li",
    author_email="sirily1997@gmail.com",
    description="Code parser with secyan_python",
    long_description="",
    long_description_content_type="text/markdown",
    zip_safe=False,
    platforms=['any'],
    classifiers=['Programming Language :: Python :: 3.6',
                 'Programming Language :: Python :: 3.7',
                 'Programming Language :: Python :: 3.8',
                 'Programming Language :: Python :: 3.9', ],
    python_requires='>=3.6',
    install_requires=[
        "setuptools",
        "wheel",
        "secyan_python",
        "sqlparse",
        "jinja2",
        "psycopg2-binary",
    ],
    packages=find_packages(),
    package_dir={"codegen": "codegen"}
)
