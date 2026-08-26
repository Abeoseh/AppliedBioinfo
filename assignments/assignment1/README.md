


### Assignment 1
1. Follow the Getting Started instructions to set up your computer.
2. Install an AI ready code editor as described on the page.
3. Create a GitHub account and create a public repository under your account.
4. Create a new directory for this week's assignment. Add a README.md file to the directory
5. Write the commands and their outputs into the README.md file. Format it nicely.
    From within the AppliedBioinfo folder
```bash
mkdir -p assignments/assignment1
cd assignments/assignment1
touch README.md
```

6. What version is your samtools command in the bioinfo environment?
```bash
conda activate bioinfo
samtools --version
```
output: samtools 1.24


7. Show commands needed to create a nested directory structure.
```bash
mkdir -p assignments/assignment1
```
The -p creates a nested directory structure 


8. Show commands that create files in different directories
If you just want to make it:
```bash
touch README.md
```
If you want to make it and open it:
```bash
nano README.md
```
If you want to make it while adding text to it:
```bash
echo "#Assignment 1" > README.md
```

9. Show how to access these files using relative and absolute paths.
Establishing where we are:
```bash
pwd
```
/mnt/c/Users/brean/Downloads/phd/AppliedBioinfo/
Relative:
```bash
nano ./assignments/assignment1/README.md
```
Absloute
```bash
nano /mnt/c/Users/brean/Downloads/phd/AppliedBioinfo/assignments/assignment1/README.md
```

10. Commit and push your changes to the repository.
```git
git add .
git commit -m "assignment 1"
git push
```
Submit the link to your repository.