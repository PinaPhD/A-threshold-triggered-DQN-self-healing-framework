Pre-requisites:
GitHub configuration
$git config –global user.name “PinaPhD”
$git config –global user.email amwangi@alumni.cmu.edu
$git config –global init.defaultBranch main
$git config –global --list
#Creating a repository (git init) in either the current directory or a directory name passed as the first argument to the command
$git init git-series
#Checking the status of files
$cd git-series
$git status
#Adding files to commit (a newly created file readme.md)
$echo "#Git Series Readme" > README.md
$git status
#Committing tracked files - or record our changes
$git commit
#Modifying existing files and reviewing changes
$echo >> README.md
$echo 'Welcome to my first local repository!' >> README.md
$git status
$git diff   #outputs most difference utility outputs
#use git mv ---> renaming files
#use git rm ---> removing files
#To view the commit log 
$git log
$git show



