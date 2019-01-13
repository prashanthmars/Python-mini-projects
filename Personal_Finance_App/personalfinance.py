
##########CLASS FOR DOING THE TRANSACTION################################################
class jarvismoneymanager:
	def __init__(self):	
		import mysql.connector as mysqlcon
		
		################################CREATE A NEW DATABASE######################################
		mydb = mysqlcon.connect(
		  host="localhost",
		  user="root",
		  passwd=""
		)
		mycursor = mydb.cursor()

		#Check all database; If our DB exists, do not attempt creating a new one
		#else create it
		mycursor.execute('SHOW DATABASES')
		dbexistcheck=any([x[0]=='personalfinance' for x in mycursor])
				
		if(dbexistcheck):
			print("DB already exists")
		else:
			sql="CREATE DATABASE personalfinance"
			mycursor.execute(sql)
			print('DB created')
		
		#add dbname to the cursor
		mydb = mysqlcon.connect(
			host="localhost",
			user="root",
			passwd="",
			database='personalfinance'
		)
		mycursor = mydb.cursor()
		
		#Check all tables; If our table exist, do not attempt creating a new one
		#else create it
		mycursor.execute("SHOW TABLES")
		tblexistcheck=any([x[0]=='alltransactions' for x in mycursor])

		if(tblexistcheck):
			print("Table already exists")
		else:
			sql="CREATE TABLE alltransactions (id INT AUTO_INCREMENT PRIMARY KEY, transactiondate DATE NOT NULL, Itemname VARCHAR(255), Iteminfo VARCHAR(255), category VARCHAR(255), amount FLOAT)"
			mycursor.execute(sql)
			print('Table created')
			
	def __str__(self):
		
		import mysql.connector as mysqlcon
		mydb = mysqlcon.connect(
			host="localhost",
			user="root",
			passwd="",
			database='personalfinance'
		)
		
		mycursor = mydb.cursor()
		sql="SELECT * FROM alltransactions"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		return (str(myresult))
	
	def summary_category(self):
		
		import mysql.connector as mysqlcon
		mydb = mysqlcon.connect(
			host="localhost",
			user="root",
			passwd="",
			database='personalfinance'
		)
		
		mycursor = mydb.cursor()
		sql="SELECT * FROM alltransactions"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		transactionsummary={x[4]:0 for x in myresult}
		for eachentry in myresult:
			transactionsummary[eachentry[4]]+=eachentry[5]
		
		return(transactionsummary)
	

	def summary_item(self):
		
		import mysql.connector as mysqlcon
		
		mydb = mysqlcon.connect(
			host="localhost",
			user="root",
			passwd="",
			database='personalfinance'
		)
		
		mycursor = mydb.cursor()
		sql="SELECT * FROM alltransactions"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		transactionsummary={x[2]:0 for x in myresult}
		for eachentry in myresult:
			transactionsummary[eachentry[2]]+=eachentry[5]
		
		return(transactionsummary)
	
	
	def summary_yearmon(self):
		
		import mysql.connector as mysqlcon
		import datetime as dt
		import pandas
		
		mydb = mysqlcon.connect(
			host="localhost",
			user="root",
			passwd="",
			database='personalfinance'
		)
		
		mycursor = mydb.cursor()
		sql="SELECT * FROM alltransactions"
		mycursor.execute(sql)
		myresult = mycursor.fetchall()
		transactionsummary={x[1].strftime("%Y-%m"):0 for x in myresult}
			
		for eachentry in myresult:
			if eachentry[4]=='credit':
				transactionsummary[eachentry[1].strftime("%Y-%m")]+=eachentry[5]
			elif eachentry[4]=='debit':
				transactionsummary[eachentry[1].strftime("%Y-%m")]-=eachentry[5]
			else:
				next
		
		#budget summary in a csv
		filename="budgetsummary.csv"
		transactionsummary_csv=[(x,y) for x,y in transactionsummary.items()]
		pd = pandas.DataFrame(list(transactionsummary_csv))
		pd.to_csv("budgetsummary.csv")
		
		return(transactionsummary)

	
	def addtransaction(self):
		
		input_date=input("enter the transaction date\n")
		input_itemname=input("enter the name of the item\n")
		input_iteminfo=input("enter additional information of the item\n")
		input_category=input("enter the category of the item: credit or debit\n")
		input_amount=float(input("enter the transaction amount\n"))
		
		import mysql.connector as mysqlcon
		mydb = mysqlcon.connect(
			host="localhost	",
			user="root",
			passwd="",
			database='personalfinance'
		)
		
		mycursor = mydb.cursor()
		
		sql = "INSERT INTO alltransactions (transactiondate, Itemname, Iteminfo, category,amount) VALUES (%s, %s, %s, %s,%s)"
		val = [
			(input_date, input_itemname,input_iteminfo,input_category,input_amount),
		]

		mycursor.executemany(sql,val)
		mydb.commit()
		print("added transaction into database")
	
	def edittransaction(self):
		
		chosentransactionid=int(input("enter the transaction id\n"))
		
		
		import mysql.connector as mysqlcon
		mydb = mysqlcon.connect(
			host="localhost	",
			user="root",
			passwd="",
			database='personalfinance'
		)
		
		mycursor = mydb.cursor()
		sql="SELECT * FROM alltransactions WHERE id = %s"
		mycursor.execute(sql,(chosentransactionid,))
		myresult = mycursor.fetchall()[0]
		print("The below transaction would be picked up for editing")
		print(myresult)
		
		input_date=input("enter the transaction date. Just type enter to skip / no change.\n")
		if input_date=="":
			input_date=str(myresult[1])
		
		input_itemname=input("enter the name of the item. Just type enter to skip / no change.\n")
		if input_itemname=="":
			input_itemname=myresult[2]
		
		input_iteminfo=input("enter additional information of the item. Just type enter to skip / no change.\n")
		if input_iteminfo=="":
			input_iteminfo=myresult[3]
		
		input_category=input("enter the category of the item: credit or debit. Just type enter to skip / no change.\n")
		if input_category=="":
			input_category=myresult[4]
			
		input_amount=input("enter the transaction amount. Just type enter to skip / no change.\n")
		if input_amount=='':
			input_amount=float(myresult[5])
		else:
			input_amount=float(input_amount)
		
		sql = "UPDATE alltransactions SET transactiondate = %s, Itemname = %s, Iteminfo = %s, category = %s, amount = %s WHERE id=%s"
		val = [
			(input_date,input_itemname,input_iteminfo,input_category,input_amount,chosentransactionid),
		]

		mycursor.executemany(sql,val)
		mydb.commit()
		print("updated transaction into database")
		
		
##########################JARVIS IN ACTION#######################################################
		
myjarvis=jarvismoneymanager()

print("Good morning")
while 1:
	print("select the appropriate nos for the transaction")
	transactiontype=int(input("1: Add a new transaction\n2: Edit Transaction\n3: Summary: By category\n4: Summary: By Item\n5: Summary: By Year-Month\n6: All Transactions\n9: Exit App\n"))
	
	if transactiontype==1:
		print("transaction for add")
		myjarvis.addtransaction()
	
	elif transactiontype==2:
		print("Edit a specific transaction")
		myjarvis.edittransaction()
	
	elif transactiontype==3:
		print("Summary of all transaction by categories")
		print(myjarvis.summary_category())
		
	elif transactiontype==4:
		print("Summary of all transaction by item")
		print(myjarvis.summary_item())
		
	elif transactiontype==5:
		print("Summary of all transaction by year-month")
		print(myjarvis.summary_yearmon())
		
	elif transactiontype==6:
		print("Detailed list of all transactions")
		print(myjarvis)
		
	elif transactiontype==9:
		break
	
	else:
		print("enter a valid input")
		#print(myjarvis.summary())
		
print("Looking forward to see you soon")


		







