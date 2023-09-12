from distutils.core import setup

setup(
    name='nvccplugin',
    version='0.1',
    author='Mohamed Elashri',
    author_email='nvccplugin@elashri.com',
    py_modules=['nvcc_plugin', 'jupyternvcc.jupyternvcc_plugin', 'jupyternvcc.jupyternvcc_helper'],
    url='https://github.dev/MohamedElashri/jupyternvcc',
    license='LICENSE',
    description='A plugin to run CUDA C/C++ in Jupyter Notebook using magic cell commands',
)