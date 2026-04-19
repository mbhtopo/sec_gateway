Hello world!

This is my contribution to a safer interaction with QR-Codes while maintaining the current usability. 
We all love QR-Codes and we should make sure that our enthusiasm towards them is not overshadowed by potential risks.
You are looking at a Secure Web Gateway that is made to ensure a safe QR-Code handling by implementing the following security measures, 
apart from it's inherently secure architecture: 

- URL validation and sanitization
- Malicious IP detection via CrowdSec
- Redirection chain control and protection
- Sandbox analyzation
- Request logging for security audits

## Installation

TODO test instruction
git clone https://github.com/mbhtopo/sec_gateway.git  
cd sec_gateway  
python -m venv venv  
venv\Scripts\activate   # Windows  
pip install -r requirements.txt  

Start the Gateway in the main.py file. Look at all functions used in the gateway.py file   
via src>app>gateway.py  
Look at the logic behind all functions in their modules in the folder security  
via src>app>security  
Note that the Sandbox is seperately inside the sandbox folder  

## Reading docs
read the documentation to understand and see all functions  
via docs and a double click on the index.html  
Now an HTML site should open  for you to see the docs  

Check endpoint documentation (project must be running):
http://localhost:5000/apidocs

For productive environment:
- Let API-Key rotate  
- Activate HTTPS-only
- Manage `debug=True` with environment variable
- Add Rate Limits
- Clean Code from unnecessary comments/ commented functions

Please contact me if you have any doubts on how to use the Gateway, if you discover bugs or want to give feedback.  
Have fun and always be safe !  
@mbhtopo
