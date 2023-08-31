To filrer the results merged .csv file excute the following script

1. filter_csv_prog.py
```
python scripts/qual_collect_scripts/filter_csv_prog.py results/combined.csv  results/with_test_combined.csv
```
run the above command from ```/data_collection directory``` 
This program will filter repos that have column name ```automated_testing``` true and with ```language``` as r and python as we found that these languages are used the most amoung research community around potsdam.

2. test_doc_cov.py 
This prorgam is only to append the values for column names in csv file 
* test_document: ```Bool```
```true``` if the repository have ```codecov``` badge or there is coverega report is already generated in repository
```false``` if the repository does not have ```codecov``` badge or there is no information provided about testing 

```
python test_doc_cov.py results/test_doc_cov.csv "http://example.com/page1" True "Method A" 95.0
```

This will read the existing data from ```results/with_test_combined.csv```, find the row where the html_url is "http://github_url", and update the test_document, test_document_method, and coverage columns for that row with the new values (True, "codecov", and 66, respectively). It will then save the updated DataFrame back to the original ```results/with_test_combined.csv``` file.


Eg. - 
python scripts/qual_collect_scripts/test_doc_cov.py results/with_test_combined.csv "https://github.com/EarthSystemDiagnostics/ncdftools" False "No test info" 0.0


