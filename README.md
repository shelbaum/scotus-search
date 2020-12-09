# scotus-search

This Flask app searches Supreme Court opinions within a selected date range for mentions of SLS faculty members and student journals. It's currently deployed at https://scotus-search.herokuapp.com/. 

<h4>The important files:</h4>

<b>searchopinions.py</b> contains the function for searching opinions. It connects to the CourtListener API, finds all opinions (including opinions on orders) in the given date range, searches for any instances of the terms in the list of search terms, and returns any opinions found along with the locations of any matches. 

<b>search_app.py</b> is the app itself. It contains the list of search terms, calls the function in searchopinions.py (providing as parameters the list of search terms and the dates seleted by the user) and outputs the results to the home.html template.

<b>home.html</b> (in templates folder) is the html file on which all this displays. It doesn't look like a normal html file because it's a Flask template; all the stuff in curly brackets {{}} allows the app to dynamically generate html as the user searches, so that it displays the search form before the user searches, then displays the search results after on the same page. 

<h4>Everything else:</h4> 
<p><b>Procfile</b> and <b>requirements.txt</b> are required to deploy the app on Heroku. They provide information that it needs for the initial setup.</p>

<p>The <b>static</b> folder contains CSS, which is just <a href="http://getskeleton.com/">Skeleton boilerplate</a> plus a little custom CSS to make the search results collapsible.</p>

<h4>Maintaining the app:</h4>

The maintainer will need to create a free CourtListener account to get an API Key. Once you have an account, you can find your API Key here: https://www.courtlistener.com/profile/api/. Enter that key in <b>searchopinions.py</b> (line 9, header = {'Authorization': 'Token ENTER_KEY_HERE'}). Don't enter it in <b>search_app.py</b> - there's a variable in there called app.config['SECRET_KEY'], which looks like it might be an API key, but it isn't and you don't need to change it (although nothing bad will happen if you do). 

If you want to deploy it on Heroku, create a free Heroku account and a GitHub account; create a new GitHub repository with all these files; create a new Heroku app from your dashboard; and in the Heroku app edit page, under the Deploy tab, connect to your GitHub account, select "Enable Automatic Deploys", then "Deploy Branch" at the bottom of the page. 

The only part of this that needs to be updated on an ongoing basis is the list of search terms in <b>search-app.py</b>. The terms are case-sensitive and must be enclosed in quotation marks and separated with commas. Two special notes:
<ul><li>If you'd like to search for a name with and without a diacritic, or both capitalized and uncapitalized, you can enclose the possible characters in brackets: e.g. "Cu[eé]llar" will return both "Cuellar" and "Cuéllar", and "[Bb]rief" will return both "Brief" and "brief".</li>
<li>If you have a name that might appear at the start of other words (e.g., "Ho" appears in "House", "Honor",...), put "\\b" at the end of the term (e.g. "Ho\\b"). This searches for those characters followed by a word boundary, like a space, comma, or period. You can also put this at the beginning of the word if needed, but since the terms are case-sensitive, that probably won't be necessary (e.g., "Ho" will <i>not</i> match "ghost").</li></ul>
These special search options work because the search function actually searches for each term as a regular expression - a pattern of characters described with special notation. I think the brackets and word boundary will be the only regular expression features needed, but if you'd like to learn more about them or craft more complex search terms, https://www.regular-expressions.info/ has an excellent tutorial and reference material. 

<h4>Weird Stuff</h4>
<p>The opinion text provided by the CourtListener API is just one long string containing everything printed on the page - the main text, footnotes, headers, and footers - with no divisions between them. So if you get a result that's in a footnote, or near the end or beginning of a page, the snippet shown in the results will look a little weird. It might include something like "Cite as: 592 U. S. ____ (2020) 3 SOTOMAYOR, J., dissenting" in the middle of a sentence. That's because it just displays the matched term plus the 150 characters on either side - which might include the page header or part of the footnote on the preceding page.</p>

<p>Right now, this tool will only return 20 opinions at a time. This is because it just looks at the first "page" of results from the CourtListener API. It could be expanded to look at all the results in a given date range, but then if someone accidentally entered a very large date range, it would be incredibly slow and may max out our query limit with CourtListener. Since it's incredibly unlikely that there will be more than 20 results in the date ranges we're concerned with, I suggest leaving this as is, but if you do get 20 results, search CourtListener itself to see if there are actually more than 20, and search for portions of the date range in this app to get them all.</p>

<p>Sometimes the Court issues corrections to opinions. These will show up as a new opinion in the search results, so if you see two or more opinions for the same case with different filing dates, that's probably why. The link to the PDF of the original version of a corrected case will probably no longer work, and the PDF of the corrected version will have a cover sheet and indicate the revisions made.</p>

