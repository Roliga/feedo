Plugin Spec
==

Functions
--

* info()
	- Returns: A dictionary of information about the plugin
* priority()
	- Returns: Plugins priority, used when multiple plugins can be used for the same url
* check(url)
	- Takes a url and checks if this plugin can handle it
	- Arguments: url(string)
	- Returns: Boolean
* generate(query)
	- Generates a feed from the given query, and returns it as a utf-8 encoded string
	- Arguments: query(string)
	- Returns: Utf-8 encoded string containing the feed
