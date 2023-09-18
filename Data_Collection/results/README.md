

### Organizations 
The organisations inlcuded in this study are listed below 

column name``organization`` states the name of organisation, ``number of research group`` and ``no. of repositories``states the total number of research groups and their opensource repositories.  

| organization                                                                                                 | No of research groups | No of repositories | GitHub repo link                                                | 
|--------------------------------------------------------------------------------------------------------------|-----------------------|--------------------|-----------------------------------------------------------------|
| [University of Potsdam](./university_of_potsdam)                                                             | 7                     | 174                | [Link]()                             |
| [Hasso Plattner Institute](./hasso_plattner_institute)                                                       | 5                     | 282                | [Link]()                   |
| [Helmholtz Centre Potsdam / GFZ German](./helmholz_center-gfz_potsdam)                                       | 3                     | 49                 | [Link]()         |
| [Startup](./startups)                                                                                        | 2                     | 310                | [Link]()            |
| [Potsdam institute of climate impact research](./potsdam_institute_for_climate_impact_research)              | 5                     | 111                | [Link]()                             |
| [Alfred-Wegener Institute](./alfred-wegener_institute)                                                       | 2                     | 32                 | [Link]() |
| [Berlin-Brandenburgische Akademie der Wissenschaften](./berlin-brandenburgische_akademie_der_wissenschaften) | 2                     | 53                 | [Link]()                |
| [Leibniz Institute](./leibniz_institute)                                                                     | 2                     | 32                 | [Link]()                          |


### Data 
        
* General Repository Info

    - **`name`**: The name of the repository.
      - **`owner`**: Information about the owner of the repository, stored as a dictionary-like string.
      - **`description`**: A text description of the repository.
      - **`language`**: The primary programming language used in the repository.
      - **`forks_count`**: The number of forks the repository has.
      - **`stargazers_count`**: The number of stars the repository has received.

* URLs and Identifiers
    
    - **`html_url`**: URL for the events related to the repository.
      - **`tags_url`**: URL where the tags for the repository can be found.
      - **`notifications_url`**: URL for the notifications related to the repository.
    
* FAIR Score and Related
  **`automated_testing`**: Boolean indicating whether automated testing is present.
      - **`howfairis_repository`**: Boolean indicating the FAIRness (Findable, Accessible, Interoperable, Reusable) in terms of repository aspects.
      - **`howfairis_license`**: Boolean indicating the FAIRness in terms of license.
      - **`howfairis_registry`**: Boolean indicating the FAIRness in terms of registry.
      - **`howfairis_citation`**: Boolean indicating the FAIRness in terms of citation.
      - **`howfairis_checklist`**: Boolean indicating the FAIRness based on a checklist.
      - **`fair_score`**: A score related to the FAIRness of the repository.    
  
    
    ## Date and Groups
    
    - **`date`**: The date on which the data for this entry was recorded.
      - **`organisation`**: The organization type to which the repository belongs.
      - **`researchGroup`**: The specific research group associated with the repository.
      """




### Analysis and results
* [combined.csv](combined.csv) is the meta data collected about the opensource organization/ research group repositories. 
* The results can be found [here](analysis_potsdam.ipynb).
* We have found that python and r are widely used in research groups in potsdam. So the [with_test_combined.csv](with_test_combined.csv) enriched data collected for the qualitative analysis. 