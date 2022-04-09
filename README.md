# scotus-search

This Flask app searches Supreme Court opinions within a selected date range for a preset list of search terms. It was originally created to find citations to Stanford Law School faculty and journals, but you can edit the list of terms in **search_app.py** to adapt it to your own needs. 

### The important files:

**searchopinions.py** contains the function for searching opinions. It connects to the CourtListener API, finds all opinions (including opinions on orders) in the given date range, searches for any instances of the terms in the list of search terms, and returns any opinions found along with the locations of any matches. You will need to get your own CourtListener account and enter your API key on line 9 here.

**search_app.py** is the app itself. It contains the list of search terms, calls the function in searchopinions.py (providing as parameters the list of search terms and the dates seleted by the user) and outputs the results to the home.html template.

**home.html** (in templates folder) is the html file on which all this displays. It is a Flask template; the stuff in curly brackets {{}} allows the app to dynamically generate html as the user searches, so that it displays the search form before the user searches, then displays the search results after on the same page. 

### Everything else:
**Procfile** and **requirements.txt** are required to deploy the app on Heroku, which was its original home. They provide information that it needs for the initial setup. You should not edit these. 

The **static** folder contains CSS, which is just [Skeleton boilerplate](http://getskeleton.com/) plus a little custom CSS to make the search results collapsible.

### Maintaining the app:

The only part of this that needs to be updated on an ongoing basis is the list of search terms in **search-app.py**. The terms are case-sensitive and must be enclosed in quotation marks and separated with commas. Two special notes:
* If you'd like to search for a name with and without a diacritic, or both capitalized and uncapitalized, you can enclose the possible characters in brackets: e.g. "Cu[eé]llar" will return both "Cuellar" and "Cuéllar", and "[Bb]rief" will return both "Brief" and "brief".
* If you have a name that might appear at the start of other words (e.g., "Ho" appears in "House", "Honor",...), put "\\\b" at the end of the term (e.g. "Ho\\\b"). This searches for those characters followed by a word boundary, like a space, comma, or period. You can also put this at the beginning of the word if needed, but since the terms are case-sensitive, that probably won't be necessary (e.g., "Ho" will <i>not</i> match "ghost").

These search options work because the search function reads each term as a regular expression - a pattern of characters described with special notation. The brackets and word boundary should be the only regular expression features needed, but if you'd like to learn more about them or craft more complex search terms, https://www.regular-expressions.info/ has an excellent tutorial and reference material. 

### Weird Stuff
The opinion text provided by the CourtListener API is just one long string containing everything printed on the page - the main text, footnotes, headers, and footers - with no divisions between them. So if you get a result that's in a footnote, or near the end or beginning of a page, the snippet shown in the results will look a little weird. It might include something like "Cite as: 592 U. S. \____ (2020) 3 SOTOMAYOR, J., dissenting" in the middle of a sentence. That's because it just displays the matched term plus the 150 characters on either side - which might include the page header or part of the footnote on the preceding page. If you'd like a larger snippet to be shown, edit line 93 in **home.html** accordingly; e.g., changing it to read `...[match[0]-200:match[1]+200]...` will make it show the 200 characters on either side of the term. 

Right now, this tool will only return 20 opinions at a time. This is because it just looks at the first "page" of results from the CourtListener API. It could be expanded to look at all the results in a given date range, but then if someone accidentally entered a very large date range, it would be incredibly slow and may max out our query limit with CourtListener. Since it's incredibly unlikely that there will be more than 20 results in the date ranges we're concerned with, I suggest leaving this as is, but if you do get 20 results, search CourtListener itself to see if there are actually more than 20, and search for portions of the date range in this app to get them all.

Sometimes the Court issues corrections to opinions. These will show up as a new opinion in the search results, so if you see two or more opinions for the same case with different filing dates, that's probably why. The link to the PDF of the original version of a corrected case will probably no longer work, and the PDF of the corrected version will have a cover sheet and indicate the revisions made.

