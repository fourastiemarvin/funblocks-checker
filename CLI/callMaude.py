import subprocess
# subprocess.run(["ls", "./master_project"])

# subprocess.run(["ls"])
# subprocess.run(["./maude-2.7-hooks-linux/maude++ ./maude-2.7-hooks-linux/MFE-mfe-2.7/src/mfe.maude"])
# subprocess.run(["./maude-2.7-hooks-linux/maude++"])
# subprocess.run(["./maude++ MFE-mfe-2.7/src/mfe.maude"])

subprocess.run(["./maude++ MFE-mfe-2.7/src/mfe.maude ../tools/Parser/Sources/fun.mfe"])
# call with a one liner !!!!!!
#./maude++ MFE-mfe-2.7/src/mfe.maude ../tools/Parser/Sources/fun.mfe
