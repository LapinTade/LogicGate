#
# simpleBool.py
#
# Example of defining a boolean logic parser using
# the operatorGrammar helper method in pyparsing.
#
# In this example, parse actions associated with each
# operator expression will "compile" the expression
# into BoolOperand subclass objects, which can then
# later be evaluated for their boolean value.
#
# Copyright 2006, by Paul McGuire
#

from pyparsing import *
import re

class BoolOperand(object):
    def __init__(self,t):
        self.args = t[0][0::2]
    def __str__(self):
        sep = " %s " % self.reprsymbol
        return "(" + sep.join(map(str,self.args)) + ")"
    
class BoolAnd(BoolOperand):
    reprsymbol = '&'
    def __nonzero__(self):
        for a in self.args:
            if isinstance(a,basestring):
                v = eval(a)
            else:
                v = bool(a)
            if not v:
                return False
        return True

class BoolOr(BoolOperand):
    reprsymbol = '|'    
    def __nonzero__(self):
        for a in self.args:
            if isinstance(a,basestring):
                v = eval(a)
            else:
                v = bool(a)
            if v:
                return True
        return False

class BoolNot(BoolOperand):
    def __init__(self,t):
        self.arg = t[0][1]
    def __str__(self):
        return "~" + str(self.arg)
    def __nonzero__(self):
        if isinstance(self.arg,basestring):
            v = eval(self.arg)
        else:
            v = bool(self.arg)
        return not v

def decompose(expr):
  regex = re.compile('\((\w+)\s+(and|or|not)\s+(\w)\)|(\w+)')
	results = regex.findall(expr)
	results = [i[:3] if i[0] else i[3] for i in results]
	return results


def calculValeur(expr):
	boolOperand = Word(alphas,max=1) | oneOf("True False")
	boolExpr = operatorPrecedence( boolOperand,
		[
		("not", 1, opAssoc.RIGHT, BoolNot),
		("and", 2, opAssoc.LEFT,  BoolAnd),
		("or",  2, opAssoc.LEFT,  BoolOr),
		])
	res = boolExpr.parseString(expr)[0]
	return res

def ordreGraphique(l):
	i = 0
	j = 0
	st=""
	arg=""
	ope=""
	while i < len(l):
		print(l[i])
		st=l[i]
		#convertir ce passage en fonction par la suite
		while j < len(st):
			if(st[j] == 'p' or st[j] == 'q' or st[j] == 'r'):
				arg += st[j]
			if(st[j] == 'and' or st[j] == 'or' or st[j] == "not"):
				ope += st[j]
			j += 1
		#On appel la fonction instruction
		instr(arg,ope)
		arg = ""
		ope = ""
		j = 0
		i=i+1
		
def instr(arg, ope):
	i = 0
	j = 0
	if(len(ope)==len(arg) and arg!="" and ope!=""):
		print("Reprendre l'expression precedente et y ajouter la nouvelle!")
	if(arg!=""):
		print("Argument :")
	while i < len(arg):
		print(arg[i])
		i+=1
	if(ope!=""):
		print("Operateur :")
	while j < len(ope):
		print(ope[j])
		j+=1

def affichePorte(expr):
	i = 0
	temp = ""
	compt = 0
	conteneur = []
	while i<len(expr):
		if(expr[i]=='and'):
			if(expr[i-1]==')'):
				compt=i-2
				temp=""
				while expr[compt]!=')':
					temp+= expr[compt]
					compt-=1
				conteneur.append(compt)
			if(expr[i-1]!=')'):
				conteneur.append(expr[i-1])
				
			conteneur.append(expr[i])
			
			if(expr[i+1]=='('):
				compt=i+2
				temp=""
				while expr[compt]!=')':
					temps+= expr[compt]
					compt+=1
				conteneur.append(compt)
			if(expr[i+1]!='('):
				if(expr[i+1]=='not'):
					conteneur.append(expr[i+1]+" "+expr[i+2])
				else:
					conteneur.append(expr[i+1])
		i+=1
	return conteneur

