from distutils.core import setup
import setuptools

setup(name='nepx',
      version='0.1',
      description='Python interface for NEP',
      author='Ke XU',
      author_email='kickhsu@gmail.com',
      packages=setuptools.find_packages(),
      include_package_data=True,
      install_requires=['scipy',
                        'ase>=3.20.1'],
      )
