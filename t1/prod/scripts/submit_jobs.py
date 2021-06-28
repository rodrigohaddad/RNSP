from random import sample
from os import listdir, path
from subprocess import run
from os.path import isfile, join

SUBSET_SIZE = 100


def print_and_run(cmd: str):
    print(f"Executing command\"{cmd}\"...")
    run(cmd.split(" "))


config_files = [path.abspath("configs/" + f) for f in listdir(
    "configs/") if isfile(join("configs/", f))]
command = "/usr/bin/sbatch --job-name={job_name}.job -c 1 /home/gabriel-milan/GIT_REPOS/RNSP/t1/prod/scripts/run.sh {config_file}"

i = 0
for config_file in sample(config_files, k=SUBSET_SIZE):
    cmd = command.format(job_name="train_{}_{}".format(i, config_file.split("/")[-1]),
                         config_file=config_file)
    print_and_run(cmd)
    i += 1