def compteAnd(expr):
	i = 0
	appelAnd = False
	while i<len(expr):
		if(expr[i]=='('):
			print("\t\t"+expr[i+1])
		if(expr[i]=='&'):
			if(expr[i-1]==')'):
				compt=i-2
				temp=""
				while expr[compt]!=')':
					if(expr[compt] =='&'):
						appelAnd = True
					temp+= expr[compt]
					compt-=1
				if(appelAnd == True):
					compteAnd(temp)
				if(appelAnd == False):
					print("\t\t"+temp)
			#if(expr[i-1]!=')'):
				#if(expr[i-2]=='~' and expr[i):
				#	print("\t\t"+expr[i-2]+expr[i-1])
				#if(expr[i-2]!=expr[i-1] and expr[i-2]!='&' and expr[i-1]!=')'):
				#	print "\t\t"+expr[i-1]		
			print("\t"+expr[i])
			if(expr[i+1]=='('):
				compt=i+2
				temp=""
				while expr[compt]!=')':
					if(expr[compt] =='&'):
						appelAnd = True
					temp+= expr[compt]
					compt+=1
				if(appelAnd == True):
					compteAnd(temp)
				if(appelAnd == False):
					print("\t\t"+temp)
			if(expr[i+1]!='('):
				if(expr[i+1]=='~'):
					print("\t\t"+expr[i+1]+expr[i+2])
				else:
					print("\t\t"+expr[i+1])
			appelAnd = False
		i+=1

def affiche(expr):
	i = 0
	temp = ""
	compt = 0
	decal = ""
	appelAnd = False
	while i<len(expr):
		'''if(expr[i]=='&'):
			if(expr[i-1]==')'):
				compt=i-2
				temp=""
				while expr[compt]!=')':
					if(expr[compt] == '&'):
						appelAnd = True
					temp+= expr[compt]
					compt-=1
				if(appelAnd == True):
					compteAnd(temp)
				if(appelAnd == False):
					print("\t"+temp)
			if(expr[i-1]!=')'):
				print("\t"+expr[i-1])
			else :
				print(expr[i])
				if(expr[i+1]=='('):
					compt=i+2
					temp=""
					while expr[compt]!=')':
						if(expr[compt] =='&'):
							appelAnd = True
						temp+= expr[compt]
						compt+=1
					if(appelAnd == True):
						compteAnd(temp)
					if(appelAnd == False):
						print("\t"+temp)
				if(expr[i+1]!='('):
					if(expr[i+1]=='~'):
						print("\t"+expr[i+1]+" "+expr[i+2])
					else:
						print("\t"+expr[i+1])
			appelAnd=False
		i+=1'''
		if(expr[i]=='('):
			while(expr[i]!=')'):
				if(expr[i] =='&'):
					appelAnd = True
				temp+=expr[i]
				i+=1
			if(appelAnd == True):
				compteAnd(temp)
			if(appelAnd == False):
				print("\t"+temp)
		if(expr[i]=='&'):
			if(expr[i-2]=='~'):
				print("\t"+expr[i-2]+expr[i-1])
			elif(expr[i-2]!=expr[i-1] and expr[i-2]!='&' and expr[i-1]!=')'):
				print "\t"+expr[i-1]+"\n&"
			if(expr[i+1]=='('):
				while(expr[i]!=')'):
					if(expr[i] =='&'):
						appelAnd = True
					temp+=expr[i]
					i+=1
				if(appelAnd == True):
					compteAnd(temp)
				if(appelAnd == False):
					print("\t"+temp)
			else:
				if(expr[i+1]!='~'):
					print('&\n\t'+expr[i+1])		
		appelAnd=False
		i+=1
	
	
def addapt(s):
   j=""
   for x in s.split():
      j=j+str(x)
  
   return j

choix=raw_input("Calcul de la valeur de l'expression(1), decomposition de l'expression(2) : ");

if(choix=='1'):
	expr = "( p and not q and q) and q"
	valeurBool = calculValeur(expr)
	p = True
	q = True
	r = True
	print expr,'\n', valeurBool, '=', bool(valeurBool),'\n'
	
if(choix=='2'):
	temps = []
	expr = '(q and not r and q) and r'
	test = calculValeur(expr)
	exprBool=decompose(expr)
	#ordreGraphique(str(test))
	expression = addapt(str(test))
	
	print expression[1:len(expression)-1]
	affiche(expression[1:len(expression)-1])	
