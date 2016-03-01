import Tkinter as tk
import tkMessageBox
from SPARQLWrapper import SPARQLWrapper, JSON

def query():
	"""
	"""
	title = input1.get()

	print title

	query = "SELECT ?book ?author WHERE {?book dbp:name \""+ title+ "\"@en . ?book dbp:author ?author }"
	print "Query: " + query
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery(query)
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	print results
	res = ""
	for result in results["results"]["bindings"]:
	    res += (result["book"]["value"]) + "\n"
	    print "Book Title: " + result["book"]["value"]
	    author = result["author"]["value"]
	    print "Book's Author: " + result["author"]["value"]

	    print

	author = author[author.rfind("/")+1:]
	#author.split("/")[-1] another way
	var.set(author)

	tkMessageBox.showinfo("Query Results", res)

author = ""
top = tk.Tk()
textFrame = tk.Frame(top)
textFrame.pack(fill="x")
label1 = tk.Label(textFrame, text="Title")
label1.pack(side="left")
input1 = tk.Entry(textFrame)
input1.pack(side="right",fill="x")
buttonFrame = tk.Frame(top)
buttonFrame.pack(side="bottom")
b1 = tk.Button(buttonFrame, text="Query", command= query)
b1.pack(side="bottom", fill="x")

bottomBottomFrame = tk.Frame(top)
bottomBottomFrame.pack(side="bottom")
var = tk.StringVar()
var.set(author)
ms = tk.Message(bottomBottomFrame, textvariable=var)
ms.pack(side="bottom")

top.mainloop()

