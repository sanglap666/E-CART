import subprocess as cmd
import os


if __name__ == "__main__":
    
    cmd.run("git add .", check=True, shell=True)
   
    

    

    

    cp = cmd.run("git commit -m 'update '", check=True, shell=True)
    cp = cmd.run("git push -u origin master -f", check=True, shell=True)

    

    
