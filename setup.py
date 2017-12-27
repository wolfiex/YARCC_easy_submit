from setuptools import setup

setup(name='yarcc_easy',
      version='0.0.1',
      description='Simple submission script maker and job starter.',
      url='https://github.com/wolfiex/YARCC_easy_submit',
      author='Dan Ellis',
      author_email='daniel.ellis.research@gmail.com',
      license='MIT',
      packages=['yarcc_easy'],
         install_requires=[
            'sys',
            're',
            'argparse',
            'os',
        ],
      zip_safe=True)
