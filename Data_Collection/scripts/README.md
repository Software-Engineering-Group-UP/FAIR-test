```
+- FAIR-test
    +- data_collection
        +- results
            .
            .
        +- scripts
            +- collect_org_repos.py  # collect all the repositories within the organisation 
            +- howfairis_org.py      # Enriches the collected repositories with howfairis variable
            +- all_testing.py        # Collects and save 
                     
```

We have used SWORDS-UP to gather repositories and organisation/ research group names. Although it is not the most effective way to find out 
research groups and repositories associated with university as university of potsdam has no central place (dedicated github organisation) to list
all the research groups. 
With the help of swords and playing around with the keywords we found the research groups available 
We found out (Link to results readme table) research groups that we have analysed 


### Steps of data collection 

After finding the research group name 

1. Collect Organisation repositories- navigate to  ../scripts 
run following command 


make folder with <organisation_name>
and <research_group_name> in results folder
```
python test_folder.py <resarch_group_name> --csv_path ../results/<organisation_name>/<research_group_name>
```



