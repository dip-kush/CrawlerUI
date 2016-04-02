#Ajax Crawler

Clone the repository

	https://github.com/dip-kush/CrawlerUI/

Use the requirement file to install the dependency file

	pip install -r requirements.txt

### Instruction for using the sample_web_application

Copy the sample_web_application and paste in the xampp server 

and import the sample_web_application/forum.sql into the database

###Usage

    Run the Application first creat database
    python manage syncdb
    then run  
    python manage.py runserver

###Sample Command for using it in command line
   
Go inside the crawler/ directory

python ExtractDom.py -l login_script.html -u path_to_sample_application/login.php -f form_values.html

Edit the sample script to run

./run.sh
./script.sh


Once the Values are specified in the Crawling Specification press the submit button. There will be sample run and values will be stored in the database
Reload it .Check the last run in Last 4 runs tab
Now run the application from there. This will generate a workflow in the database.
After that click the Workflow button to print the workflows

Executing the workflow part needs to be added 
