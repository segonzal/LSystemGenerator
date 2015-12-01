# TODO:
# BEGIN debe aceptar listas de APP
# Arreglar yields (genTokens) para que sea leible
# Incorporar Tortuga3D y generar primeros modelos en OpenSCAD
# Modificar RULE para agregar condiciones
# Modificar env_lookup para que considere condiciones
# Modificar RULE para agregar probabilidades
# Modificar env_lookup para que considere probabilidades
# Agregar clave #ignore
# Agregar clave #tropism <NUM> <NUM> <NUM>

import re

LFUN = "[FfG+-^&/|$\[\]{.}~!'%\\\\]"
ONEARGFUN = "[FfG+-^&/!%\\\\]"
NOARGFUN = "[|$\[\]{.}~']"

NUM = "(?:\d*\.?\d+)"
SYM = "(?:[a-zA-Z]+\d*)"
APP = "("+LFUN+"|"+SYM+") *(\([^()]*\))?"
DEFUN = "("+SYM+"|"+LFUN+") *(\([^()+\-*/^\d]*\))?"

NUMVAR = "(?:"+SYM+"|"+NUM+")"
NUMEXPR = "\s*("+NUMVAR+")|([+\-*/^])"
NUM2 = NUMVAR+"(?:[+\-*/^]"+NUMVAR+")+|"+NUMVAR

BOOL = "*|"+NUMVAR+"(<|>|<=|>=|=|!=)"+NUMVAR
BOOLVAR = BOOL+"[&|^]"+BOOL+"|!?"+BOOL

WHITESPACE = re.compile("\s*")
COMMENT = re.compile("(/\*([^*]|[\r\n]|(\*+([^*/]|[\r\n])))*\*+/)|(//.*(?=\n))")
ASSIGN = re.compile("^\s*("+SYM+") *=\s*("+NUM2+")\s*$") #Change to NUMEXPR ? (restoring to NUM)
DEFINE = re.compile("^\s*#define +("+SYM+") +("+NUM+")\s*$")
DELTA = re.compile("^\s*#delta +("+NUM+")\s*$")
ITERATION = re.compile("^\s*#iterate +("+NUM+")\s*$")

BEGIN = re.compile("^\s*begin\s*:\s*"+APP+"\s*$")
RULE = re.compile("^\s*rule\s*:\s*"+DEFUN+"\s*::=\s*(.+)\s*$") #It could be needed a multiline definition of fun

APPLICATION = re.compile(APP)
NUMERICEXPRESSION = re.compile(NUMEXPR)
NUMPAT = re.compile("("+NUM+")")
INTPAT = re.compile("^([0-9]+)$")
SYMPAT = re.compile("("+SYM+")")

OPINFO = {
	'||': (5   ,'LEFT'),
	'&&': (6   ,'LEFT'),
	'==': (10  ,'LEFT'),
	'!=': (10  ,'LEFT'),
	'<' : (11  ,'LEFT'),
	'<=': (11  ,'LEFT'),
	'>' : (11  ,'LEFT'),
	'>=': (11  ,'LEFT'),
	'+' : (13  ,'LEFT'),
	'-' : (13  ,'LEFT'),
	'*' : (14  ,'LEFT'),
	'/' : (14  ,'LEFT'),
	'^' : (14  ,'RIGHT')#If it starts to fail, try 14.5
}

def computeOp(op, lhs, rhs):
	if op   == '+' : return lambda env: lhs(env) +   rhs(env)
	elif op == '-' : return lambda env: lhs(env) -   rhs(env)
	elif op == '*' : return lambda env: lhs(env) *   rhs(env)
	elif op == '/' : return lambda env: lhs(env) /   rhs(env)
	elif op == '^' : return lambda env: lhs(env) **  rhs(env)
	elif op == '<' : return lambda env: lhs(env) <   rhs(env)
	elif op == '>' : return lambda env: lhs(env) >   rhs(env)
	elif op == '<=': return lambda env: lhs(env) <=  rhs(env)
	elif op == '>=': return lambda env: lhs(env) >=  rhs(env)
	elif op == '==': return lambda env: lhs(env) ==  rhs(env)
	elif op == '!=': return lambda env: lhs(env) !=  rhs(env)
	elif op == '&&': return lambda env: lhs(env) and rhs(env)
	elif op == '||': return lambda env: lhs(env) or  rhs(env)
	else: raise ValueError("Unknown operator '%s'." % op)

