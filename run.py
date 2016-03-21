#!flask/bin/python
from app import app
# app.run(host="0.0.0.0", port=80)
if __name__ == "__main__":
	# app.run(debug=True)
	app.debug = True
	app.run(host="0.0.0.0", port=2000)
# 	app.run()