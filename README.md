# Email Filter

* Install all requirments
```
pip install -r requirments.txt
```
* Write config.json 
  
  - Example:

    	"AND" : {
    				"contains" : [], 
    				"notcontains" : [ ["subject","confidential"]] ,
    				"older" : [],
    				"notolder" : []
    			},
    	"OR" : {
    			"contains" : [],
    			"notcontains" : [] ,
    			"older" : [],
    			"notolder" : [ ["date" , 4] ]
    		  },
    	"DO" : {
    		"add" : ["STARRED"],
    		"remove" : []
    	}
	
	- rules for a string(contains,notcontains) : [column_name,string_to_match]
	-  rules for a date(older,notcontains) : [column_name,(int) days ]

- Add  valid label ids
		
      "CATEGORY_PERSONAL"
      "CATEGORY_SOCIAL"
      "CATEGORY_UPDATES"
      "CATEGORY_FORUMS"
      "CHAT"
      "SENT"
      "TRASH"
      "CATEGORY_PROMOTIONS"
      "DRAFT"
      "SPAM"
      "STARRED"
      "UNREAD"
      "IMPORTANT"
    
* Run main.py