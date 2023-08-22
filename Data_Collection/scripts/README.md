```
. FAIR-test
└──  data_collection
    ├── results # collected and enriched data with analysis
    └── scripts      # scripts to collect repositories and users with metadata              
        ├── collect_org_repos.py  # collect all the repositories within the organisation
        ├── howfairis_org.py      # Enriches the collected repositories with howfairis variable             
        └── all_testing.py        # Collects and save

```

We have used SWORDS-UP to gather repositories and organisation/ research group names. Although it is not the most effective way to find out 
research groups and repositories associated with university as university of potsdam has no central place (dedicated github organisation) to list
all the research groups. 
With the help of swords and playing around with the keywords we found the research groups available 
We found out (Link to results readme table) research groups that we have analysed 


### Steps of data collection 
 We followed ETL (Extract Transform Load Process). Some of the steps has to be done manually. 


####  1. Extract 
After finding the research group name 

1. Collect Organisation repositories- navigate to  ../scripts 
run following command 


make folder with <organisation_name>
and <research_group_name> in results folder
```
python collect_org_repos.py <resarch_group_name> --csv_path ../results/<organisation_name>/<research_group_name>
```

for example If you want to collect data for research group software engineering you found on github and it is associated with universtiy of potsdam than

<research_group_name> will be software_engineering and <organisation_name> will be university of potsdam. You will have to create folder <organisation_name> and 
sub folder <research_group_name_folder>

2. Collect howfairis complience 

```
python howfairis_org.py --input ../results/<organisation_name>/<research_group_name_folder>/<research_group_name>.csv --output ../results/<organisation_name>/<research_group_name_folder>/<research_group_name>.csv 
```

3. Collect all testing details 
If testing is done, if github actions or cicd implemented and if automated testing is implemented
```
 python all_testing.py ../results/<organisation_name>/<research_group_name_folder>/<research_group_name>.csv  
```

4. Combine results in single .csv file

```
 python combine_csv.py 
 ```
5. Count the fair score and save in a new .csv file column

```
python fair_score_counting.py <input>.csv
```


```
python append_org_researchGroup_names.py ../results/university_of_potsdam/AEye/aeye-lab.csv --organization "university_of_potsdam" --research_group "aeya"
```