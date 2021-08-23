from cassandra.cluster import Cluster
cluster = Cluster(contact_points=['127.0.0.1'], port=9042)
session = cluster.connect("bd04")
def register(u,e,p):
	session.execute("INSERT INTO users (username,email,password) VALUES (%s,%s,%s)",(u,e,p))
	return
	
def login(u,p):
	future = session.execute("SELECT password FROM users WHERE username = '{0}'".format(u))
	return p == future.one().password

def cCarro(c,u):
	session.execute("INSERT INTO carrito_by_user (username,car,status) VALUES (%s,%s,%s)",(u,c,0))
	return

def aCarro(p,c,q):
	pro = session.execute("SELECT valor FROM producto WHERE product = {0}".format(p))
	vp = int(pro.one().valor)
	session.execute("INSERT INTO product_by_car (car,product,cantidad,valor,status) VALUES (%s,%s,%s,%s,%s)",(c,p,q,vp*q,0))	
	return

def qCarro(p,c):
	session.execute("DELETE FROM product_by_car WHERE product = {0} and car = {1}".format(p,c))	
	return

def eCarro(c):
	session.execute("UPDATE bd04.carrito_by_user SET status = {0} WHERE car = {1}".format(2,c))
	session.execute("DELETE FROM product_by_car WHERE car = {0}".format(c))
	return
	

def vCarro(c):
	total = 0
	compra = session.execute("SELECT * FROM product_by_car WHERE car = {0}".format(c))
	print("Factura Carrito: " + str(c))
	for com in compra:
		pro = session.execute("SELECT nombre FROM producto WHERE product = {0}".format(com.product))
		np = pro.one().nombre
		total+=com.valor
		print("{0} por valor total de: {1}".format(np,com.valor))
	print("Total a pagar por el carro: " + str(total))
	return

def comprar(c):
	session.execute("UPDATE bd04.carrito_by_user SET status = {0} WHERE car = {1}".format(1,c))
	up = session.execute("SELECT product FROM product_by_car WHERE car = {0}".format(c))
	for date in up:
		session.execute("UPDATE bd04.product_by_car SET status = {0} WHERE car = {1} and product = {2}".format(1,c,date.product))

	vCarro(c)
	return
def tProduct(p):
	total = 0
	pro = session.execute("SELECT nombre FROM producto WHERE product = {0}".format(p))
	np = pro.one().nombre
	ducto = session.execute("SELECT cantidad FROM product_by_car WHERE product = {0} and status = {1} allow filtering".format(p,0))
	for obj in ducto:
		total += obj.cantidad
	print("Total del producto {0} en los carritos es: {1}".format(np,total))
	return
def main():
	"""usuarios = session.execute("SELECT * FROM users")
	for u in usuarios:
		print (u.username, u.email, u.password)
	future = session.execute("SELECT password FROM users WHERE username = 'pedro'")
	print(future.one().password)"""
	#print(login('pedro','1234'))
	return
main()

