#-*- coding: utf-8 -*- 
from pyparsing import *
from string import *
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
	i = 0
	j = 0
	nombreInsertion = 0
	exprPar = 1
	print l
	porte=[]
	while i<len(l):
		if(len(str(l[i]))==1):
			print l[i]
			try :
				if(str(l[i-1])=='or' or str(l[i-1])=='and'):
					if(len(str(l[i+1]))>3):
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
				if(len(str(l[i+2]))>3):
					porte.append(l[i]+","+l[i+1]+","+str(nombreInsertion+1))
					nombreInsertion+=1
					i+=2
				else :
					porte.append(l[i]+","+l[i+1]+","+l[i+2])
					nombreInsertion+=1
					i+=2
			except Exception :
				None
		if(len(str(l[i]))==2 or len(str(l[i]))==3):
			try :
				if(l[i]=="and" or l[i]=="or"):
					if(len(str(l[i-1]))>3 and (l[i-2]=='and' or l[i-2]=='or')):
						if(len(str(l[i+1]))>3):
							if(len(str(l[i-1]))>3):
								if(l[i-2]=='and' or l[i-2]=='or'):
									if(len(str(l[i-3]))==1):
										porte.append(str(nombreInsertion-exprPar)+","+l[i]+","+str(nombreInsertion+1))
									else:
										porte.append(str(nombreInsertion-exprPar-1)+","+l[i]+","+str(nombreInsertion+1))
							else:
								porte.append(str(nombreInsertion-exprPar)+","+l[i]+","+str(nombreInsertion+1))
						elif(l[i+1]=='not' and len(str(l[i+2]))==1):
							porte.append(str(nombreInsertion-1)+","+l[i]+","+l[i+1]+" "+l[i+2])
						else : 
							porte.append(str(nombreInsertion-exprPar)+","+l[i]+","+l[i+1])
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
								try:
									if(len(str(l[i+2]))>1):
										porte.append(str(nombreInsertion-1)+","+l[i]+","+str(nombreInsertion+2))
								except Exception:
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
			except Exception :
					None
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

#terminer ca !
def testNewCompose(l, expr):
	test = addapt(str(calculValeur(expr)))
	global porteTemp
	porteTemp = []
	tabTemp = []
	porte = []
	compt = 0
	intTemp = 0
	test2=compteParent(expr,0)
	print "quoi " + str(test2)
	t = 1
	inter = 0
	callPar = 0	
	while t <len(l):
		try :
			if(t>1):
				test2=compteParent(expr,callPar)
				print "TEST 2 " + str(test2)
			#if(len(str(l[t]))>3):
			#	print len(l[t][0]) + len(l[t][1])+len(l[t][2]) + 2
			#if(t==
			#	test=compteParent(addapt(expr2),inter)
			if(test2==-1):
				callPar += 1
				intTemp=calculDebut(l,test,t,intTemp)
				t+=intTemp	
			elif(test2==0):
				if(intTemp != 0 ):
					if(len(str(l[t-1]))>3):
						tempPar = compteParent(expr,callPar)
						if(tempPar==1):
							porteTemp.append(str(intTemp-1)+","+l[t-1]+","+str(intTemp+1))
						else:
							porteTemp.append(str(intTemp-2)+","+l[t-1]+","+l[t])
						#t+=1
						intTemp+=1
					elif(len(str(l[t-1]))==1):
						tempPar = compteParent(expr,callPar)
						if(tempPar==1):
							porteTemp.append(str(intTemp-1)+","+l[t-2]+","+str(intTemp+1))
						else:
							porteTemp.append(str(intTemp-1)+","+l[t]+","+l[t+1])
						#t+=1
						intTemp+=1
					else:
						tempPar = compteParent(expr,callPar)
						print tempPar
						if(tempPar!=0):
							porteTemp.append(str(intTemp-2)+","+l[t-1]+","+l[t])
							intTemp+=1
				else:
					if(len(str(l[t-1]))==1):
						if(str(l[t-2])=='or' or str(l[t-2])=='and'):
							if(len(str(l[i+1]))>3):
								porteTemp.append(str(t-1)+","+l[i]+","+str(t+1))
							elif(len(str(l[i+1]))==1):
								porteTemp.append(str(t-1)+","+l[i]+","+l[i+1])
						else:		
							porteTemp.append(l[t-1]+","+l[t]+","+l[t+1])
						t+=1
			elif(test2==1):
				callPar+=1
				t+=calculFin(l,test,t,intTemp)
				t+=1
			#	print "COMPT " + str(l[t+1])
			#elif(test==1):
			#	t+=calculFin(l,addapt(expr2))
			#else:
			#	print "FUCK" + str(l[t])
		except Exception:
			None
		t+=1
	for j in range(0, len(porte) ):
		try:	
			porteTemp[j]=porteTemp[j].split(',')
		except Exception:
			None
	#porteTemp.append(str(test-1)+","+l[test+1]+","+str(test+1))
	porte=remiseEnForme(porteTemp)
	#print porte
	return porte
	#if(test == 1):
	#porte=calculFin(l,addapt(expr2))
	