class Token:
	def __init__(self,name,value):
		self.name = name
		self.value = value

	def __str__(self):
		return "<"+self.name+" "+str(self.value)+">"

class Closure:
	def __init__(self,ids,body,env):
		self.ids = ids
		self.body = body
		self.env = env

def argsFromList(args):
	return filter(lambda x: x!='',WHITESPACE.sub('',args)[1:-1].split(','))

def throwError(err):
	raise ValueError(err)

def throwKeyFunSynErr(F,argn,i,line):
	if argn == 0:
		raise SyntaxError("rule %s shouldn't have any arguments. at line %i:\n%s" % (F,i,line))
	else:
		raise SyntaxError("rule %s must have at most one argument. at line %i:\n%s" % (F,argn,i,line))

class LParser:
	def __init__(self,text):
		self.tokgen = self.genTokens(text)
		self.curToken = None

	def genNumExprToken(self,val):
		for (num,op) in NUMERICEXPRESSION.findall(val):
			if NUMPAT.match(num):
				yield Token('NUM', num)
			elif SYMPAT.match(num):
				yield Token('SYM', num)
			else:
				yield Token('BINOP',op)

	def genArgExprToken(self,F,args,i):
		yield Token('APP',F)
		args = argsFromList(args)
		if   F in ONEARGFUN and len(args)>1: throwKeyFunSynErr(F,1,i,line)
		elif F in NOARGFUN  and len(args)>0: throwKeyFunSynErr(F,0,i,line)
		for arg in args:
			for s in self.genNumExprToken(arg): yield s

	def genTokens(self,text):
		if COMMENT.search(text):
			text = COMMENT.sub("",text)
		i = 1
		for line in text.split("\n"):
			i += 1
			if len(line)==0: continue
			if ASSIGN.match(line):
				(sym,val) = ASSIGN.findall(line)[0]
				yield Token('ASIGN',sym)
				for s in self.genNumExprToken(val): yield s
			elif DEFINE.match(line):
				(key,value) = DEFINE.findall(line)[0]
				yield Token('DEF',key)
				yield Token('NUM', value)
			elif DELTA.match(line):
				value = DELTA.findall(line)[0]
				yield Token('DELTA', None)
				yield Token('NUM', value)
			elif BEGIN.match(line):
				(F,args) = BEGIN.findall(line)[0]#TODO accept as begin a list of APPS
				yield Token('BEGIN',None)
				#for (F,args) in APPLICATION.findall(args):
				for s in self.genArgExprToken(F,args,i): yield s
			elif RULE.match(line):
				(F,args,ret) = RULE.findall(line)[0]
				yield Token('RULE',F)
				args = argsFromList(args)
				if   F in ONEARGFUN and len(args)>1: throwKeyFunSynErr(F,1,i,line)
				elif F in NOARGFUN  and len(args)>0: throwKeyFunSynErr(F,0,i,line)
				for sym in args:
					yield Token('SYM', sym)
				for (F,args) in APPLICATION.findall(ret):
					for s in self.genArgExprToken(F,args,i): yield s
			elif ITERATION.match(line):
				num = ITERATION.findall(line)[0]
				yield Token('ITER',num)
			else:
				raise SyntaxError("at line %i:\n%s" % (i,line))

	def getNextToken(self):
		try:
			self.curToken = self.tokgen.next()
		except StopIteration:
			self.curToken = None
		return self.curToken

	def computeNum(self):
		tok = self.curToken
		if tok.name == 'BINOP':
			if tok.value == '-':
				self.getNextToken()
				val = self.computeNum()
				return lambda env: -val(env)
			elif tok.value == '!':
				self.getNextToken()
				val = self.computeNum()
				return lambda env: not val(env)
			else:
				raise ValueError("Expected an expresion, not an operator '%s'" % tok.value)
		else:
			self.getNextToken()
			if tok.name == 'NUM':
				if INTPAT.match(tok.value):
					return lambda env: int(tok.value)
				else:
					return lambda env: float(tok.value)
			elif tok.name == 'SYM':
				return lambda env: env[tok.value] if tok.value in env else throwError("'%s' is Undefined." % tok.value)
			else:
				raise ValueError("What? '%s'" % tok.value)

	def computeNumExpr(self,minPrec):
		lhs = self.computeNum()
		while True:
			cur = self.curToken
			if cur is None or cur.name !='BINOP' or OPINFO[cur.value][0] < minPrec:
				break
			assert cur.name == 'BINOP'
			op = cur.value
			prec, assoc = OPINFO[op]
			nextMinPrec = prec + 1 if assoc == 'LEFT' else prec

			self.getNextToken()
			rhs = self.computeNumExpr(nextMinPrec)
			lhs = computeOp(op,lhs,rhs)
		return lhs

	def computeFun(self,env):
		assert self.curToken.name == 'RULE'
		funname = self.curToken.value
		ids = []
		while self.getNextToken().name == 'SYM':
			ids.append(self.curToken.value)
		body = []
		while self.curToken is not None and self.curToken.name == 'APP':
			body.append( self.computeApp() )
		fbod = lambda e,i:"".join(map(lambda x: x(e,i),body))
		env[(funname,len(ids))] = Closure(ids,fbod,env)

	def computeApp(self):
		assert self.curToken.name == 'APP'
		fname = self.curToken.value

		self.getNextToken()
		args = []
		while self.curToken is not None and (self.curToken.name == 'SYM' or self.curToken.name == 'NUM' or self.curToken.name == 'BINOP'):
			args.append( self.computeNumExpr(1) )
		return lambda env,i: self.app(fname,args,env,i)

	def app(self,F,args,env,i):
		args = map(lambda x: x(env), args )
		if i==0:
			#Change this line to execute the drawing operations or ignores
			if F not in ONEARGFUN+NOARGFUN: return ''
			if len(args)==0:
				return F
			else:
				# print F,args
				return F+"("+",".join(map(str,args))+")"
		try:
			c = env[(F,len(args))]
		except KeyError as e:
			raise Exception("There is No rule named %s defined with %i arguments." % (F,len(args)))
		#if len(args)!=len(c.ids):
		#	raise ValueError("T" % F+"("+",".join(c.ids)+")" )
		#assert len(args)==len(c.ids)
		e2 = dict(c.env,**dict(zip(c.ids, args)))
		return c.body(e2,i-1)

	def computeExpr(self):
		env = {}
		# Cero to one argument function
		env[('F',0)]  = Closure([   ], lambda env,i:  'F', env)
		env[('F',1)]  = Closure(['w'], lambda env,i:  'F', env)
		env[('f',0)]  = Closure([   ], lambda env,i:  'f', env)
		env[('f',1)]  = Closure(['w'], lambda env,i:  'f', env)
		env[('G',0)]  = Closure([   ], lambda env,i:  'G', env)
		env[('G',1)]  = Closure(['w'], lambda env,i:  'G', env)
		env[('+',0)]  = Closure([   ], lambda env,i:  '+', env)
		env[('+',1)]  = Closure(['w'], lambda env,i:  '+', env)
		env[('-',0)]  = Closure([   ], lambda env,i:  '-', env)
		env[('-',1)]  = Closure(['w'], lambda env,i:  '-', env)
		env[('^',0)]  = Closure([   ], lambda env,i:  '^', env)
		env[('^',1)]  = Closure(['w'], lambda env,i:  '^', env)
		env[('&',0)]  = Closure([   ], lambda env,i:  '&', env)
		env[('&',1)]  = Closure(['w'], lambda env,i:  '&', env)
		env[('/',0)]  = Closure([   ], lambda env,i:  '/', env)
		env[('/',1)]  = Closure(['w'], lambda env,i:  '/', env)
		env[('!',0)]  = Closure([   ], lambda env,i:  '!', env)
		env[('!',1)]  = Closure(['w'], lambda env,i:  '!', env)
		env[('%',0)]  = Closure([   ], lambda env,i:  '%', env)
		env[('%',1)]  = Closure(['w'], lambda env,i:  '%', env)
		env[('\\',0)] = Closure([   ], lambda env,i: '\\', env)
		env[('\\',1)] = Closure(['w'], lambda env,i: '\\', env)
		# No arguments functions
		env[('|',0)]  = Closure([], lambda env,i:  '|', env)
		env[('$',0)]  = Closure([], lambda env,i:  '$', env)
		env[('[',0)]  = Closure([], lambda env,i:  '[', env)
		env[(']',0)]  = Closure([], lambda env,i:  ']', env)
		env[('{',0)]  = Closure([], lambda env,i:  '{', env)
		env[('.',0)]  = Closure([], lambda env,i:  '.', env)
		env[('}',0)]  = Closure([], lambda env,i:  '}', env)
		env[('~',0)]  = Closure([], lambda env,i:  '~', env)
		env[('\'',0)] = Closure([], lambda env,i: '\'', env)
		iteration = 0
		delta = 90
		begin = lambda e,i: ''
		while self.curToken != None:
			cur = self.curToken
			if cur.name == 'ASIGN':
				self.getNextToken()
				env[cur.value] = self.computeNumExpr(1)
			elif cur.name == 'DEF':
				self.getNextToken()
				env[cur.value] = float(self.curToken.value)
				self.getNextToken()
			elif cur.name == 'DELTA':
				self.getNextToken()
				delta = float(self.curToken.value)
				self.getNextToken()
			elif cur.name == 'BEGIN':
				self.getNextToken()
				begin = self.computeApp()
			elif cur.name == 'RULE':
				self.computeFun(env)
			elif cur.name == 'ITER':
				iteration = float(cur.value)
				self.getNextToken()
			else:
				raise ValueError("This should never happen. I hope.")
		return lambda: begin(env,iteration)

