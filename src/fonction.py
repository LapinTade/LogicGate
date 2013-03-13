#-*- coding: utf-8 -*- 
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
	regex = re.compile('\((\w+)\s+(and|or|and\s+not|or\s+not)\s+(\w)+\)|(\w+)|not(\w)')
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

#Fonction qui retourne un dictionnaire contenant les portes utilisees.

def comptePorte(l):
	i = 0
	j = 0
	portes = {}
	portes["or"]=0
	portes["and"]=0
	portes["not"]=0
	for i in range(0, len(l) ):
		for j in range(0, len(l[i]) ):
				if(l[i][j]=='or'):
					portes["or"]+=1
				elif(l[i][j]=='and'):
					portes["and"]+=1
				elif(l[i][j]=='and not'):
					portes["and"]+=1
					portes["not"]+=1
				elif(l[i][j]=='or not'):
					portes["or"]+=1
					portes["not"]+=1          			
		if(l[i]=='and'):
			portes["and"]+=1
		elif(l[i]=='or'):
			portes["or"]+=1
		elif(l[i]=='not'):
			portes["not"]+=1
	print "Portes utilisees : " + str(portes) + "\n"
	return portes

#Fonction qui renvoit les entrees utilisees dans l'expression.

def donneEntree(l):
	i = 0
	j = 0
	t = 0
	test=""
	testsec=""
	entree=[]
	dejaVu=False
	for i in range(0, len(l) ):
		for j in range(0, len(l[i]) ):
			if(l[i][j]=='a' or l[i][j]=='o' or l[i][j]=='n'):
				try :
					test=l[i][j]+l[i][j+1]
					testsec=l[i][j]+l[i][j+1]+l[i][j+2]
				except Exception:
					None
				if(test!='or' and testsec!='and' and testsec!='not'):
					for t in range(0, len(entree)):
						if(l[i][j]==entree[t]):
							dejaVu=True
					if(dejaVu==False):
						entree.append(l[i][j])
						dejaVu=False
			elif(l[i][j]!='or' and l[i][j]!='and' and l[i][j]!='and not' and l[i][j]!='or not'):
				try :
					test=l[i][j-1]+l[i][j]
					testsec=l[i][j-2]+l[i][j-1]+l[i][j]
				except Exception:
					dejaVu=False
					for t in range(0, len(entree)):
						if(l[i][j]==entree[t]):
							dejaVu=True
					if(dejaVu==False):
						entree.append(l[i][j])
						dejaVu=False
				if(test!='or' and testsec!='and' and testsec!='not'):
					dejaVu=False
					for t in range(0, len(entree)):
						if(l[i][j]==entree[t]):
							dejaVu=True
					if(dejaVu==False):
						entree.append(l[i][j])
						dejaVu=False
	print "Entrees : " + str(entree) + "\n"
	return entree