def compteParent(expr,inter):
	i = 0
	parentDeb = 0
	parentFin = 0
	temp = 0
	callE = 0
	nombreOuvrante = 0
	nombreFermante = 0
	while i < len(expr):
		if(i==temp and expr[i]=='('):
			parentDeb +=1
		else:
			temp+=1
		if(expr[i]=='(' and expr[i-1]=='('):
			parentDeb +=1
		if(expr[i]=='('):
			nombreOuvrante += 1
		if(expr[i]==')'):
			nombreFermante += 1
		if(nombreFermante==nombreOuvrante and nombreOuvrante > 0):	
			j = i
			while expr[j]==')':
				parentFin +=1
				j-=1
			if(callE == inter):
				break
			else:
				while expr[i]!='(':
					temp = i+1
					i+=1
				i-=1
				callE+=1
				parentDeb = 0
				parentFin = 0
		i+=1
	#print "NOMBRE OUVRE " + str(parentDeb)
	#print "NOMBRE FERME " + str(parentFin)
	if(parentDeb>parentFin):
		return -1
	elif(parentDeb<parentFin):
		return 1
	else:
		return 0
	print str(parentDeb) + " " + str(parentFin)
	
	
def calculDebut(l,expr,t,nbInser):
	i = 1
	#print expr
	nombreOuvrante = 0
	nombreFermante = 0
	while i < len(expr):
		if(expr[i]=='('):
			nombreOuvrante += 1
		if(expr[i]==')'):
			nombreFermante += 1
		if(nombreFermante==nombreOuvrante and nombreOuvrante > 0):
			break
		i+=1
	i = t-1
	parVu = 0
	nombreInsertion = nbInser
	while i<len(l):
		if(len(str(l[i]))>3):
			nombreOuvrante -= 1
			parVu+=1
			porteTemp.append(l[i])
			nombreInsertion+=1
		elif(l[i]=='and' or l[i]=='or'):
			if(len(str(l[i+1]))>3):
				porteTemp.append(str(nombreInsertion-1-parVu+1)+","+l[i]+","+str(nombreInsertion+1))
				nombreOuvrante-=1
				nombreInsertion+=1
			elif(len(str(l[i+1]))==1):
				#if(len(str(l[i-1]))==1 and (l[i-2]!='not' and l[i-2]!='or')):
				#	porteTemp.append(l[i-1]+","+l[i]+","+l[i+1])
				#	nombreInsertion+=1
					#i+=1
				#else:
				porteTemp.append(str(nombreInsertion-parVu)+","+l[i]+","+l[i+1])
				nombreInsertion+=1
				#parVu+=1
				nombreOuvrante -=1
				
		#elif(len(str(l[i]))==1):
			#if(len(str(l[i+2]))>3):
			#	porteTemp.append(l[i]+","+l[i+1]+","+str(nombreInsertion+parVu))
			#else:
			#	print "hihi"
		if(nombreOuvrante==0):
			break
		i+=1
		
	for j in range(0, len(porteTemp) ):
		try:	
			porteTemp[j]=porteTemp[j].split(',')
		except Exception:
			None		
	return nombreInsertion		
		
