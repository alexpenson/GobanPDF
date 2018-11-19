from setuptools import setup

setup(
    # Needed to silence warnings (and to be a worthwhile package)
    name='GobanPDF',
    url='https://github.com/alexpenson/GobanPDF',
    author='Alex Penson',
    author_email='alexpenson@gmail.com',
    # Needed to actually package something
    packages=['GobanPDF'],
    # Needed for dependencies
    install_requires=['numpy', 'pandas', 'sgfmill', 'plotnine'],
    # *strongly* suggested for sharing
    version='0.1',
    # The license can be anything you like
    license='MIT',
    description='Make a pdf from an sgf file',
    # We will also need a readme eventually (there will be a warning)
    long_description=open('README.md').read(),
)
