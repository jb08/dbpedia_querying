import Tkinter as tk
import tkMessageBox
import tkFont
import urllib
from titlecase import titlecase
from SPARQLWrapper import SPARQLWrapper, JSON

prop = {"author": "dbp:author", "genre": "dbp:genre", "country": "dbp:country", "title":"dbp:name", "pages":"dbp:pages", "publisher":"dbp:publisher", "subjects":"dct:subject", "similar":"rdfs:seeAlso"}

class App(tk.Frame):
	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
		self.labelFont = tkFont.Font(family='Times', size='14')
		self.buttonFont = tkFont.Font(family='Times', size='16', weight='bold')
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
		self.label1.grid(column=0, row=0)
		self.input1 = tk.Entry(self)
		self.input1.grid(column=1,row=0, sticky=tk.E+tk.W)
		
		self.b1 = tk.Button(self, text="Find Author", font=self.buttonFont, command=author_query)
		self.b2 = tk.Button(self, text="Find Genre", font=self.buttonFont, command=genre_query)
		
		self.b1.grid(column=0, row=self.numQueries+1, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		self.b2.grid(column=0, row=self.numQueries+2, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

	def displayWidget(self, results, query_type):
		#var = tk.StringVar()
		#var.set(result)
		howMany = len(results)

		self.authorLabel = tk.Label(self, text=query_type, font=self.labelFont, anchor=tk.W)
		self.authorLabel.grid(column=0, row=1)
		r = 0
		for i in range(howMany):
			#self.disp = tk.Message(self, textvariable=var, anchor = tk.W)
			self.disp = tk.Label(self, text=results[i], anchor = tk.W)
			self.disp.grid(column=1, row=i+1, sticky=tk.N+tk.S+tk.E+tk.W)
			i+=1
			r = i

		#remove any higher
		for label in self.winfo_children():
			text =  str(label["text"])
			if text == "Birth Place": #hacky, but this was staying on screen 
				label.destroy()

		for label in self.grid_slaves():
			row =  int(label.grid_info()["row"])
			if row > r and row < self.numQueries: #hacky, but this was staying on screen 
				label.grid_forget()


	def displayResults(self, res):
		"""
		Generalized to display all query results.
		"""
		queries = res["queries"]
		bindings = res["results"]
		row = 1
		howMany = len(queries)

		for i in range(howMany):
			self.authorLabel = tk.Label(self, text=queries[i], font=self.labelFont, anchor=tk.N+tk.W)
			self.authorLabel.grid(column=0, row=row)

			#self.disp = tk.Message(self, textvariable=var, anchor = tk.W)
			self.disp = tk.Label(self, text=bindings[i], anchor = tk.W)
			self.disp.grid(column=1, row=row, sticky=tk.N+tk.S+tk.E+tk.W)
			row+=1

		#remove any higher
		for label in self.grid_slaves():
			currRow = int(label.grid_info()["row"])
			if currRow >= row and currRow < self.numQueries:
				label.grid_forget()


		#tkMessageBox.showinfo("Query Results:", result)

def cleanInput(userInput):
	"""
	Fix user input.
	"""
	return titlecase(userInput.lower())

def cleanResults(res):
	"""
	Cleans the query variable results by removing the URI and underscores.
	"""
	if (res == []):
		return "[Nothing Found]"
	final = []
	#get rid of namespace
	for item in res:
		noNS = item[item.rfind("/")+1:]
		final += [" ".join(noNS.split("_"))] #split on underscore and join with space in between

	#print final
	return final[-1]

def cleanResultsAll(res):
	"""
	Cleans the query variable results by removing the URI and underscores.
	"""
	if (res == []):
		return ["[Nothing Found]"]
	final = []
	#get rid of namespace
	for item in res:
		noNS = item[item.rfind("/")+1:]
		final += [" ".join(noNS.split("_"))] #split on underscore and join with space in between

	#print final
	return list(set(final))

def author_query():
	"""
	"""
	d = {}
	d["results"] = []
	d["queries"] = []

	title = cleanInput(app.input1.get())

	query = "SELECT ?book ?author WHERE {?book dbp:name \""+ title+ "\"@en . ?book dbp:author ?author. }"
	#print "Query: " + query
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	#print results
	author = "[book not found]"
	bookResults = []
	authorResults = []

	res = ""
	for result in results["results"]["bindings"]:
	    #res += (result["book"]["value"]) + "\n"
	    bookResults.append(result["book"]["value"])
	    #print "Book Title: " + result["book"]["value"]
	    authorResults.append(result["author"]["value"])
	    #print "Book's Author: " + result["author"]["value"]
	    print

	print cleanResultsAll(bookResults)
	print cleanResultsAll(authorResults)
	#author_full = authorResults[-1]
	author = cleanResults(authorResults)
	#author.split("/")[-1] another way
	d["queries"] += ["Author"]
	d["results"] += [author]
	
	birthResults = []
	query = "SELECT ?author ?town WHERE {?author dbp:name \""+ author+ "\"@en . ?author dbp:birthPlace ?town. }"

	#print "Query: " + query
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	#print results

	for result in results["results"]["bindings"]:
	    birthResults.append(result["town"]["value"])
	    print

	birthPlace = "[No Hometown]"
	birthPlace = cleanResults(birthResults)

	#author = "[book not found]"
	d["queries"] += ["Birth Place"]
	d["results"] += [birthPlace]

	#res = ""
	app.displayResults(d);
	#tkMessageBox.showinfo("Query Results", res)


def genre_query():
	"""
	"""
	title = app.input1.get()
	title = cleanInput(title)
	query = "SELECT ?book ?genre WHERE {?book dbp:name \""+ title+ "\"@en . ?book dbp:genre ?genre. ?book dbp:publisher ?pub}"
	#print "Query: " + query
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	#print results

	genre = "[book not found]"
	genres = []
	res = ""
	for result in results["results"]["bindings"]:
	    res += (result["book"]["value"]) + "\n"
	    #print "Book Title: " + result["book"]["value"]
	    genres += [result["genre"]["value"]]

	genre = cleanResults(genres)

	genres = cleanResultsAll(genres)
	#print author
	#author.split("/")[-1] another way
	print ("Genres", genres)
	display = genre
	app.displayWidget(genres, "Genres");
	#tkMessageBox.showinfo("Query Results", genres)


#main --->
author = ""
app = App()
app.master.title('Query DBpedia')
app.mainloop()
#print author_result