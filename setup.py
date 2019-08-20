from setuptools import find_packages, setup

setup(
  name='news-summarizer',
  version='0.0.1',
  author='Anyama Richard',
  author_email='anyamaronyango@gmail.com',
  description="An application for deploying an article summarizing model using NLP and Machine Learning",
  url="https://github.com/anyric/News-Summarizer",
  packages=find_packages(),
  include_packages_data=True,
  zip_safe=False,
  install_requires=[
    'APScheduler<=2.1.2',   
    'beautifulsoup4<=4.7.1',   
    'Flask<=1.0.2',
    'Flask-Bootstrap4<=4.0.2',
    'Flask-Cors<=3.0.7',  
    'gunicorn<=19.9.0',     
    'networkx<=2.2',   
    'nltk<=3.4',     
    'numpy<=1.16.2',  
    'pandas<=0.24.2',  
    'requests<=2.21.0',   
    'scipy<=1.2.1',
    'scikit-learn<=0.19.1',
    'lxml<=4.3.3'
  ],
  classifiers=[
    "Programming Language :: Python :: 3",
    "Operating System :: OS Independent",
    "Framework :: Flask"
    ],
  python_requires='<=3.6.5',
  package_data={
    'src': [
      'templates/*',
      'static/*',
      'static/img*',
      'databases/*',
      'databases/model/*'
      ],
  },
  exclude_package_data={
    '': ['__pycache__/']
    },
  entry_points={
    'console_scripts': [
      'manage=manage:app',
    ],
  }
)