import os
import sys
import glob
import platform

repo_dir = os.path.abspath(os.path.dirname(__file__))

# First, check the RELIA_GR_PYTHON_PATH environment variable

relia_gr_python_path = os.environ.get('RELIA_GR_PYTHON_PATH')
expected_relia_gr_python_path = os.path.join(repo_dir, 'python')

error_path = False

if not relia_gr_python_path:
    print("Error: RELIA_GR_PYTHON_PATH not found", file=sys.stderr)
    error_path = True
elif relia_gr_python_path != expected_relia_gr_python_path:
    print(f"Error: wrong RELIA_GR_PYTHON_PATH found ({relia_gr_python_path})", file=sys.stderr)
    error_path = True

if error_path:
    print(f"You should have an environment variable (e.g., in ~/.bashrc) the following:", file=sys.stderr)
    print(f"export RELIA_GR_PYTHON_PATH={expected_relia_gr_python_path}")
else:
    print("RELIA_GR_PYTHON_PATH is properly installed")
    

# Second, make sure that all the blocks are properly linked

# From gnuradio.core.Constants
DEFAULT_HIER_BLOCK_LIB_DIR = os.path.expanduser('~/.grc_gnuradio')

if not os.path.exists(DEFAULT_HIER_BLOCK_LIB_DIR):
    os.mkdir(DEFAULT_HIER_BLOCK_LIB_DIR)

if 'windows' in platform.system().lower():
    for filename in glob.glob(os.path.join(repo_dir, "blocks", "*.block.yml")):
        base_filename = os.path.basename(filename)
        target_file = os.path.join(DEFAULT_HIER_BLOCK_LIB_DIR, base_filename)

        print(f"Overriding {filename} in {target_file}")
        shutil.copyfile(filename, target_file)
else:
    for filename in glob.glob(os.path.join(repo_dir, "blocks", "*.block.yml")):
        base_filename = os.path.basename(filename)
        target_file = os.path.join(DEFAULT_HIER_BLOCK_LIB_DIR, base_filename)

        if not os.path.exists(target_file):
            print(f"Creating symlink {target_file} -> {filename}")
            os.symlink(filename, target_file)
        else:
            if os.readlink(target_file) != filename:
                print(f"Error: {target_file} is not pointing to {filename}", file=sys.stderr)
            else:
                print(f"{target_file} properly installed")

