from setuptools import setup
from setuptools.command.build_ext import build_ext
from Cython.Build import cythonize
from Cython.Compiler import Options

Options.docstrings = False

link_args = ['-static-libgcc',
            '-static-libstdc++',
            '-Wl,-Bstatic,--whole-archive',
            '-lwinpthread',
            '-Wl,--no-whole-archive']

class Build(build_ext):
    def build_extensions(self):
        if self.compiler.compiler_type == 'mingw32':
            for e in self.extensions:
                e.extra_link_args = link_args
        super(Build, self).build_extensions()

setup(
    ext_modules = cythonize("app.py"),
    cmdclass={'build_ext': Build},
    embed = True,
)

# python setup.py build_ext --inplace