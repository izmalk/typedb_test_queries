import pyan3
from IPython.display import HTML
HTML(pyan3.create_callgraph(filenames="**/*.py", format="html"))