import Tkinter as tk
import tkMessageBox
import tkFont
import urllib
from titlecase import titlecase
from SPARQLWrapper import SPARQLWrapper, JSON


class QueryInfo:
	def __init__(self, title=""):
		"""
		To keep track of queries
		"""
		self.title = title
		self.author = ""
		self.authorBirthPlace = ""
		self.genres = []
		self.allResults = {}

	def setTitle(self, title):
		self.title = title

	def setAuthor(self, author):
		self.author = author

	def setBirthPlace(self, bP):
		self.birthPlace = bP

	def setGenres(self, gs):
		self.genres = gs

	def allResults(self, res):
		self.allResults = res

	def reset(self):
		self.title =""
		self.author=""
		self.authorBirthPlace=""
		self.genres=[]

	def __str__(self):
		return """
				Title: """ + self.title +"""\n
				Author: """ + self.author + """\n
				Genres: """ + str(self.genres) + """\n"""

class App(tk.Frame):
	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
		self.labelFont = tkFont.Font(family='Helvetica', size='12')
		self.buttonFont = tkFont.Font(family='Helvetica', size='14', weight='bold')
		self.numQueries = 15 #must update each time we add results
		self.createWidget()

	def createWidget(self):
		top = self.winfo_toplevel()
		top.geometry('275x400')
		top.rowconfigure(0,weight=1)
		top.columnconfigure(0,weight=1)
		self.columnconfigure(0,weight=1)

		top.rowconfigure(1,weight=3)
		top.columnconfigure(1,weight=3)
		self.columnconfigure(1,weight=3)

		self.label1 = tk.Label(self, text="Title*", font=self.labelFont, anchor=tk.N+tk.W)
		self.label1.grid(column=0, row=0, sticky=tk.N+tk.W)
		self.input1 = tk.Entry(self)
		self.input1.grid(column=1,row=0, sticky=tk.E+tk.W)
		
		self.b = tk.Button(self, text="Find Book", font=self.buttonFont, command=findBook)
		self.b.grid(column=0, row=1, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

		#self.how_to_label = tk.Label(self, text="*Once a specific book is found, then additional options will appear!", font=self.labelFont, anchor=tk.N+tk.W)
		#self.how_to_label.grid(column=0, row=3, sticky=tk.N+tk.W)

		#clear any old stuff
		self.clear(2,float("inf"))

	def displayOptions(self):
		"""
		Allow the user to see whether they want to see more about the author or genres
		"""
		self.b.grid_remove()
		self.input1.configure(state="disabled")

		self.clear(1, self.numQueries)

		self.b1 = tk.Button(self, text="Find Author", font=self.buttonFont, command=lambda: makeQuery(1))
		self.b2 = tk.Button(self, text="Find Genre", font=self.buttonFont, command=lambda: makeQuery(2))
		self.b3 = tk.Button(self, text="Read Abstract", font=self.buttonFont, command=lambda: makeQuery(3))
		self.b4 = tk.Button(self, text="Pages", font=self.buttonFont, command=lambda: makeQuery(4))
		self.b5 = tk.Button(self, text="Reset", font=self.buttonFont, command=reset)

		self.b1.grid(column=0, row=self.numQueries+1, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		self.b2.grid(column=0, row=self.numQueries+2, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		self.b3.grid(column=0, row=self.numQueries+3, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		self.b4.grid(column=0, row=self.numQueries+4, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		self.b5.grid(column=0, row=self.numQueries+5, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

	def clarifyResults(self,  res):
		"""
		Should create a pop up window with radio buttions so user can specify which book 
		they were refering to
		"""
		self.newWin = tk.Toplevel(self)
		self.newWin.grid()
		title = tk.Label(self.newWin, text="Multiple results for your search. Please select one.")
		title.grid(row = 0)
		#Radio Buttons
		self.v = tk.StringVar()
		disp = "Title:"+res[1][0] + ":Author:"+res[1][1]
		self.v.set(disp) #set the default to be the first entry
		for key in res:
			(title, author) = res[key]
			val = "Title:"+title + ":Author:"+ author
			display = title + ", " +author
			b = tk.Radiobutton(self.newWin, text=display, variable=self.v, value=val)
			b.grid(row=key, sticky =tk.W)

		submit = tk.Button(self.newWin, text="Submit", command=submitSelect)
		submit.grid(row=key+1)
		self.displayOptions()

	def displayResults(self, res):
		"""
		Generalized to display all query results.
		"""
		queries = res["queries"]
		bindings = res["results"]
		isGenre = False;

		row = 1
		howMany = len(queries)

		#clear
		self.clear(row, self.numQueries)

		for i in range(howMany):
			if (not isinstance(bindings[i], list)):
				self.label1 = tk.Label(self, text=queries[i], font=self.labelFont)
				self.label1.grid(column=0, row=row, sticky=tk.N+tk.W)

				self.disp1 = tk.Label(self, text=bindings[i], anchor = tk.W)
				self.disp1.grid(column=1, row=row, sticky=tk.N+tk.S+tk.E+tk.W)
				row+=1
			else:
				if queries[i] == "Genre":
					isGenre = True;
				self.label1 = tk.Label(self, text=queries[i], font=self.labelFont)
				self.label1.grid(column=0, row=row, sticky=tk.N+tk.W)
				for b in bindings[i]:
					self.disp1 = tk.Label(self, text=b, anchor = tk.W)
					self.disp1.grid(column=1, row=row, sticky=tk.N+tk.S+tk.E+tk.W)
					row+=1

		if isGenre:
			for label in self.winfo_children():
					text =  str(label["text"])
					if text == "Birth Place": #hacky, but this was staying on screen 
						label.destroy()

	def clear(self, start, end):
		"""
		Clears widgets on rows froms start up to end
		"""
		for widget in self.grid_slaves():
			if (int(widget.grid_info()["row"]) >= start and int(widget.grid_info()["row"]) < end ):
				widget.grid_remove()

	def userMessage(self, title, message):
		"""
		Pop to give the user some information.
		"""
		tkMessageBox.showinfo(title, message)

def reset():
	"""
	Takes users back to the homepage to look for another book.
	"""
	app.b2.grid_remove()
	app.b1.grid_remove()
	app.b3.grid_remove()
	app.clear(2,float("inf"))
	qInfo.reset()
	app.createWidget()

def submitSelect():
	"""
	Called when user selects a book and clicks on Submit. 
	Sets the author and title in qInfo (which is keeping track of query result)
	"""
	app.newWin.destroy()
	selectedBook= app.v.get()
	author = selectedBook.split(':')[-1]
	title = selectedBook.split(':')[1]

	qInfo.setAuthor(author)
	qInfo.setTitle(title)

def cleanInput(userInput):
	"""
	Fix user input.
	output: a string
	"""
	return titlecase(userInput.lower())

def cleanResult(res):
	"""
	input: a string
	Cleans the query variable results by removing the URI and underscores.
	returns: a string
	"""
	if (res == ""):
		return "[Nothing Found]"
	#get rid of namespace
	noNS = res[res.rfind("/")+1:]
	final = " ".join(noNS.split("_")) #split on underscore and join with space in between
	return final

def findBook():
	"""Does DBpedia have the book the user is looking for?
	"""
	title = cleanInput(app.input1.get()) # get and clean user input
	print "User title input: " + title
	query = """
		SELECT ?book ?author
		WHERE {?book dbp:name \"""" + title + """\" @en. 
			   ?book dbp:author ?author.
			   }
		"""
	results = sendQuery(query)

	print results
	print
	cleanResults = extractResults(results, "author")
	qInfo.allResults = cleanResults

	print cleanResults
	if len(cleanResults) == 1: # Just one book found
		print "Successful"
		qInfo.setTitle(cleanResults[1][0]) #might as well save title and author
		qInfo.setAuthor(cleanResults[1][1])
		app.displayOptions()

	elif len(cleanResults) > 1: #Multiple books found
		app.clarifyResults(cleanResults)
	else:
		#app.userMessage("Sorry, no books found. Please try another search.")
		queryRDFSLabel(title)

def queryRDFSLabel(title):
	"""
	If nothing is found with name, look at the label
	"""
	query = """
		SELECT ?book ?author
		WHERE {?book rdfs:label \"""" + title + """\" @en. 
			   ?book dbp:author ?author. }
		"""
	results = sendQuery(query)

	cleanResults = extractResults(results, "author")
	qInfo.allResults = cleanResults

	if len(cleanResults) == 1: # Just one book found
		print "Successful"
		qInfo.setTitle(cleanResults[1][0]) #might as well save title and author
		qInfo.setAuthor(cleanResults[1][1])
		app.displayOptions()

	elif len(cleanResults) > 1: #Multiple books found
		app.clarifyResults(cleanResults)
	else:
		app.userMessage("No Book Found","Sorry, no books found with that specific title. Please try another search.")

def sendQuery(q):
	"""
	input: string query
	Uses the sparql wrapper to send query to SPARQL endpoint
	Outputs: results dictionary
	"""
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(q)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	return results

def makeQuery(option):
	"""
	New consolidated way to query
	"""
	d = {} #store query and result
	if (option == 1):
		d["queries"] = ["Author"]
		d["results"] = [qInfo.author]

		birthPlace = findAuthorBirthPlace()

		d["queries"] += ["Birth Place"]
		d["results"] += [birthPlace]
		qInfo.setBirthPlace(birthPlace)
		
		otherBooks = moreByAuthor()
		d["queries"] += ["Also by Author"]
		d["results"] += [otherBooks]

		app.displayResults(d)

	elif (option == 2):
		userChoice = "genre"
		query = """
			SELECT ?book ?genre
			WHERE {?book rdfs:label \"""" + qInfo.title + """\" @en. 
				   ?book dbp:genre ?genre. 
				   ?book dbp:author ?author}
			"""
		#print query
		results = sendQuery(query)

		cleanResults = extractResults(results, userChoice) #returns a dictionary of pairings of the title either genre or author

		listOfResults = []
		for key in cleanResults:
			listOfResults += [cleanResults[key][1]]

		if (len(listOfResults) == 0 ):
			listOfResults = ["[None Found]"]

		d["queries"] = ["Genre"]
		d["results"] = [listOfResults]

		qInfo.setGenres(listOfResults)
		app.displayResults(d);  #still need to consolidate display

	elif (option == 3):
		userChoice="abstract"
		getAbstract(userChoice);

	elif (option == 4):
		userChoice="pages"
		getNumPages(userChoice);		

def getAbstract(userChoice):
	"""
	Displays a pop up window with the abstract of the user's selected book.
	"""
	query = """
			SELECT ?book ?abstract
			WHERE {?book rdfs:label \"""" + qInfo.title + """\"@en . 
				   ?book dbo:abstract ?abstract . 
				   ?book dbp:author ?author.
				   FILTER langMatches(lang(?abstract), 'en') . 
				   }
			"""
	results = sendQuery(query)
	cleanRes = extractResults(results, userChoice)

	if len(cleanRes) == 0:
		abstract = "None Found"
	else:
		abstract = cleanRes[1][1]

	app.userMessage(qInfo.title+ " Abstract", abstract)

def getNumPages(userChoice):
	"""
	Displays a pop up window with the number of pages of the user's selected book.
	"""
	query = """
			SELECT ?book ?pages
			WHERE {?book rdfs:label \"""" + qInfo.title + """\"@en . 
				   ?book dbp:pages ?pages . 
				   ?book dbp:author ?author.
				   }
			"""
	results = sendQuery(query)
	cleanRes = extractResults(results, userChoice)

	pages_per_min = 2.0
	if len(cleanRes) == 0:
		num_pages = "None Found"
		#temp_page_num = 1296
		#num_pages = "There are " + str(temp_page_num) + " pages in " + qInfo.title + ". Based on the average adult reading speed, this may take you "+ str(int(float(temp_page_num)*pages_per_min/60)) + " hours."

	else:
		num_pages = cleanRes[1][1]
		num_pages = "There are " + str(num_pages) + " pages in " + qInfo.title + ". Based on the average adult reading speed, this may take you "+ str(int(float(num_pages)*pages_per_min/60)) + " hours to read."
		

	app.userMessage(qInfo.title+ " Pages", num_pages)
		
def findAuthorBirthPlace():
	"""
	input: string
	output: a string, the birthplace of the author
	"""
	query = """
			SELECT distinct ?author ?town 
			WHERE {?author dbp:name \""""+ qInfo.author + """\"@en . 
			?author dbp:birthPlace ?town }
			"""

	results = sendQuery(query)
	#print results
	cleanResults = extractResults(results, "town")
	places = []
	for key in cleanResults:
		places += [cleanResults[key][1]]

	#print ("places", places)
	if len(places) == 1:
		return places[0]
	elif len(places) > 1:
		place = determineIfDifferent(places)
		return place
	else:
		return "Not Found"

def moreByAuthor():
	"""
	Returns a list of other books by the same author
	"""
	query = """
			SELECT distinct ?author ?books
			WHERE {?author dbp:name \""""+ qInfo.author + """\"@en . 
			?author dbo:notableWork ?books}
			"""

	results = sendQuery(query)
	cleanRes = extractResults(results, "books")

	books = []
	for key in cleanRes:
		books += [cleanRes[key][1]]

	if len(books) == 0:
		return "None Found"
	return books

def determineIfDifferent(places):
	"""
	If multiple birth places are returned need to verify if they're the same and
	which to return. For now returning first
	"""
	return places[0]

def extractResults(res, userChoice):
	"""
	Goes through the Sparql result and extracts desired information.
	Outputs: a dictionary with format {1: (title, queryResult), 2: (title2, queryResult) etc.}
	"""
	d = {}
	d["title"] = []
	d[userChoice] = []

	pairedDict = {}
	count = 1
	bookName = ""

	for result in res["results"]["bindings"]:
		if (userChoice == "genre" or userChoice == "author"):
			bookName = cleanResult(result["book"]["value"])

		if (userChoice != "abstract"):
			answer = cleanResult(result[userChoice]["value"])
		else:
			answer = result[userChoice]["value"]
		pairedDict[count] = (bookName, answer)
		count+=1

	return pairedDict

#global variables:
app = App()
qInfo = QueryInfo()

def main():
	app.master.title('Query DBpedia')
	app.mainloop()

if __name__ == "__main__":
	main()