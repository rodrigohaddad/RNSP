from os import listdir, path
from subprocess import run
from os.path import isfile, join

config_files = [path.abspath(f) for f in listdir(
    "configs/") if isfile(join("configs/", f))]
command = "sbatch --job-name={job_name}.job --output=.out/{job_name}.out --error=.out/{job_name}.err -c 1 /home/gabriel-milan/GIT_REPOS/rnsp/tp1/prod/scripts/run.sh {config_file}"

i = 0
for config_file in config_files:
    cmd = command.format(job_name="train_{}_{}".format(i, config_file.split("/")[-1]),
                         config_file=config_file)
    print(cmd)
    i += 1
