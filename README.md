# scotus-search

This Flask app searches Supreme Court opinions within a selected date range for mentions of SLS faculty members and student journals. It's currently deployed at https://scotus-search.herokuapp.com/. 

<h4>The important files:</h4>

<b>searchopinions.py</b> contains the function for searching opinions. It connects to the CourtListener API, finds all opinions (including opinions on orders) in the given date range, searches for any instances of the terms in the list of search terms, and returns any opinions found along with the locations of any matches. 

<b>search_app.py</b> is the app itself. It contains the list of search terms, calls the function in searchopinions.py (providing as parameters the list of search terms and the dates seleted by the user) and outputs the results to the home.html template.

<b>home.html</b> (in templates folder) is the html file on which all this displays. It doesn't look like a normal html file because it's a Flask template; all the stuff in curly brackets {{}} allows the app to dynamically generate html as the user searches, so that it displays the search form before the user searches, then displays the search results after on the same page. 

<h4>Everything else:</h4> 
<b>Procfile</b> and <b>requirements.txt</b> are required to deploy the app on Heroku. They provide information that it needs for the initial setup. 

The <b>static</b> folder contains CSS.

<h4>Maintaining the app:</h4>

The maintainer will need to create a free CourtListener account to get an API Key. Once you have an account, you can find your API Key here: https://www.courtlistener.com/profile/api/. Enter that key in <b>searchopinions.py</b> (header = {'Authorization': 'Token ENTER_KEY_HERE'}). Don't enter it in <b>search_app.py</b> - there's a variable in there called app.config['SECRET_KEY'], which looks like it might be an API key, but it isn't and you don't need to change that. 

If you want to deploy it on Heroku, create a free Heroku account and a GitHub account; create a new GitHub repository with all these files; create a new Heroku app from your dashboard; and in the Heroku app edit page, under the Deploy tab, connect to your GitHub account, select "Enable Automatic Deploys", then "Deploy Branch" at the bottom of the page. 

The only part of this that needs to be updated on an ongoing basis is the list of search terms in <b>search-app.py</b>