def composition(l):
	tab=[]
	i = 0
	j = 0
	nombreInsertion = 0
	exprPar = 0
	print l
	porte=[]
	while i<len(l):
		if(len(str(l[i]))==1):
			print l[i]
			try :
				if(l[i+2]=="not"):
					print "lol"
					#porte.append(l[i]+","+l[i+1]+","+l[i+2]+" "+l[i+3])
					#nombreInsertion+=1
				elif(str(l[i-1])=='or' or str(l[i-1])=='and'):
					porte.append(str(nombreInsertion-1)+","+l[i+1]+","+l[i+2])
					nombreInsertion+=1
					i+=2
				elif(l[i-1]=='not'):
					if(str(l[i-2])=='or' or str(l[i-2])=='and'):
						porte.append(str(nombreInsertion-1)+","+l[i+1]+","+l[i+2])
						nombreInsertion+=1
						i+=2
					else:
						porte.append(l[i]+","+l[i+1]+","+l[i+2])
						nombreInsertion+=1
						i+=2
				else :
					porte.append(l[i]+","+l[i+1]+","+l[i+2])
					nombreInsertion+=1
					i+=2
			except Exception :
				None
		if(len(str(l[i]))==2 or len(str(l[i]))==3):
			if(l[i]=="and" or l[i]=="or"):
				if(len(str(l[i-1]))>3 and (l[i-2]=='and' or l[i-2]=='or')):
					if(len(str(l[i+1]))>3):
						exprPar = 1
						porte.append(str(nombreInsertion-1-exprPar)+","+l[i]+","+str(nombreInsertion+1))
					elif(l[i+1]=='not' and len(str(l[i+2]))==1):
						porte.append(str(nombreInsertion-1)+","+l[i]+","+l[i+1]+" "+l[i+2])
					else : 
						exprPar = 1
						porte.append(str(nombreInsertion-1-exprPar)+","+l[i]+","+l[i+1])
					nombreInsertion+=1
				elif(l[i+1]=='not' and len(str(l[i+2]))==1):
					porte.append(str(nombreInsertion-1)+","+l[i]+","+l[i+1]+" "+l[i+2])
					nombreInsertion+=1
				elif(l[i+1]=='not' and len(str(l[i+2]))>3):
					porte.append(str(nombreInsertion-1)+","+l[i]+","+l[i+1]+" "+str(nombreInsertion+1))
					nombreInsertion+=1
				elif(len(str(l[i-1]))==1):
					if(str(l[i-2])=='or' or str(l[i-2])=='and'):
						if(len(str(l[i+1]))>3):
							porte.append(str(nombreInsertion-1)+","+l[i]+","+str(nombreInsertion+1))
						elif(len(str(l[i+1]))==1):
							porte.append(str(nombreInsertion-1)+","+l[i]+","+l[i+1])
						nombreInsertion+=1
				elif(len(str(l[i+1]))>1):
					porte.append(str(nombreInsertion-1)+","+l[i]+","+str(nombreInsertion+1))
					nombreInsertion+=1
				else:
					porte.append(str(nombreInsertion-1)+","+l[i]+","+l[i+1])
					nombreInsertion+=1
		elif(len(str(l[i]))>3):
			porte.append(l[i])
			nombreInsertion+=1
		i+=1
	for j in range(0, len(porte) ):
		try:	
			porte[j]=porte[j].split(',')
		except Exception:
			None
	portes=remiseEnForme(porte)
	return portes
	
	
def remiseEnForme(l):
	porte=[]
	i = 0
	for i in range(0, len(l)):
		tempVar=""
		if(l[i][1]=='and not'):
			temp=list(l[i])
			temp[1]='and'
			tempVar=temp[2]
			temp[2]='not '+temp[2]
			porte.append(temp)
		elif(l[i][1]=='or not'):
			temp=list(l[i])
			temp[1]='or'
			tempVar=temp[2]
			temp[2]='not '+temp[2]
			porte.append(temp)
		elif(l[i][1]=='or' or l[i][1]=='and'):
			temp=list(l[i])
			porte.append(temp)
		else:
			porte.append(l[i])
	return porte	

if __name__=="__main__":
		
	choix=raw_input("Calcul de la valeur de l'expression(1), decomposition de l'expression(2) : ");

	if(choix=='1'):
		expr = "p and q"
		valeurBool = calculValeur(expr)
		test=decompose(expr)
		entree=donneEntree(test)
		#p = True
		#q = False
		#r = True
		dic = {}
		dic["q"]=True
		dic["p"]=True
		print entree
		str(valeurBool).replace(entree[0],dic["q"])
		#print expr,'\n', valeurBool, '=', bool(valeurBool),'\n'
		
	if(choix=='2'):
		temps = []
		#expr = '((a or not r) and (a or b)) and (a or not r) or not(x and y)'
		#expr = 'a and b or ((a and b) or (c and d))'
		#expr = '(((a and b) and (b and c)) or (b and c)) and ((a and b) and (b and c))'
		expr = '(a and b) and ((a and b) and (c and b))'
		#expr = '(a and not b)'
		#expr = '(a and v) and c or c and ((a and b) and (b and c))' a gerer les priorités entre parenthèses.
		#expr = 'a and b and c and d'
		#expr = '(a and not r) and b'
		#expr = 'a or b and not b'
		test = calculValeur(expr)
		exprBool=decompose(expr)
		print("\n"+str(exprBool)+"\n")
		comptePorte(exprBool)
		donneEntree(exprBool)
		print(composition(exprBool))
		#ordreGraphique(str(test))
		#expression = addapt(str(test))
