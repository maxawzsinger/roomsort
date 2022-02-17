from datetime import datetime, timedelta
import csv
import boto3

def lambda_handler(event, context):
    today = datetime.today()
    time_string = today.strftime('%d%b%y')
    
    melb_status = 'go'
    melb_counter = 1
    melb_suburb_dict = {}
   
    syd_status = 'go'
    syd_counter = 1
    syd_suburb_dict = {}
    
    syd_subs = []
    melb_subs = []

    #processing melbourne
    while melb_status == 'go':
        d= datetime.today() - timedelta(days=melb_counter)
        date_string = d.strftime('%d%b%y')
        file_name = date_string + 'melb.csv'
        s3 = boto3.resource('s3')
        obj = s3.Object('roomsortdata', file_name)
        #get file from bucket:
        try:
            body = obj.get()['Body'].read().decode('utf-8').split()
            for row in csv.reader(body):
                suburb = row[0] 
                price = row[1]
                price = float(price)
                if suburb in melb_suburb_dict:
                    melb_list = melb_suburb_dict[suburb]
                    melb_list.append([date_string, price])
                    melb_suburb_dict[suburb] = melb_list
                else:
                    melb_suburb_dict[suburb] = [[date_string, price]]
            melb_counter += 1
        except:
            melb_status = 'stop'
    
    for suburb in melb_suburb_dict:
        melb_subs.append(suburb)
        melb_list = melb_suburb_dict[suburb]
        s3 = boto3.resource('s3') #boto is aws python sdk
        bucket = s3.Bucket('www.roomsort.com.au')
        key = suburb + 'melb.csv'
        file_tmp = '/tmp/' + key
        with open(file_tmp, 'w') as f:
            w = csv.writer(f)
            w.writerows(melb_list)
        bucket.upload_file(file_tmp, key)
    
    s3 = boto3.resource('s3') #boto is aws python sdk
    bucket = s3.Bucket('www.roomsort.com.au')
    key = 'available_subs_melb.csv'
    file_tmp = '/tmp/' + key
    with open(file_tmp, 'w') as f:
        w = csv.writer(f)
        w.writerows([melb_subs])
    bucket.upload_file(file_tmp, key) 
        #https://stackoverflow.com/questions/1816880/why-does-csvwriter-writerow-put-a-comma-after-each-character
        #if i need these in a column in csv could change so for loop sends each string to a one item list
    
    #processing sydney
    while syd_status == 'go':
        d= datetime.today() - timedelta(days=syd_counter)
        date_string = d.strftime('%d%b%y')
        file_name = date_string + 'syd.csv'
        s3 = boto3.resource('s3')
        obj = s3.Object('roomsortdata', file_name)
        #get file from bucket
        try:
            body = obj.get()['Body'].read().decode('utf-8').split()
            for row in csv.reader(body):
                suburb = row[0] 
                price = row[1]
                price = float(price)
                if suburb in syd_suburb_dict:
                    syd_list = syd_suburb_dict[suburb]
                    syd_list.append([date_string, price])
                    syd_suburb_dict[suburb] = syd_list
                else:
                    syd_suburb_dict[suburb] = [[date_string, price]]
            syd_counter += 1
        except:
            syd_status = 'stop'
    
    for suburb in syd_suburb_dict:
        syd_subs.append(suburb)
        syd_list = syd_suburb_dict[suburb]
        s3 = boto3.resource('s3') #boto is aws python sdk
        bucket = s3.Bucket('www.roomsort.com.au')
        key = suburb + 'syd.csv'
        file_tmp = '/tmp/' + key
        with open(file_tmp, 'w') as f:
            w = csv.writer(f)
            w.writerows(syd_list)
        bucket.upload_file(file_tmp, key)  
    
    s3 = boto3.resource('s3') #boto is aws python sdk
    bucket = s3.Bucket('www.roomsort.com.au')
    key = 'available_subs_syd.csv'
    file_tmp = '/tmp/' + key
    with open(file_tmp, 'w') as f:
        w = csv.writer(f)
        w.writerows([syd_subs])
    bucket.upload_file(file_tmp, key) 
