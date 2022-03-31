from setuptools import setup

setup(
    name='MatOS',
    version='0.1.0',
    description='MatOS System Classes',
    url='https://github.com/Ixonblitz-MatOS/MatOSPip',
    author='Ixonblitz',
    author_email='mathew@onpointlinux.com',
    license='BSD 2-clause',
    packages=['pyexample'],
    install_requires=['psutil','cpuinfo','wmi' 'platform','colorama','datetime','netifaces','GPUtil','tabulate','socket'],
    classifiers=[
        'Development Status :: 3 - Done',
        'Intended Audience :: Computer Programming',
        'License :: OSI Approved :: BSD License',
        'Operating System :: POSIX :: Linux',
        'Programming Language :: Python :: 3.10',
    ],
)
