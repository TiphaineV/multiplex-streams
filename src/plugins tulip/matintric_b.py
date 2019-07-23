# Powered by Python 3.7

# To cancel the modifications performed by the script
# on the current graph, click on the undo button.

# Some useful keyboards shortcuts : 
#   * Ctrl + D : comment selected lines.
#   * Ctrl + Shift + D  : uncomment selected lines.
#   * Ctrl + I : indent selected lines.
#   * Ctrl + Shift + I  : unindent selected lines.
#   * Ctrl + Return  : run script.
#   * Ctrl + F  : find selected text.
#   * Ctrl + R  : replace selected text.
#   * Ctrl + Space  : show auto-completion dialog.

from tulip import tlp

# The updateVisualization(centerViews = True) function can be called
# during script execution to update the opened views

# The pauseScript() function can be called to pause the script execution.
# To resume the script execution, you will have to click on the "Run script " button.

# The runGraphScript(scriptFile, graph) function can be called to launch
# another edited script on a tlp.Graph object.
# The scriptFile parameter defines the script name to call (in the form [a-zA-Z0-9_]+.py)

# The main(graph) function must be defined 
# to run the script on the current graph

def main(graph): 
  betweenness = graph.getDoubleProperty("betweenness")
  condprob = graph.getDoubleProperty("condprob")
  dist = graph.getDoubleProperty("dist")
  viewBorderColor = graph.getColorProperty("viewBorderColor")
  viewBorderWidth = graph.getDoubleProperty("viewBorderWidth")
  viewColor = graph.getColorProperty("viewColor")
  viewFont = graph.getStringProperty("viewFont")
  viewFontSize = graph.getIntegerProperty("viewFontSize")
  viewIcon = graph.getStringProperty("viewIcon")
  viewLabel = graph.getStringProperty("viewLabel")
  viewLabelBorderColor = graph.getColorProperty("viewLabelBorderColor")
  viewLabelBorderWidth = graph.getDoubleProperty("viewLabelBorderWidth")
  viewLabelColor = graph.getColorProperty("viewLabelColor")
  viewLabelPosition = graph.getIntegerProperty("viewLabelPosition")
  viewLayout = graph.getLayoutProperty("viewLayout")
  viewMetric = graph.getDoubleProperty("viewMetric")
  viewRotation = graph.getDoubleProperty("viewRotation")
  viewSelection = graph.getBooleanProperty("viewSelection")
  viewShape = graph.getIntegerProperty("viewShape")
  viewSize = graph.getSizeProperty("viewSize")
  viewSrcAnchorShape = graph.getIntegerProperty("viewSrcAnchorShape")
  viewSrcAnchorSize = graph.getSizeProperty("viewSrcAnchorSize")
  viewTexture = graph.getStringProperty("viewTexture")
  viewTgtAnchorShape = graph.getIntegerProperty("viewTgtAnchorShape")
  viewTgtAnchorSize = graph.getSizeProperty("viewTgtAnchorSize")
  weighted_betweenness = graph.getDoubleProperty("weighted_betweenness")

  for n in graph.getNodes():
    print(n)
  
  vectP=[0.27749673, 0.25194718, 0.16685788, 0.20150753, 0.24252859,0.33725188, 0.21135147, 0.02341837, 0.14913524, 0.26583884,0.25858937, 0.17197693, 0.24551491, 0.32037526, 0.15400122,0.26682843, 0.3551151 ]
  vectPT=[0.20795291, 0.27373133, 0.08285877, 0.10976848, 0.30729312,0.19487826, 0.16601739, 0.02163729, 0.01391393, 0.16801402,0.14241953, 0.08436564, 0.5157522 , 0.35000431, 0.31933842, 0.13651766, 0.37085694]
  intric=graph.getDoubleProperty("intrication")
  intricT=graph.getDoubleProperty("intricationT")
  ni=0
  for i in graph.getNodes():
    intric[i]=vectP[ni]
    intricT[i]=vectPT[ni]
    ni=ni+1
