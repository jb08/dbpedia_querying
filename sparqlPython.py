import Tkinter as tk
import tkMessageBox
import tkFont
from SPARQLWrapper import SPARQLWrapper, JSON

prop = {"author": "dbp:author", "genre": "dbp:genre", "country": "dbp:country", "title":"dbp:name", "pages":"dbp:pages", "publisher":"dbp:publisher", "subjects":"dct:subject", "similar":"rdfs:seeAlso"}

class App(tk.Frame):
	def __init__(self, master = None):
		tk.Frame.__init__(self, master)
		self.grid(sticky=tk.N+tk.S+tk.E+tk.W)
		self.labelFont = tkFont.Font(family='Times', size='16')
		self.buttonFont = tkFont.Font(family='Times', size='18', weight='bold')
		self.createWidget()

	def createWidget(self):

		top = self.winfo_toplevel()
		top.geometry('300x400')
		top.rowconfigure(0,weight=1)
		top.columnconfigure(0,weight=1)
		self.columnconfigure(0,weight=1)

		top.rowconfigure(1,weight=3)
		top.columnconfigure(1,weight=3)
		self.columnconfigure(1,weight=3)

		self.label1 = tk.Label(self, text="Title*", font=self.labelFont, anchor=tk.W)
		self.label1.grid(column=0, row=0)
		self.input1 = tk.Entry(self)
		self.input1.grid(column=1,row=0, sticky=tk.E+tk.W)
		
		self.b1 = tk.Button(self, text="Find Author", font=self.buttonFont, command= author_query)
		self.b2 = tk.Button(self, text="Find Genre", font=self.buttonFont, command= genre_query)
		
		self.b1.grid(column=0, row=3, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)
		self.b2.grid(column=0, row=4, columnspan=2, sticky=tk.N+tk.S+tk.E+tk.W)

	def displayWidget(self, result, query_type):
		#var = tk.StringVar()
		#var.set(result)
		
		self.authorLabel = tk.Label(self, text=query_type, font=self.labelFont, anchor=tk.W)
		self.authorLabel.grid(column=0, row=1)

		#self.disp = tk.Message(self, textvariable=var, anchor = tk.W)
		self.disp = tk.Label(self, text=result, anchor = tk.W)
		self.disp.grid(column=1, row=1, sticky=tk.N+tk.S+tk.E+tk.W)

		#tkMessageBox.showinfo("Query Results:", result)

def cleanInput():
	"""
	"""

def cleanResults(res):
	"""
	"""
	#get rid of namespace
	return res[res.rfind("/")+1:]

def buildQuery(subject, predicate, object):
	"""
	"""


def author_query():
	"""
	"""
	title = app.input1.get()

	query = "SELECT ?book ?author WHERE {?book dbp:name \""+ title+ "\"@en . ?book dbp:author ?author. }"
	print "Query: " + query
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	print results

	author = "[book not found]"
	
	res = ""
	for result in results["results"]["bindings"]:
	    res += (result["book"]["value"]) + "\n"
	    print "Book Title: " + result["book"]["value"]
	    author = result["author"]["value"]
	    print "Book's Author: " + result["author"]["value"]

	    print


	author_full = author
	author = cleanResults(author)
	#author.split("/")[-1] another way
	
	
	# query = "SELECT ?author ?town WHERE {?author owl:sameAs \""+ author_full+ "\"@en . ?author dbp:birthPlace ?town. }"

	# print "Query: " + query
	# sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	# sparql.setQuery(query)
	# sparql.setReturnFormat(JSON)
	# results = sparql.query().convert()
	# print results

	#author = "[book not found]"
	
	#res = ""


	display = author
	app.displayWidget(display, "Author");
	#tkMessageBox.showinfo("Query Results", res)





def genre_query():
	"""
	"""
	title = app.input1.get()

	query = "SELECT ?book ?genre WHERE {?book dbp:name \""+ title+ "\"@en . ?book dbp:genre ?genre. }"
	print "Query: " + query
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	print results

	genre = "[book not found]"
	
	res = ""
	for result in results["results"]["bindings"]:
	    res += (result["book"]["value"]) + "\n"
	    #print "Book Title: " + result["book"]["value"]
	    genre = result["genre"]["value"]

	genre = cleanResults(genre)
	#print author
	#author.split("/")[-1] another way
	
	display = genre
	app.displayWidget(display, "Genre");
	#tkMessageBox.showinfo("Query Results", res)


#main --->
author = ""
app = App()
app.master.title('Query DBpedia')
app.mainloop()
print author_result