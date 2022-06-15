"""
Bypass Google Captcha Active Scanning
"""

title = "Bypass Google Captcha (Costum Script)"
descriptions = "Bypass google captch with remove g-recaptcha-response parameter on the request"
risk = 2 # risk: 0: info, 1: low, 2: medium, 3: high
confidence = 1 # confidence: 0: false positive, 1: low, 2: medium, 3: high
solution = "Ignore requests if do not contain the g-recaptcha-response parameter"
otherInfo = "Control Failure"
cweID = 804
wascID = 0

"""
The scanNode function will typically be called once for every page
The scan function will typically be called for every parameter in every URL and Form for every page

Note that new active scripts will initially be disabled
Right click the script in the Scripts three and select "enable"

# Alert function

raiseAlert(risk, int confidence, String name, String description, String uri, 
	String param, String attack, String otherInfo, String solution, String evidence, 
	int cweId, int wascId, HttpMessage msg)

if (True):
	sas.raiseAlert(1, 1, alertTitle, alertDescriptions, msg.getRequestHeader().getURI().toString(), 
	      param, 'Your attack', alertOtherInfo, alertSolution, '', cweID, wascID, msg);

"""

# Demo response
response = "may mean the user just didn't complete the reCAPTCHA"

# Smartchecking invalid response
#response = "Mohon validasi recaptcha terlebih dahulu"


def scanNode(sas, msg):
  origMsg = msg
  # Debugging can be done using print like this
  print ("Bypass Google Captcha Testing");
  # Copy requests before reusing them
  msg = origMsg.cloneRequest()
  if response in msg.getResponseBody().toString():
  	pass
  else:
     reqMethod = msg.getRequestHeader().getMethod()
     if reqMethod == "POST":
        editedReq = msg.getRequestBody().toString() + "&g-recaptcha-response="
        msg.setRequestBody(editedReq)
        sas.sendAndReceive(msg, True, True)
        if response in msg.getResponseBody().toString(): 
           lastScan(True, msg, sas)
        else:
           lastScan(False, msg, sas)

def lastScan(googleCaptcha, msg, sas):
  if googleCaptcha == False:
     pass
  elif googleCaptcha == True:
     newReq = msg.getRequestBody().toString().replace("&g-recaptcha-response=", "")
     msg.setRequestBody(newReq)
     sas.sendAndReceive(msg, True, False)
     if response in msg.getResponseBody().toString():
        pass
     else:
        code = msg.getResponseHeader().getStatusCode()
        if code == 200:
           sas.raiseAlert(risk, confidence, title, descriptions, msg.getRequestHeader().getURI().toString(), '', '', otherInfo, solution, '', cweID, wascID, msg);

def scan(sas, msg, param, value):
  pass
	