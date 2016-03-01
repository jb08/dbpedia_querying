import Tkinter as tk
import tkMessageBox
from SPARQLWrapper import SPARQLWrapper, JSON

def query():
	"""
	"""
	title = input1.get()
	print title
	sparql = SPARQLWrapper("http://dbpedia.org/sparql")
	sparql.setQuery("""
	    SELECT ?book
	    WHERE {?book dbp:pages 1216}
	""")
	sparql.setReturnFormat(JSON)
	results = sparql.query().convert()
	#print results
	res = ""
	for result in results["results"]["bindings"]:
	    res += (result["book"]["value"]) + "\n"

	tkMessageBox.showinfo("Query Results", res)


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
top.mainloop()