def parse(text):
	p = LParser(text)
	p.getNextToken()
	f = p.computeExpr()
	return lambda: f()

def LSystem(text):
	#try:
	f = parse(text)
	return f()
	#except Exception as e:
	#	raise e

def TEST(text,res):
	l = LSystem(text)
	#assert l == res
	print l

# #iterate 10
# n = 10
# #define r1 0.9   /* contraction ratio 1 */
# #define r2 0.7   /* contraction ratio 2 */
# #define a1 10	/* branching angle 1   */
# #define a2 60	/* branching angle 2   */
# #define wr 0.707 /* width decrease rate */
#
# begin: A(1,10)
# rule: A(l,w) ::= !(w)F(l)[&(a1)B(l*r1 ,w*wr )]/(180)[&(a2 )B(l*r2 ,w*wr )]
# rule: B(l,w) ::= !(w)F(l)[+(a1 )$B(l*r1 ,w*wr )][-(a2 )$B(l*r2 ,w*wr )]

# text = """
# #iterate 4
# begin: AB
# rule: A ::= G
# rule: B ::= F
# """
# print LSystem(text)
TEST("""
#delta 90
#iterate 2
begin: F
rule: F ::= GA
rule: A ::= F
""",
"F+F-F-F+F+F+F-F-F+F-F+F-F-F+F-F+F-F-F+F+F+F-F-F+F")
#
# TEST("""
# #delta 90
# #iterate 2
# begin: F(2)
# rule: F(l) ::= F(l)+F(l)-F(l)-F(l)+F(l)
# """,
# "F(2)+F(2)-F(2)-F(2)+F(2)+F(2)+F(2)-F(2)-F(2)+F(2)-F(2)+F(2)-F(2)-F(2)+F(2)-F(2)+F(2)-F(2)-F(2)+F(2)+F(2)+F(2)-F(2)-F(2)+F(2)")
