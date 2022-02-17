
from datetime import datetime, timedelta
import csv
import boto3

def lambda_handler(event, context):
    today = datetime.today()
    time_string = today.strftime('%d%b%y')


    #processing melbourne
    melb_dict = {} #holds the suburbs and prices after processing

    for i in range(7):
        #get file name
        d= datetime.today() - timedelta(days=i)
        date_string = d.strftime('%d%b%y')
        file_name = 'melb' + date_string + '.csv'
        #get file from bucket
        s3 = boto3.resource('s3')
        obj = s3.Object('roomsortdata', file_name)
        try:
            body = obj.get()['Body'].read().decode('utf-8').split()
            for row in csv.reader(body):
                suburb = row[0] #trying to reference first value (suburb)
                price = row[1]
                price = float(price)
                if suburb in melb_dict:
                    melb_list = melb_dict[suburb]
                    melb_list[0] += price
                    melb_list[1] +=1
    
                else:
                    melb_dict[suburb] = [price, 1]
        except:
            break
                    
    for suburb in melb_dict:
        price_list = melb_dict[suburb]
        melb_dict[suburb] = price_list[0] / price_list[1]

    #write to s3 static website bucket FIX BELOW - have just copied over. change new_data to melb _dict
    #bring over the code getting each daily average to this function. need to keep track of total rooms per suburb for city wide average

    s3 = boto3.resource('s3') #boto is aws python sdk
    bucket = s3.Bucket('roomsortdata')
    key = time_string + 'melb.csv'
    file_tmp = '/tmp/' + key
    with open(file_tmp, 'w') as f:
        w = csv.writer(f)
        w.writerows(melb_dict.items())
    bucket.upload_file(file_tmp, key)
    
    #processing sydney
    syd_dict = {} #holds the suburbs and prices after processing

    for i in range(7):
        #get file name
        d= datetime.today() - timedelta(days=i)
        date_string = d.strftime('%d%b%y')
        file_name = 'syd' + date_string + '.csv'
        #get file from bucket
        s3 = boto3.resource('s3')
        obj = s3.Object('roomsortdata', file_name)
        try:
            body = obj.get()['Body'].read().decode('utf-8').split()
            for row in csv.reader(body):
                suburb = row[0] #trying to reference first value (suburb)
                price = row[1]
                price = float(price)
                if suburb in syd_dict:
                    syd_list = syd_dict[suburb]
                    syd_list[0] += price
                    syd_list[1] +=1
    
                else:
                    syd_dict[suburb] = [price, 1]
        except:
            break
        
    for suburb in syd_dict:
        price_list = syd_dict[suburb]
        syd_dict[suburb] = price_list[0] / price_list[1]

    #write to s3 static website bucket FIX BELOW - have just copied over. change new_data to melb _dict
    #bring over the code getting each daily average to this function. need to keep track of total rooms per suburb for city wide average

    s3 = boto3.resource('s3') #boto is aws python sdk
    bucket = s3.Bucket('roomsortdata')
    key = time_string + 'syd.csv'
    file_tmp = '/tmp/' + key
    with open(file_tmp, 'w') as f:
        w = csv.writer(f)
        w.writerows(syd_dict.items())
    bucket.upload_file(file_tmp, key)
