### Idea
Keeping track of how much time you spend on something is a good idea, but to extract a valuable information from this data requires a lot of effort. 
This program is meant to automate this process as much as possible for now with phone screen time and schedule time data. 

Screen time data is meant to be collected weekly from your special phone application.

Schedule time is meant to be collected weekly from whatever application you like to schedule your time with. 
One way to do this is to set up Notion Calendar with a database attached to it. 
Then you add a special formula propery that counts time of an event in hours. 
After that you create a tag propery (a schedule category you want to keep track of).
Then create a table view of this database, set boundaries for current week and sum time column. You will enter this value to Time Manager. 

It is important to schedule the day fully, so sleep time can be computed accurately (it equals to unscheduled time). 

### Installation
Just clone these files and run 
```
python3 time_manager.py
```
I suggest using a decorator script added to your PATH. 

### Configuration
Step I. Rename \*-sample.yaml files to \*.yaml. 

Step II. Fill in desired abolute paths where to store time data. Write current month to start from. 

Step III. Choose a subset of apps you want to track time of. **Total must always be included**

Step IV. Enter your schedule tags and Other (scheduled but not tagged time) category.

Step V. In entries.py specify an absolute path to configuration.yaml. In notion_api.py specify an absolute path to keys.yaml, if you intend to use Notion API integration. 

### Usage
Use commands from the hint panel: *schedule* to enter schedule time, *screen* to enter phone screen time, *present* to present stats for current month, ...
