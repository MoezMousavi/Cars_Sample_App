import mysql.connector
import random

def get_array_of_randoms(length, limit):
    randoms = []
    for x in range(length):
        candidate = random.randrange(limit)
        while candidate in randoms:
            candidate = random.randrange(limit)
        randoms.append(candidate)
    randoms = list(dict.fromkeys(randoms))
    return randoms

def trim_table(selectQuery, deleteQuery, max, toDelete, cnx):
    cursor = cnx.cursor()
    cursor.execute(selectQuery)
    IDs = cursor.fetchall()
    cursor.close()
    
    if len(IDs) > max:
        randoms = get_array_of_randoms(len(IDs) - max + toDelete, len(IDs))
        print(len(randoms))
        cursor = cnx.cursor()
        # Don't delete car 1 as that is where enquiries get posted
        for x in randoms:
            if x != 0:
                cursor.execute(deleteQuery, IDs[x])
        cnx.commit()
        cursor.close()

config = {
  'user': 'root',
  'password': 'AppDynamics',
  'host': 'mysql',
  'database': 'supercars',
  'raise_on_warnings': True
}

carsQuery = 'SELECT CAR_ID FROM CARS'
carsDelete = 'DELETE FROM CARS WHERE CAR_ID = %s'
enquiryQuery = 'SELECT ENQUIRY_ID FROM ENQUIRIES'
enquiryDelete = 'DELETE FROM ENQUIRIES WHERE ENQUIRY_ID = %s'

maxCars = 3000
carsToDelete = 2000
maxEnquiries = 3000
enquiriesToDelete = 2000

print('Start Cleanup')
cnx = mysql.connector.connect(**config)

trim_table(carsQuery, carsDelete, maxCars, carsToDelete, cnx)
print('End CARS cleanup')
print('Start ENQUIRIES cleanup')
trim_table(enquiryQuery, enquiryDelete, maxEnquiries, enquiriesToDelete, cnx)
print('End ENQUIRIES cleanup')

cnx.close()