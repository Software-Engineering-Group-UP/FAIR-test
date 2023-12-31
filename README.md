### Background

Scientific software developers/ research software developers are increasingly employing various software engineering practices for developing scientific software or also called as research software.
There are many studies that points out the need of empirical evaluation of the use of testing techniques, methods, and practices in research software developer community. 
Our goal is to collect and analyse a dataset of opensource research software repositories which can be used to empirically evaluate the software testing and quality component.

In this study we collected repositories from over 7 organizations which has 21 research groups and collective collection of 815 repositories and 2 startups with around 310 open repositories. 

We have also included research focus startups which would help to compare the testing across domains.

    
    
    
    
### Installation 
    
    
    
#### Requirements 
    
    git 
    python 
    pip 
    
#### Steps 
Clone this project  
```
git clone https://github.com/Software-Engineering-Group-UP/FAIR-test.git
```
Create a virtual environment at project root, and activate it 
    
```
cd FAIR-test
    
python -m venv venv
    
./venv/Scripts/activate.bat
    
```
    
    
### Create a virtual environment 

Note that you need to create a .env file in the root directory of the project and add the following lines:
```
ACCESS_TOKEN = "your github access token" 
USER = "your github username" 
```
Look at the documentation here:  https://docs.github.com/en/github/authenticating-to-github/creating-a-personal-access-token
    
### Project structure
    
    ├── data_collection                     # results and scripts to collect the data  
    │  ├── results                          # Folder that contains the results of data collected through scripts
    │  │    ├── <organisation_name>	            # Folder contains all research groups in perticular organisation 
    │  │    │    └── <research_group_name>      # Folder contains .csv file collected and enriched for analysis accessing the qualtiy of research software 
    │  │    │        └──<research_group_name>.csv
    │  │    └──README.md 
    │  └── Scripts 
    │       ├── all_testing.py                   # collect all the repositories within the organisation
    │       ├── collect_org_repos.py             # Collects and save
    │       ├── howfairis_org.py                 # Enriches the collected repositories with howfairis variable
    │       └── combine_csv.py                   # Combines all .csv files in to single csv file.
    ├── .gitignore				                # Defines content which shouldn't be tracked by Git
    ├── CITATION.cff			                # Human- and machine-readable citation information for software
    ├── LICENSE				                    # License used for this software project
    └── README.md				                # Documentation of this project
    
    
     
### Usage 
You can find the 
    
### License 