def calculFin(l,expr,t,nbInser):
	i = 0
	#print expr
	nombreOuvrante = 0
	nombreFermante = 0
	while i <= len(expr):
		if(expr[i]=='('):
			nombreOuvrante += 1
		if(expr[i]==')'):
			nombreFermante += 1
		if(nombreFermante==nombreOuvrante and nombreOuvrante > 0):
			break
		i+=1
	i = t-1
	parVu = 0
	nombreInsertion = nbInser
	while i<len(l):
		try :
			if(len(str(l[i]))>3):
				nombreOuvrante -= 1
				parVu+=1
				porteTemp.append(l[i])
				nombreInsertion+=1
			elif(len(str(l[i]))==1):
				if(len(str(l[i+2]))>3):
					print l[i]+l[i+3]
					if(l[i+3]=='and' or l[i+3]=='or'):
						parVu+=1
						porteTemp.append(l[i]+","+l[i+1]+","+str(nombreInsertion+1+parVu))
					else:
						parVu+=1
						porteTemp.append(l[i]+","+l[i+1]+","+str(nombreInsertion+parVu))
					nombreOuvrante-=1
					nombreInsertion+=1
					i+=1
				if(len(str(l[i+2]))==1):
					porteTemp.append(l[i]+","+l[i+1]+","+str(nombreInsertion+1+parVu))
					nombreInsertion+=1
					i+=1
			elif(l[i]=='and' or l[i]=='or'):
				if(len(str(l[i+1]))>3):
					if(len(str(l[i-1]))==1):
						parVu+=1
						porteTemp.append(l[i-1]+","+l[i]+","+str(nombreInsertion+parVu))
					else:
						porteTemp.append(str(nombreInsertion-parVu+1)+","+l[i]+","+str(nombreInsertion+1))
					nombreOuvrante-=1
					nombreInsertion+=1
				elif(len(str(l[i+1]))==1):
					if(len(str(l[i-1]))>3):
						porteTemp.append(str(nombreInsertion-parVu)+","+l[i]+","+str(nombreInsertion+1))
					else:
						porteTemp.append(str(nombreInsertion-parVu-1)+","+l[i]+","+str(nombreInsertion+1))
				elif(len(str(l[i-1]))==1):
					#if(len(str(l[i-1]))==1 and (l[i-2]!='not' and l[i-2]!='or')):
					#porteTemp.append(l[i-1]+","+l[i]+","+l[i+1])
					#	nombreInsertion+=1
						#i+=1
					#else:
					porteTemp.append(str(nombreInsertion-parVu)+","+l[i]+","+l[i+1])
					nombreInsertion+=1
					#parVu+=1
					nombreOuvrante -=1
				elif(len(str(l[i-1]))>3):
					porteTemp.append(str(nombreInsertion-parVu)+","+l[i]+","+str(nombreInsertion+1))
					nombreInsertion+=1

			#elif(len(str(l[i]))==1):
				#if(len(str(l[i+2]))>3):
				#	porteTemp.append(l[i]+","+l[i+1]+","+str(nombreInsertion+parVu))
				#else:
				#	print "hihi"
			if(nombreOuvrante==0):
				break
		except Exception:
			None
		i+=1
		
	for j in range(0, len(porteTemp) ):
		try:	
			porteTemp[j]=porteTemp[j].split(',')
		except Exception:
			None
			
	return nombreInsertion
	
	
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
		#expr = '((a or not r) and (a or b)) and (a or not r) or not(x and y)' # OK!
		temps = []
		#expr = 'a and b or ((a and b) or (c and d))' #Ok!
		#expr = 'a and b or (a and c)' #ok
		#expr = '(((a and b) and a) or (a and b)) and ((a and b) and (b and c))' # nOk problème, appel calculDébut
		#expr = '(((a and b) or (b and c)) and c) or (b and (c and b))' # OK
		#expr = '(a and not b)' #ok
		#expr = '(((a and b) and c) and (b and c)) and b' #Nok
		#expr = '(a and b) and ((b or c) and (c or d))'#marche pas a and (((( a and b) and c) and e) and c) and (( a and c) and c)
		#expr = '(a and ((b or c) or (d or f)))'# Ok !
		#expr = '(a and (b and (c and (c or d))))' # OK
		#expr = '(a and b or c)'#OK
		#expr = '((a and b) and (a and (b and (c and (b and d)))))' #OK !
		#expr = '(a and not b)'#ok
		#expr = '(a and b) and (b and c)'#OK
		#expr = '(a and v) and c and ((a and b) and (b and c))' #a gerer les priorités entre parenthèses.
		#expr = 'a and b and c and d'#nok
		#expr = '(a and not r) and b'#ok
		expr = 'a or b and not b'#ok
		test = calculValeur(expr)
		print "TEST"+str(test)
		exprBool=decompose(expr)
		print("\n"+str(exprBool)+"\n")
		comptePorte(exprBool)
		donneEntree(exprBool)
		######################################### C'EST ICI QUE CA CE PASSE #####################################
		prote = []
		testCh = addapt(str(calculValeur(expr)))
		testP = compteParent(expr,0)
		print "TEST P" + str(testP)
		if(testP == 0):
			print(composition(exprBool))
		else:	
			prote=testNewCompose(exprBool)
			for j in range(0, len(prote) ):
				try:	
					prote[j]=prote[j].split(',')
				except Exception:
					None
			print prote
		#ordreGraphique(str(test))
		#expression = addapt(str(test))
