from setuptools import setup, find_packages

setup(
    name='video_sdk',
    version='0.2',
    description='视频处理',
    packages=find_packages(exclude=[]),
    author='suchang',
    include_package_data=True,
    long_description=__doc__,
    long_description_content_type="text/markdown",
    zip_safe=False,
    platforms='any',
    python_requires='>=2.7,!=3.0.*,!=3.1.*,!=3.2.*,!=3.3.*'
)
