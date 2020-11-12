import subprocess
import os




if __name__ == "__main__":
    subprocess.Popen(["git", "add", "."],stdout=subprocess.PIPE)

    subprocess.Popen(["git", "status"],stdout=subprocess.PIPE)

    subprocess.Popen(["git", "commit", "-m", "updating" ,"e-cart"],stdout=subprocess.PIPE)

    subprocess.Popen(["git", "push", "-u", "origin", "master"],stdout=subprocess.PIPE)

    

    