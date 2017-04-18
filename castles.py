import random
from random import randint

from BaseHTTPServer import BaseHTTPRequestHandler, HTTPServer

import getopt, sys

class Land:

	# function makes it easier to use 2D coordinates to access 1D array
	def to1DIndex(self, i, j):
		if i < 0 or j < 0:
			raise IndexError

		if i >= self.rows or j >= self.columns:
			raise IndexError

		return i * self.rows + j

	def get(self, i, j):
		return self.data[self.to1DIndex(i, j)]

	def isFirstCoordinate(self, l, i, j):
		if len(l) == 0:
			return False
		x, y = l[0]
		if x == i and y == j:
			l.pop(0)
			return True
		return False

	def prettyPrintLand(self, peaks = False, valleys = False):
		ss = ''
		for i in xrange(self.rows):
			for j in xrange(self.columns):
				fill = '%02d' % land.get(i, j)
				if peaks != False and valleys != False:
					if self.isFirstCoordinate(peaks, i, j):
						fill = 'PP'
					if self.isFirstCoordinate(valleys, i, j):
						fill = 'VV'
				ss = ss + fill
				if j != self.columns - 1:
					ss = ss + (',')
			if i != self.rows - 1:
				ss = ss + '\n'

		return ss

	def prettyPrintCastles(self, peaks, valleys):
		return self.prettyPrintLand(peaks, valleys)

	def generateLand(self):
		self.data = []
		print 'Initiating land with ' + str(self.rows) + ' rows and ' + str(self.columns) +' columns...' 

		for i in xrange(self.rows):
			for j in xrange(self.columns):
				self.data.append(randint(1, self.max_height))

	def isLocalMinOrMaxWithinRow(self, land, i, j, comp):
		# row above
		if i > 0:
			if not comp(land.get(i, j), land.get(i - 1, j)):
				return False
			if j > 0:
				if not comp(land.get(i, j), land.get(i - 1, j - 1)):
					return False

			if j < land.columns - 1:
				if not comp(land.get(i, j), land.get(i - 1, j + 1)):
					return False

		# row element is in
		if j > 0:
			if not comp(land.get(i, j), land.get(i, j - 1)):
				return False

		if j < land.columns - 1:
			if not comp(land.get(i, j), land.get(i, j + 1)):
				return False

		# row below
		if i < land.rows - 1:
			if not comp(land.get(i, j), land.get(i + 1, j)):
				return False
			if j > 0:
				if not comp(land.get(i, j), land.get(i + 1, j - 1)):
					return False

			if j < land.columns - 1:
				if not comp(land.get(i, j), land.get(i + 1, j + 1)):
					return False

		return True


	def __init__(self, rows, columns, max_height = 99):
		self.rows = rows
		self.columns = columns
		self.max_height = max_height

	def isLocalMinWithinRow(self, land, i, j):
		comp = lambda x, y: x < y
		return self.isLocalMinOrMaxWithinRow(land, i, j, comp)

	def isLocalMaxWithinRow(self, land, i, j):
		comp = lambda x, y: x > y
		return self.isLocalMinOrMaxWithinRow(land, i, j, comp)

	def findPeaksAndValleys(self, land):
		peaks = []
		valleys = []

		rows = land.rows
		columns = land.columns

		for i in xrange(rows):
			for j in xrange(columns):
				if self.isLocalMaxWithinRow(land, i, j):
					peaks.append((i, j))
				if self.isLocalMinWithinRow(land, i, j):
					valleys.append((i, j))

		return (peaks, valleys)


class S(BaseHTTPRequestHandler):
	def _set_headers(self):
		self.send_response(200)
		self.send_header('Content-type', 'text/html')
		self.end_headers()

	def do_GET(self):
		self._set_headers()

		if self.path == "/":
			self.path = "/index.html"

		if self.path == "/land":
			land.generateLand()
			landStr = land.prettyPrintLand()
			
			self.wfile.write(landStr)

		elif self.path == "/castles":
			peaks, valleys = land.findPeaksAndValleys(land)
			castlesStr = land.prettyPrintCastles(peaks, valleys)

			self.wfile.write(castlesStr)

		elif self.path == "/index.html":
			html = open('index.html', 'r')
			for line in html:
				self.wfile.write(line)

		
def run(server_class=HTTPServer, handler_class=S, port=3000):
	server_address = ('', port)
	httpd = server_class(server_address, handler_class)
	print 'Starting httpd on port ' + str(port) + '...'
	httpd.serve_forever()

def main(argv):
	rows = False
	columns = False
	port = False

	try:	
		opts, args = getopt.getopt(argv,"p:r:c:",["port=","rows=","columns="])
	except getopt.GetoptError:
		print 'test.py -p <port> -r <rows> -c <columns>'
		sys.exit(2)
	for opt, arg in opts:
		if opt in ("-p", "--port"):
			port = arg
		elif opt in ("-r", "--rows"):
			rows = arg
		elif opt in ("-c", "--columns"):
			columns = arg

	if not rows:
		rows = 10
	if not columns:
		columns = 10

	global land
	land = Land(rows, columns)

	if port:
		run(port=port)
	else:
		run()

if __name__ == "__main__":
	main(sys.argv[1:])
