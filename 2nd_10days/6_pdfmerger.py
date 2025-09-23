import os
from PyPDF2 import PdfMerger
import colors as c
#intro part

msg = ["Welcome to letApdf a pdf task performer",
	"Here you can perform multiple operation with pdf",
	"[1] Pdf Merger\n[2] Pdf Spliter\n[3] Pdf cropping\n[4] Extract text from pdf."
	]
for i in msg:
  c.color(i)


#_____________ main part _____________

def merge_pdf():
  merger = PdfMerger()
  c.color(f"Pdf merger use cases:\n1. enter files name like this --  '<file1.pdf> file2.pdf>' to merge them together.\n\n2.you can merge any number of pdf together in one line like -- ' <1.pdf> <2.pdf> .... <n.pdf>'")
  file = input("Enter files name: ").lower()
  for i in file.split(" "):
    try:
      if i[-4:] == ".pdf":
        with open(i, "r") as f:
          merger.append(f)
      else:
        c.color(f"Enter a valid filename with extensions '.pdf'\n", 0)
    except Exception:
      c.color(f"error(1): file {i} does not exists.\n", 0)

  merger.close()


merge_pdf()

def split_pdf():
  pass

def crop():
  pass

def extract():
  pass


def app():
  pass



