from setuptools import setup, find_packages

with open('README.md') as readme_file:
    README = readme_file.read()

setup_args = dict(
    name='amazon_product_review_scraper',
    packages=find_packages(),
    version='0.1',
    description='Python package to scrape product review data from amazon',
    long_description_content_type="text/markdown",
    long_description=README,
    license='MIT',
    keywords=["Scraper", "Amazon", "Reviews"],
    author='Harsh Singhal',
    author_email='harshsinghal726@gmail.com',
    python_requires='>=3.6',
)

install_requires = [
    'beautifulsoup4',
    'tqdm',
    'fake_useragent'
]

if __name__ == '__main__':
    setup(**setup_args, install_requires=install_requires)