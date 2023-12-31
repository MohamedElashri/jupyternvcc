import os
import subprocess
import sys
sys.path.insert(0, os.path.dirname(__file__))
# Add the tmp dir to be the same as the current dir
os.environ['TMPDIR'] = '.'
from IPython.core.magic import Magics, cell_magic, magics_class
from IPython.core.magic_arguments import argument, magic_arguments, parse_argstring
import jupyternvcc_helper

compiler = '/usr/local/cuda/bin/nvcc'


@magics_class
class NVCCPLUGIN(Magics):

    def __init__(self, shell):
        super(NVCCPLUGIN, self).__init__(shell)
        self.argparser = jupyternvcc_helper.get_argparser()
        current_dir = os.getcwd()
        self.output_dir = os.path.join(current_dir, 'src')
        if not os.path.exists(self.output_dir):
            os.mkdir(self.output_dir)
            print(f'created output directory at {self.output_dir}')
        else:
            print(f'directory {self.output_dir} already exists')

        self.out = os.path.join(current_dir, "result.out")
        print(f'Out bin {self.out}')

    @staticmethod
    def compile(output_dir, file_paths, out, options): #include options parameter
        print(f"Options received: {options}")
        cmd = [compiler, '-I' + output_dir, file_paths, "-o", out, '-Wno-deprecated-gpu-targets']
        cmd += ['--compile'] if options.compile else []
        cmd += ['--run'] if options.run else []
        cmd += ['--cudart={}'.format(options.cudart)]
        cmd += ['--std={}'.format(options.std)]
        cmd += ['--threads={}'.format(options.threads)]
        cmd += ['-arch={}'.format(options.arch)]

        # Run the nvcc compiler
        try:
            print(" ".join(cmd))
            open(out, "w").close()
            res = subprocess.check_output(cmd, stderr=subprocess.STDOUT)
        except subprocess.CalledProcessError as e:
            print("Compilation failed: ", e.output)
            return

        # Change the permissions of the output file to be read, write, and executable for everyone
        os.chmod(out, 0o755)
        res = res.decode()
        jupyternvcc_helper.print_out(res)
        return None

    @magic_arguments()
    @argument('-n', '--name', type=str, help='file name, must end with .cu extension')
    @argument('-c', '--compile', action='store_true', help='Should it be compiled?')
    @argument('-r', '--run', action='store_true', help='Should it be run?')
    @argument('-t', '--timeit', action='store_true', help='Should it be timed?')
    @argument('--cudart', type=str, default='static', help='Cuda runtime version (default static)')
    @argument('--std', type=str, default='c++14', help='C++ standard (default c++14)')
    @argument('--threads', type=int, default=1, help='Number of threads (default 1)')
    @argument('-arch', type=str, default='sm_70', help='GPU architecture (default sm_70)')
    @cell_magic
    def cuda(self, line='', cell=None):
        args = parse_argstring(self.cuda, line)

        ex = args.name.split('.')[-1]
        if ex not in ['cu', 'h']:
            raise Exception('name must end with .cu or .h')

        if not os.path.exists(self.output_dir):
            print(f'Output directory does not exist, creating')
            try:
                os.mkdir(self.output_dir)
            except OSError:
                print(f"Creation of the directory {self.output_dir} failed")
            else:
                print(f"Successfully created the directory {self.output_dir}")

        file_path = os.path.join(self.output_dir, args.name)
        with open(file_path, "w") as f:
            f.write(cell)
        print(f'Parsed arguments: {args}')

        if args.compile:
            try:
                self.compile(self.output_dir, file_path, self.out, args)  # pass args as options
                output = self.run(timeit=args.timeit)
            except subprocess.CalledProcessError as e:
                jupyternvcc_helper.print_out(e.output.decode("utf8"))
                output = None
        else:
            output = f'File written in {file_path}'

        return output
    
    def run(self, timeit=False):
        if timeit:
            stmt = f"subprocess.check_output(['{self.out}'], stderr=subprocess.STDOUT)"
            output = self.shell.run_cell_magic(
                magic_name="timeit", line="-q -o import subprocess", cell=stmt)
        else:
            output = subprocess.check_output(
                [self.out], stderr=subprocess.STDOUT)
            output = output.decode('utf8')

        helper.print_out(output)
        return None

    @cell_magic
    def cuda_run(self, line='', cell=None):
        try:
            args = self.argparser.parse_args(line.split())
        except SystemExit:
            self.argparser.print_help()
            return

        try:
            cuda_src = os.listdir(self.output_dir)
            cuda_src = [os.path.join(self.output_dir, x)
                        for x in cuda_src if x[-3:] == '.cu']
            print(f'found sources: {cuda_src}')
            self.compile(self.output_dir, ' '.join(cuda_src), self.out, args)  # pass args as options
            output = self.run(timeit=args.timeit)
        except subprocess.CalledProcessError as e:
            jupyternvcc_helper.print_out(e.output.decode("utf8"))
            output = None

        return output
