rundev:
	ipython main.py	&&	npm run dev	&&  chromium 'http:localhost:3000' 

compile:
	npm run generate && cp static/eel.config.js dist/