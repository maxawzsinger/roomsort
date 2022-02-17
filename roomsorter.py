import imaplib
import getpass
import re
import email
from email.parser import BytesParser
import datetime
import csv
import os
import sys
import boto3
from operator import add
def lambda_handler(event, context):

    syd_suburbs = ['abbotsbury', 'abbotsford', 'acacia gardens', 'agnes banks', 'airds', 'alexandria', 'alfords point', 'allambie heights', 'allawah', 'ambarvale', 'annandale', 'annangrove', 'arcadia', 'arncliffe', 'arndell park', 'artarmon', 'ashbury', 'ashcroft', 'ashfield', 'asquith', 'auburn', 'austral', 'avalon beach', 'badgerys creek', 'balgowlah', 'balgowlah heights', 'balmain', 'balmain east', 'bangor', 'banksia', 'banksmeadow', 'bankstown', 'bankstown aerodrome', 'barangaroo', 'barden ridge', 'bardia', 'bardwell park', 'bardwell valley', 'bass hill', 'baulkham hills', 'bayview', 'beacon hill', 'beaconsfield', 'beaumont hills', 'beecroft', 'belfield', 'bella vista', 'bellevue hill', 'belmore', 'belrose', 'berala', 'berkshire park', 'berowra', 'berowracreek', 'berowra heights', 'berowra waters', 'berrilee', 'beverley park', 'beverly hills', 'bexley', 'bexley north', 'bickleyvale', 'bidwill', 'bilgola beach', 'bilgola plateau', 'birchgrove', 'birrong', 'blackett', 'blacktown', 'blair athol', 'blairmount', 'blakehurst', 'bligh park', 'bondi', 'bondi beach', 'bondi junction', 'bonnet bay', 'bonnyrigg', 'bonnyrigg heights', 'bossley park', 'botany', 'bow bowing', 'box hill', 'bradbury', 'breakfast point', 'brighton le sands', 'bringelly', 'bronte', 'brooklyn', 'brookvale', 'bundeena', 'bungarribee', 'burraneer', 'burwood', 'burwood heights', 'busby', 'cabarita', 'cabramatta', 'cabramatta west', 'caddens', 'cambridge gardens', 'cambridge park', 'camden', 'camden south', 'camellia', 'cammeray', 'campbelltown', 'camperdown', 'campsie', 'canada bay', 'canley heights', 'canley vale', 'canoelands', 'canterbury', 'caringbah', 'caringbah south', 'carlingford', 'carlton', 'carnes hill', 'carramar', 'carss park', 'cartwright', 'castle cove', 'castle hill', 'castlecrag', 'castlereagh', 'casula', 'catherine field', 'cattai', 'cawdor', 'cbd' 'cecil hills', 'cecil park', 'centennial park', 'central business district', 'chatswood', 'chatswood west', 'cheltenham', 'cherrybrook', 'chester hill', 'chifley', 'chippendale', 'chipping norton', 'chiswick', 'chullora', 'church point', 'claremont meadows', 'clarendon', 'clareville', 'claymore', 'clemton park', 'clontarf', 'clovelly', 'clyde', 'coasters retreat', 'cobbitty', 'colebee', 'collaroy', 'collaroy plateau', 'colyton', 'como', 'concord', 'concord west', 'condell park', 'connells point', 'constitution hill', 'coogee', 'cornwallis', 'cottage point', 'cowan', 'cranebrook', 'cremorne', 'cremorne point', 'cromer', 'cronulla', 'crows nest', 'croydon', 'croydon park', 'cumberland reach', 'curl curl', 'currans hill', 'currawong beach', 'daceyville', 'dangar island', 'darling point', 'darlinghurst', 'darlington', 'davidson', 'dawes point', 'dean park', 'dee why', 'denham court', 'denistone', 'denistone east', 'denistone west', 'dharruk', 'dolans bay', 'dolls point', 'doonside', 'double bay', 'dover heights', 'drummoyne', 'duffys forest', 'dulwich hill', 'dundas', 'dundas valley', 'dural', 'eagle vale', 'earlwood', 'east gordon', 'east hills', 'east killara', 'east kurrajong', 'east lindfield', 'east ryde', 'eastern creek', 'eastgardens', 'eastlakes', 'eastwood', 'ebenezer', 'edensor park', 'edgecliff', 'edmondson park', 'elanora heights', 'elderslie', 'elizabeth bay', 'elizabeth hills', 'ellis lane', 'elvina bay', 'emerton', 'emu heights', 'emu plains', 'enfield', 'engadine', 'englorie park', 'enmore', 'epping', 'ermington', 'erskine park', 'erskineville', 'eschol park', 'eveleigh', 'fairfield', 'fairfield east', 'fairfield heights', 'fairfield west', 'fairlight', 'fiddletown', 'five dock', 'flemington', 'forest glen', 'forest lodge', 'forestville', 'freemans reach', 'frenchs forest', 'freshwater', 'galston', 'georges hall', 'gilead', 'girraween', 'gladesville', 'glebe', 'gledswood hills', 'glen alpine', 'glendenning', 'glenfield', 'glenhaven', 'glenmore park', 'glenorie', 'glenwood', 'glossodia', 'gordon', 'granville', 'grasmere', 'grays point', 'great mackerel beach', 'green valley', 'greenacre', 'greendale', 'greenfield park', 'greenhills beach', 'greenwich', 'gregory hills', 'greystanes', 'grose vale', 'grose wold', 'guildford', 'guildford west', 'gymea', 'gymea bay', 'haberfield', 'hammondville', 'harrington park', 'harris park', 'hassall grove', 'haymarket', 'heathcote', 'hebersham', 'heckenberg', 'henley', 'hillsdale', 'hinchinbrook', 'hobartville', 'holroyd', 'holsworthy', 'homebush', 'homebush west', 'horningsea park', 'hornsby', 'hornsby heights', 'horsley park', 'hoxton park', 'hunters hill', 'huntingwood', 'huntleys cove', 'huntleys point', 'hurlstone park', 'hurstville', 'hurstville grove', 'illawong', 'ingleburn', 'ingleside', 'jamisontown', 'jannali', 'jordan springs', 'kangaroo point', 'kareela', 'kearns', 'kellyville', 'kellyville ridge', 'kemps creek', 'kensington', 'kenthurst', 'kentlyn', 'killara', 'killarney heights', 'kings langley', 'kings park', 'kingsford', 'kingsgrove', 'kingswood', 'kingswood park', 'kirkham', 'kirrawee', 'kirribilli', 'kogarah', 'kogarah bay', 'kuringgai chase', 'kurmond', 'kurnell', 'kurraba point', 'kurrajong', 'kurrajong hills', 'kyeemagh', 'kyle bay', 'la perouse', 'lakemba', 'lalor park', 'lane cove', 'lane cove north', 'lane cove west', 'lansdowne', 'lansvale', 'laughtondale', 'lavender bay', 'leets vale', 'leichhardt', 'len waters estate', 'leonay', 'leppington', 'lethbridge park', 'leumeah', 'lewisham', 'liberty grove', 'lidcombe', 'lilli pilli', 'lilyfield', 'lindfield', 'linley point', 'little bay', 'liverpool', 'llandilo', 'loftus', 'londonderry', 'long point', 'longueville', 'lovett bay', 'lower portland', 'lucas heights', 'luddenham', 'lugarno', 'lurnea', 'macquarie fields', 'macquarie links', 'macquarie park', 'maianbar', 'malabar', 'manly', 'manly vale', 'maraylya', 'marayong', 'maroota', 'maroubra', 'marrickville', 'marsden park', 'marsfield', 'mascot', 'matraville', 'mays hill', 'mccarrs creek', 'mcgraths hill', 'mcmahons point', 'meadowbank', 'melrose park', 'menai', 'menangle park', 'merrylands', 'merrylands west', 'middle cove', 'middle dural', 'middleton grange', 'miller', 'millers point', 'milperra', 'milsons passage', 'milsons point', 'minchinbury', 'minto', 'minto heights', 'miranda', 'mona vale', 'monterey', 'moore park', 'moorebank', 'morning bay', 'mortdale', 'mortlake', 'mosman', 'mount annan', 'mount colah', 'mount druitt', 'mount kuringgai', 'mount lewis', 'mount pritchard', 'mount vernon', 'mulgoa', 'mulgrave', 'narellan vale', 'naremburn', 'narrabeen', 'narraweena', 'narwee', 'nelson', 'neutral bay', 'newington', 'newport', 'newtown', 'normanhurst', 'north balgowlah', 'north bondi', 'north curl curl', 'north epping', 'north kellyville', 'north manly', 'north narrabeen', 'north parramatta', 'north richmond', 'north rocks', 'north ryde', 'north st ives', 'north st marys', 'north strathfield', 'north sydney', 'north turramurra', 'north willoughby', 'north wahroonga', 'northbridge', 'northmead', 'northwood', 'norwest', 'oakhurst', 'oakville', 'oatlands', 'oatley', 'old guildford', 'old toongabbie', 'oran park', 'orchard hills', 'oxford falls', 'oxley park', 'oyster bay', 'paddington', 'padstow', 'padstow heights', 'pagewood', 'palm beach', 'panania', 'parklea', 'parramatta', 'peakhurst', 'peakhurst heights', 'pemulwuy', 'pendle hill', 'pennant hills', 'penrith', 'penshurst', 'petersham', 'phillip bay', 'picnic point', 'pitt town', 'pitt town bottoms', 'pleasure point', 'plumpton', 'point piper', 'port botany', 'port hacking', 'potts hill', 'potts point', 'prairiewood', 'prestons', 'prospect', 'punchbowl', 'putney', 'pymble', 'pyrmont', 'quakers hill', 'queens park', 'queenscliff', 'raby', 'ramsgate', 'ramsgate beach', 'randwick', 'redfern', 'regents park', 'regentville', 'revesby', 'revesby heights', 'rhodes', 'richmond', 'richmond lowlands', 'riverstone', 'riverview', 'riverwood', 'rockdale', 'rodd point', 'rookwood', 'rooty hill', 'ropes crossing', 'rose bay', 'rosebery', 'rosehill', 'roselands', 'rosemeadow', 'roseville', 'roseville chase', 'rossmore', 'rouse hill', 'royal national park', 'rozelle', 'ruse', 'rushcutters bay', 'russell lea', 'rydalmere', 'ryde', 'sackville', 'sackville north', 'sadleir', 'sandringham', 'sandy point', 'sans souci', 'scheyville', 'schofields', 'scotland island', 'seaforth', 'sefton', 'seven hills', 'shalvey', 'shanes park', 'silverwater', 'singletons mill', 'smeaton grange', 'smithfield', 'south coogee', 'south granville', 'south hurstville', 'south maroota', 'south penrith', 'south turramurra', 'south wentworthville', 'south windsor', 'spring farm', 'st andrews', 'st clair', 'st helens park', 'st ives', 'st ives chase', 'st johns park', 'st leonards', 'st marys', 'st peters', 'stanhope gardens', 'stanmore', 'strathfield', 'strathfield south', 'summer hill', 'surry hills', 'sutherland', 'sydenham', 'sydney olympic park', 'sylvania', 'sylvania waters', 'tamarama', 'taren point', 'telopea', 'tempe', 'tennyson', 'tennyson point', 'terrey hills', 'the ponds', 'the rocks', 'the slopes', 'thornleigh', 'toongabbie', 'tregear', 'turramurra', 'turrella', 'ultimo', 'varroville', 'vaucluse', 'villawood', 'vineyard', 'voyager point', 'wahroonga', 'waitara', 'wakeley', 'wallacia', 'wareemba', 'warrawee', 'warriewood', 'warwick farm', 'waterfall', 'waterloo', 'watsons bay', 'wattle grove', 'waverley', 'waverton', 'wedderburn', 'wentworth point', 'wentworthville', 'werrington', 'werrington county', 'werrington downs', 'west hoxton', 'west killara', 'west lindfield', 'west pennant hills', 'west pymble', 'west ryde', 'westleigh', 'westmead', 'wetherill park', 'whalan', 'whale beach', 'wheeler heights', 'wilberforce', 'wiley park', 'willmot', 'willoughby', 'willoughby east', 'windsor', 'windsor downs', 'winston hills', 'wisemans ferry', 'wolli creek', 'wollstonecraft', 'woodbine', 'woodcroft', 'woodpark', 'woollahra', 'woolloomooloo', 'woolooware', 'woolwich', 'woronora', 'woronora heights', 'yagoona', 'yarramundi', 'yarrawarrah', 'yennora', 'yowie bay', 'zetland'] 
    melb_suburbs = ['abbotsford', 'aberfeldie', 'aintree', 'airport west', 'albanvale', 'albert park', 'albion', 'alphington', 'altona meadows', 'altona north', 'altona', 'ardeer', 'armadale', 'ascot vale', 'ashburton', 'ashwood', 'aspendale gardens', 'aspendale', 'attwood', 'auburn', 'aurora', 'avondale heights', 'balaclava', 'balwyn north', 'balwyn', 'bayswater north', 'bayswater', 'beaconsfield', 'beaumaris', 'belgrave heights', 'belgrave south', 'belgrave', 'bellfield', 'bentleigh east', 'bentleigh', 'berwick', 'bittern', 'black rock', 'blackburn north', 'blackburn south', 'blackburn', 'blairgowrie', 'bonbeach', 'bonnie brook', 'boronia', 'box hill north', 'box hill south', 'box hill', 'braeside', 'braybrook', 'briar hill', 'brighton east', 'brighton', 'broadmeadows', 'brookfield', 'brooklyn', 'brunswick east', 'brunswick west', 'brunswick', 'bulleen', 'bundoora', 'burnley', 'burnside heights', 'burnside', 'burwood east', 'burwood', 'cairnlea', 'calder park', 'camberwell', 'campbellfield', 'canterbury', 'capel sound', 'carlton north', 'carlton', 'carnegie', 'caroline springs', 'carrum downs', 'carrum', 'caulfield east', 'caulfield north', 'caulfield south', 'caulfield', 'cbd', 'chadstone', 'chelsea heights', 'chelsea', 'cheltenham', 'chirnside park', 'clarinda', 'clayton south', 'clayton', 'clifton hill', 'clyde north', 'cobblebank', 'coburg north', 'coburg', 'collingwood', 'coolaroo', 'craigieburn', 'cranbourne east', 'cranbourne north', 'cranbourne west', 'cranbourne', 'cremorne', 'crib point', 'croydon hills', 'croydon north', 'croydon south', 'croydon', 'dallas', 'dandenong north', 'dandenong south', 'dandenong', 'deanside', 'deepdene', 'deer park', 'delahey', 'derrimut', 'diamond creek', 'diggers rest', 'dingley village', 'docklands', 'doncaster east', 'doncaster', 'donvale', 'doreen', 'doveton', 'dromana', 'eaglemont', 'east melbourne', 'edithvale', 'elsternwick', 'eltham north', 'eltham', 'elwood', 'emerald', 'endeavour hills', 'epping', 'essendon fields', 'essendon north', 'essendon west', 'essendon', 'eumemmerring', 'eynesbury', 'fairfield', 'fawkner', 'ferntree gully', 'fieldstone', 'fitzroy north', 'fitzroy', 'flemington', 'footscray', 'forest hill', 'frankston north', 'frankston south', 'frankston', 'fraser rise', 'garden city', 'gardenvale', 'gladstone park', 'glen huntly', 'glen iris', 'glen waverley', 'glenroy', 'gowanbrae', 'grangefields', 'greensborough', 'greenvale', 'hadfield', 'hallam', 'hampton east', 'hampton park', 'hampton', 'harkness', 'hastings', 'hawthorn east', 'hawthorn', 'heatherton', 'heathmont', 'heidelberg heights', 'heidelberg west', 'heidelberg', 'highett', 'hillside', 'hoppers crossing', 'hughesdale', 'huntingdale', 'hurstbridge', 'ivanhoe east', 'ivanhoe', 'jacana', 'junction village', 'kealba', 'keilor downs', 'keilor east', 'keilor lodge', 'keilor north', 'keilor park', 'keilor', 'kensington', 'kew east', 'kew', 'keysborough', 'kilsyth south', 'kilsyth', 'kings park', 'kingsbury', 'kingsville', 'knoxfield', 'kooyong', 'kurunjang', 'lalor', 'langwarrin', 'laverton north', 'laverton', 'lilydale', 'lower plenty', 'lynbrook', 'lyndhurst', 'lysterfield', 'mccrae', 'mckinnon', 'macleod', 'maidstone', 'malvern east', 'malvern', 'manor lakes', 'maribyrnong', 'meadow heights', 'melbourne airport', 'melton', 'melton south', 'melton west', 'melton', 'mentone', 'mernda', 'middle park', 'mill park', 'mitcham', 'monbulk', 'mont albert north', 'mont albert', 'montmorency', 'montrose', 'moonee ponds', 'moorabbin', 'moorooduc', 'mooroolbark', 'mordialloc', 'mornington', 'mount atkinson', 'mount eliza', 'mount evelyn', 'mount martha', 'mount waverley', 'mulgrave', 'murrumbeena', 'narre warren east', 'narre warren north', 'narre warren south', 'narre warren', 'newport', 'niddrie', 'noble park north', 'noble park', 'north melbourne', 'north warrandyte', 'northcote', 'notting hill', 'nunawading', 'oak park', 'oaklands junction', 'oakleigh east', 'oakleigh south', 'oakleigh', 'officer', 'olinda', 'ormond', 'pakenham', 'park orchards', 'parkdale', 'parkville', 'pascoe vale south', 'pascoe vale', 'the patch', 'patterson lakes', 'pearcedale', 'plumpton', 'point cook', 'port melbourne', 'portsea', 'prahran', 'preston', 'princes hill', 'research', 'reservoir', 'richmond', 'ringwood east', 'ringwood north', 'ringwood', 'ripponlea', 'rockbank', 'rosanna', 'rosebud', 'rowville', 'roxburgh park', 'rye', 'safety beach', 'st albans', 'st andrews beach', 'st helena', 'st kilda east', 'st kilda west', 'st kilda', 'sandhurst', 'sandringham', 'scoresby', 'seabrook', 'seaford', 'seaholme', 'seddon', 'selby', 'skye', 'somerton', 'somerville', 'sorrento', 'south kingsville', 'south melbourne', 'south morang', 'south wharf', 'south yarra', 'southbank', 'spotswood', 'springvale south', 'springvale', 'strathmore heights', 'strathmore', 'strathtulloh', 'sunbury', 'sunshine north', 'sunshine west', 'sunshine', 'surrey hills', 'sydenham', 'tarneit plains', 'tarneit', 'taylors hill', 'taylors lakes', 'tecoma', 'templestowe lower', 'templestowe', 'the basin', 'thomastown', 'thornbury', 'thornhill park', 'toorak', 'tootgarook', 'tottenham', 'travancore', 'truganina', 'tullamarine', 'tyabb', 'upfield', 'upper ferntree gully', 'upwey', 'vermont south', 'vermont', 'viewbank', 'wantirna south', 'wantirna', 'warrandyte', 'warranwood', 'waterways', 'watsonia north', 'watsonia', 'wattle glen', 'weir views', 'werribee south', 'werribee', 'west footscray', 'west melbourne', 'westmeadows', 'wheelers hill', 'williams landing', 'williamstown north', 'williamstown', 'windsor', 'wollert', 'wyndham vale', 'yallambie', 'yarraville']

    IMAP_SERVER = 'imap.gmail.com'
    EMAIL_ACCOUNT = "maxawzsinger@gmail.com" #email subscribed to group email notifs
    EMAIL_FOLDER = "[Gmail]/Starred" #set gmail up to star mail in houemates post folder and then unstar and delete after 1 day as idk how to do this in python (code not working)
    PASSWORD = 'tgqkxgwypxisbgpp' #email password - generated from google app passwords (2fa)
    new_data = [] # holds list of dictionaries, to be exported to csv

    my_house = [] #looking for good houses for my own personal search
    error_data = [] #holds posts w error in processing
    uid_list = [] #holds UIDs of processed emails to be marked for deletion
    for_website = [] #holds bare minimum info for website
    M = imaplib.IMAP4_SSL(IMAP_SERVER)
    M.login(EMAIL_ACCOUNT, PASSWORD)
    rv, data = M.select(EMAIL_FOLDER)
    melb_sub_price = {} #holds just suburb and price of room for the website (melb)
    syd_sub_price = {}

    rv, data = M.search(None, "ALL")
    if rv == 'OK':
        print("Processing mailbox: ", EMAIL_FOLDER)  
        for num in data[0].split(): #list of uid emails
            rv, data = M.fetch(num, '(RFC822)')
            if rv != 'OK':
                print("ERROR getting message", num)
            #Parsing:
            raw_email_string = data[0][1].decode('utf-8')
            msg = email.message_from_string(raw_email_string)

            new_dict={} #to hold each email's data

            #TIME OF POST
            time = msg['Date']
            #new_dict['Time'] = datetime.strptime(time,"%a, %d %B %Y %X	")
            new_dict['Time'] = time[:-15]

        
            #GROUP ID NAME

            group_name = msg['To']        
            new_dict['Group'] = str(group_name)

            #REGEX EXTRACTION:

            #URL
        
            urlstring = re.findall(r'(?<=View on Facebook)(.*)(?=Edit Email Settings)',raw_email_string, flags=re.DOTALL) #re.DOTALL makes . match all characters inc. newline... this all returns a list of occurences
            if len(urlstring) > 0:
                try:
                    urlstring = urlstring[0]
                    #FIND GROUP ID NUMBER
                    group_id= re.findall(r'(?<=www\.facebook\.com\/nd\/\?groups%2F)(.*)(?=%2Fpermalink%)', urlstring, flags = re.DOTALL)
                    if len(group_id) > 0:
                        group_id_string = group_id[0]
                        #FIND POST ID NUMBER
                        post_id= re.findall(r'(?<=%2Fpermalink%2F)(.*)(?=%2F)', urlstring, flags = re.DOTALL)
                        if len(post_id) > 0:
                            post_id_string_rough = post_id[0]
                            post_id_string = re.sub('=\\n', '', post_id_string_rough, count=0, flags=0)
                            post_id_string = re.sub('=', '', post_id_string, count=0, flags=0)
                            #ADD TOGETHER TO FORM URL
                            final_url_string = 'https://www.facebook.com/groups/'+group_id_string+'/permalink/'+post_id_string
                            new_dict['URL'] = final_url_string
                            new_dict['URL'] = new_dict['URL'].replace('\r','') #getting rid of newline 
                            new_dict['URL'] = new_dict['URL'].replace('\n','') #getting rid of newline 
                except:
                    new_dict['URL'] = 'Error'
            else:
                new_dict['URL'] = 'Error'

            #PHOTO HTML TEXT
            try:
                photo_html = re.findall(r'(?<=<img src=3D)(.{150})', raw_email_string, flags = re.DOTALL)
                new_dict['Photo Html'] = photo_html
            except:
                new_dict['Photo Html'] = 'Error'
            #TITLE
        
            title = re.findall(r'(?<=\d\d\d\d\d\d;">)(.*)\s?(.*?)(?=<br)', raw_email_string, flags = 0)
            if len(title) > 0:
                try:
                    tuple = title[0]
                    if len(tuple) > 1:
                        new_dict['Title'] = tuple[0] + tuple[1]
                        new_dict['Title'] = new_dict['Title'].replace('=','')
                        new_dict['Title'] = new_dict['Title'].replace('\n','')
                        new_dict['Title'] = new_dict['Title'].replace('\r','')
                        new_dict['Title'] = new_dict['Title'].lower()
                        new_dict['Title'] = str(new_dict['Title'])

                    else:
                        new_dict['Title'] = tuple[0].replace('=','')
                        new_dict['Title'] = new_dict['Title'].replace('\n','')
                        new_dict['Title'] = new_dict['Title'].replace('\r','')
                        new_dict['Title'] = new_dict['Title'].lower()
                        new_dict['Title'] = str(new_dict['Title'])         
                except:
                    new_dict['Title'] = 'Error'
            else:
                new_dict['Title'] = 'Error'

        
            #POST TEXT

            post_text = re.findall(r'(?<=Hi Max,)(.*)(?=This message was sent to)', raw_email_string, flags = re.DOTALL)
            if len(post_text) > 0:
                try:
                    post_text_string_rough = post_text[0]
                    new_dict['Post Text'] = post_text_string_rough.lower()
                    new_dict['Post Text'] = new_dict['Post Text'].replace('\r\n\r\n','. ') #getting rid of newline 
                    new_dict['Post Text'] = new_dict['Post Text'].replace('\r',' ') #getting rid of newline 
                    new_dict['Post Text'] = new_dict['Post Text'].replace('\n','') #getting rid of newlines
                    new_dict['Post Text'] = new_dict['Post Text'].replace('=20','') #getting rid of newlines
                    new_dict['Post Text'] = new_dict['Post Text'].replace('=3D','') #getting rid of newlines
                    new_dict['Post Text'] = new_dict['Post Text'].replace('=','') #getting rid of newlines
                    new_dict['Post Text'] = new_dict['Post Text'].replace('  ',' ') #getting rid of newlines
                    new_dict['Post Text'] = new_dict['Post Text'].replace('  ',' ') #getting rid of newlines
                    new_dict['Post Text'] = new_dict['Post Text'].replace('  ',' ') #getting rid of newlines
                    new_dict['Post Text'] = new_dict['Post Text'].replace('..','.') #getting rid of newlines
                    new_dict['Post Text'] = new_dict['Post Text'].strip('\.')
                    new_dict['Post Text'] = new_dict['Post Text'].strip('\. ')
                    new_dict['Post Text'] = new_dict['Post Text'].strip()
                    new_dict['Post Text'] = new_dict['Post Text'].strip('\"')
                    new_dict['Post Text'] = re.sub(r'E\d{5}', '\'', new_dict['Post Text'], count=0, flags=0)
                    #still not removing emojis e.g. f09f988a
                    ## add in regex expression looking for [puncitonar marks] {2,} replace with just . ?
                    #doesn't account for repeated posts
                except:
                    new_dict['Post Text'] = 'Error'
            else:
                new_dict['Post Text'] = 'Error'

            

            #PRICE GUESS 

            new_dict['Per Week Guess'] = 'Error'
 
            price_flags = ['week','pw','/week','p/w','pm','pcm','month','/month','p/m']
            guess_phrase_one = re.search(r'(\w+)?(\s+)?(\w+)?(\s+)?(\w+)?(\s+)?(\$\d,?\d\d\d?\.?\d?\d?)', new_dict['Post Text'], flags = 0) #regex phrase finds money amount plus following three words, stopping at punctuation.
            if guess_phrase_one != None:
                try:
                    guess_phrase_one = guess_phrase_one.group()
                    for flag in price_flags:
                        if flag in guess_phrase_one:
                            price_guessed = re.search(r'(\$\d,?\d\d\d?\.?\d?\d?)', guess_phrase_one, flags = 0) #importantly only with $sign preceding so doesnt get any other digits accidentally collected
                            if price_guessed != None:
                                try:
                                    price_guessed = price_guessed.group()
                                    price_guessed = price_guessed.replace('$','')
                                    price_guessed = price_guessed.replace(',','')
                                    if flag in ('week','pw','/week','p/w'):
                                        try:
                                            new_dict['Per Week Guess'] = float(price_guessed)
                                        except:
                                            new_dict['Per Week Guess'] = 'Error'
                                    else:
                                        try:
                                            month_guessed = float(price_guessed)
                                            new_dict['Per Week Guess'] = month_guessed * 12 / 52
                                        except:
                                            new_dict['Per Week Guess'] = 'Error'

                                except:
                                    new_dict['Per Week Guess'] = 'Error'
                except:
                    new_dict['Per Week Guess'] = 'Error'



            guess_phrase_two = re.search(r'(\$\d,?\d\d\d?\.?\d?\d?)(\s+)?(\/?)(\w+)?(\/?)(\s+)?(\w+)?(\s+)?(\w+)?', new_dict['Post Text'], flags = 0) #regex phrase finds money amount with preceding three words stopping at punctuation
            if guess_phrase_two != None and new_dict['Per Week Guess'] == 'Error':
                try:
                    guess_phrase_two = guess_phrase_two.group()
                    for flag in price_flags:
                        if flag in guess_phrase_two:
                            price_guessed = re.search(r'(\$\d,?\d\d\d?\.?\d?\d?)', guess_phrase_two, flags = 0) #importantly only with $sign preceding so doesnt get any other digits accidentally collected
                            if price_guessed != None:
                                try:
                                    price_guessed = price_guessed.group()
                                    price_guessed = price_guessed.replace('$','')
                                    price_guessed = price_guessed.replace(',','')
                                    if flag in ('week','pw','/week','p/w'):
                                        try:
                                            new_dict['Per Week Guess'] = float(price_guessed)
                                        except:
                                            new_dict['Per Week Guess'] = 'Error'
                                    else:
                                        try:
                                            month_guessed = float(price_guessed)
                                            new_dict['Per Week Guess'] = month_guessed * 12 / 52
                                        except:
                                            new_dict['Per Week Guess'] = 'Error'
                                except:
                                    new_dict['Per Week Guess'] = 'Error'
                except:
                    new_dict['Per Week Guess'] = 'Error'
            if new_dict['Per Week Guess'] == 'Error':
                #price_text = re.search(r'(?<=<br \/> )(\$.*)(?= =E2=80=93)', raw_email_string, flags = re.DOTALL) #this regex finds price in facebook title
                price_text = re.search(r'(\$\d\d\d\d?)', raw_email_string, flags = re.DOTALL) #this regex finds price in facebook title
                if price_text!= None:
                    try:
                        price_text = price_text.group()
                        price_text = price_text.replace('$','')
                        price_text = price_text.replace(',','')
                        price = float(price_text)
                        if price > 500:
                            try:
                                new_dict['Per Week Guess'] = price * 12 / 52
                            except:
                                new_dict['Per Week Guess'] = 'Error'
                        else:
                            try:
                                new_dict['Per Week Guess'] = price
                            except:
                                new_dict['Per Week Guess'] = 'Error'
                    except:
                        new_dict['Per Week Guess'] = 'Error'

            if type(new_dict['Per Week Guess']) == float:
                if new_dict['Per Week Guess'] > 400:
                    new_dict['Per Week Guess'] = 'Error'
                elif new_dict['Per Week Guess'] < 100:
                    new_dict['Per Week Guess'] = 'Error'

        
            #SUBURB GUESS
            sub_count = []
            sub_post = []
            vic_flags = ['Fairy Floss Real Estate']
            nsw_flags = ['Inner West Housemates']
            new_dict['Suburb Guess'] = 'Error'
            join_text = new_dict['Title'] + new_dict['Post Text']
            splitted = re.split(r'\W+', join_text)



            for flag in vic_flags:
                if flag in group_name:
                    state = 'VIC'

            for flag in nsw_flags:
                if flag in group_name:
                    state = 'NSW'


            if state == 'VIC':
                for suburb in melb_suburbs:
                    if suburb in new_dict['Title']:
                        try:
                            sub_count.append(suburb)
                            new_dict['Suburb Guess'] = max(sub_count, key=len)
                        except:
                            new_dict['Suburb Guess'] = 'Error'

                    elif suburb in new_dict['Post Text']:
                        try:
                            sub_post.append(suburb)
                            new_dict['Suburb Guess'] = max(sub_post, key=len)
                        except:
                            new_dict['Suburb Guess'] = 'Error'
            if state == 'NSW':
                for suburb in syd_suburbs:
                    if suburb in new_dict['Title']:
                        try:
                            sub_count.append(suburb)
                            new_dict['Suburb Guess'] = max(sub_count, key=len)
                            break
                        except:
                            new_dict['Suburb Guess'] = 'Error'
                            break

                    elif suburb in new_dict['Post Text']:
                        try:
                            sub_post.append(suburb)
                            new_dict['Suburb Guess'] = max(sub_post, key=len)
                            break
                        except:
                            new_dict['Suburb Guess'] = 'Error'
                            break    

            if state == 'NSW':
                for word in splitted:
                    if word in syd_suburbs:
                        new_dict['Suburb Guess'] = word
                        break

            if state == 'VIC':
                for word in splitted:
                    if word in melb_suburbs:
                        new_dict['Suburb Guess'] = word
                        break




            #POSTER TEXT (NOT WORKING)
            #poster_regex = r'(?<=Subject:)(.*)(?=posted)' #not working?
            #poster = re.findall(poster_regex, raw_email_string, flags = 0) #not working?
            #poster_string = str(poster[0]).strip() #throws error index out of range probably because if nothing found the list will be empty
            #new_dict['Post Text'] = re.sub(r'[?/><;:~!@#$%^&*()\-+=\.]{2,}', '.', new_dict['Post Text'], count=0, flags=0)
            #new_dict['Poster'] = poster_string #not working due to above
            
            #adding to suburb and price dictionary:
            
            if new_dict['Per Week Guess'] == 'Error' or new_dict['Suburb Guess'] == 'Error':
                error_data.append(new_dict)
            #APPENDING DICIONARY TO LIST OF DICTIONARIES
            
            else:
                new_data.append(new_dict) #for records
                suburb_bare = new_dict['Suburb Guess'].replace(' ','_')
                price_bare = new_dict['Per Week Guess']
                if state == 'VIC':
                    if suburb_bare not in melb_sub_price:
                        melb_sub_price[suburb_bare] = [price_bare, 1]
                    else:
                        #melb_sub_price[suburb_bare]= list(map(add, melb_sub_price[suburb_bare], [price_bare, 1])) #also works as below
                        #tried to make it faster with just below code
                        melb_list = melb_sub_price[suburb_bare]
                        melb_list[0] = melb_list[0] + price_bare
                        melb_list[1] = melb_list[1] + 1
                        melb_sub_price[suburb_bare] = melb_list
                        
                elif state == 'NSW':
                    if suburb_bare not in syd_sub_price:
                        syd_sub_price[suburb_bare] = [price_bare, 1]
                    else:
                        #syd_sub_price[suburb_bare] = list(map(add, syd_sub_price[suburb_bare], [price_bare, 1])) #trying to store amounts to be averaged out later per suburb...
                        # https://stackoverflow.com/questions/18713321/element-wise-addition-of-2-lists
                        syd_list = syd_sub_price[suburb_bare]
                        syd_list[0] = syd_list[0] + price_bare
                        syd_list[1] = syd_list[1] + 1
                        syd_sub_price[suburb_bare] = syd_list
            
            #Calculating city avgs
            syd_total = 0
            syd_total_count = 0
            if len(syd_sub_price) > 0: 
                for suburb in syd_sub_price:
                    price_list = syd_sub_price[suburb]
                    syd_total += price_list[0]
                    syd_total_count += price_list[1]
                syd_avg = syd_total/syd_total_count
            
            melb_total = 0
            melb_total_count = 0
            if len(melb_sub_price) > 0:
                for suburb in melb_sub_price:
                    price_list = melb_sub_price[suburb]
                    melb_total += price_list[0]
                    melb_total_count += price_list[1]
                melb_avg = melb_total/melb_total_count
                
                
                
            #for my own hosue-hunting:
            if new_dict['Suburb Guess'] == 'surry hills':
                my_house.append(new_dict)

            keywords = ['tram','light rail','dove','unsw']
            
            if state == 'NSW':
                for key in keywords:
                    if key in new_dict['Post Text']:
                        my_house.append(new_dict)
                        break
                    elif key in new_dict['Title']:
                        my_house.append(new_dict)
                        break
                            
                

            #APPENDING EMAIL UID TO LIST OF UIDs 

            email_id = num.decode('utf-8')
            uid_list.append(email_id)#adds email ids for deletion after processing
            print('processing email'+ email_id)
            #print(new_data) #prints list holding a dictionary for each email procesed. to be sent to a csv
        timenow = datetime.datetime.now()
        time_string = timenow.strftime('%d%b%y')
        filename = 'housemates'+time_string+'.csv' #create informative file name
        ####################### my personal house search
        melb_avgs_error_count = 0
        if len(melb_sub_price) > 0: #AVERAGING OUT COUNTS OF PLACES FOR EACH SUBURB
            for suburb in melb_sub_price:
                price_info = melb_sub_price[suburb]
                try:
                    melb_sub_price[suburb] = price_info[0] / price_info[1]
                except:
                    melb_avgs_error_count += 1

            melb_sub_price['melb_avg'] = melb_avg
            print(melb_avgs_error_count)
            s3 = boto3.resource('s3') #boto is aws python sdk
            bucket = s3.Bucket('roomsortdata')
            key = 'melb'+time_string+'.csv'
            #with open(filename, 'w') as output_file:
            #dict_writer = csv.DictWriter(output_file, keys)
            #dict_writer.writeheader()
            #dict_writer.writerows(new_data)
            file_tmp = '/tmp/' + key
        
            with open(file_tmp, 'w') as f:
                w = csv.writer(f)
                w.writerows(melb_sub_price.items())
            #upload the data into s3
            bucket.upload_file(file_tmp, key)
        #####################
        syd_avgs_error_count = 0
        if len(syd_sub_price) > 0:
            for suburb in syd_sub_price:
                price_info = syd_sub_price[suburb]
                try:
                    syd_sub_price[suburb] = price_info[0] / price_info[1]
                except:
                    syd_avgs_error_count += 1
    
            syd_sub_price['syd_avg'] = syd_avg
            print(syd_avgs_error_count)
            s3 = boto3.resource('s3') #boto is aws python sdk
            bucket = s3.Bucket('roomsortdata')
            key = 'syd'+time_string+'.csv'
            #with open(filename, 'w') as output_file:
            #dict_writer = csv.DictWriter(output_file, keys)
            #dict_writer.writeheader()
            #dict_writer.writerows(new_data)
            file_tmp = '/tmp/' + key

            with open(file_tmp, 'w') as f:
                w = csv.writer(f)
                w.writerows(syd_sub_price.items())
            #upload the data into s3
            bucket.upload_file(file_tmp, key)
        #####################
        
        
        
        if len(my_house) > 0: #will not go through if messages already deleted, no more messages
            keys = my_house[0].keys()
            s3 = boto3.resource('s3') #boto is aws python sdk
            bucket = s3.Bucket('roomsortdata')
            key = 'houseoptions'+time_string+'.csv'
            #with open(filename, 'w') as output_file:
            #dict_writer = csv.DictWriter(output_file, keys)
            #dict_writer.writeheader()
            #dict_writer.writerows(new_data)
            file_tmp = '/tmp/' + key
        
            with open(file_tmp, 'w', newline='') as f:
                w = csv.DictWriter(f, keys)
                w.writeheader()
                #fieldnames=['Time','Group URL','Photo Html','Title', 'Post Text','Per Week Guess','Suburb Guess','Suburb Guess 2']
                w.writerows(my_house)
            #upload the data into s3
            bucket.upload_file(file_tmp, key)
        ##################### printing error log
        if len(error_data) > 0: #will not go through if messages already deleted, no more messages
            keys = error_data[0].keys()
            s3 = boto3.resource('s3') #boto is aws python sdk
            bucket = s3.Bucket('roomsortdata')
            key = 'errors'+time_string+'.csv'
            #with open(filename, 'w') as output_file:
            #dict_writer = csv.DictWriter(output_file, keys)
            #dict_writer.writeheader()
            #dict_writer.writerows(new_data)
            file_tmp = '/tmp/' + key
        
            with open(file_tmp, 'w', newline='') as f:
                w = csv.DictWriter(f, keys)
                w.writeheader()
                #fieldnames=['Time','Group URL','Photo Html','Title', 'Post Text','Per Week Guess','Suburb Guess','Suburb Guess 2']
                w.writerows(error_data)
            #upload the data into s3
            bucket.upload_file(file_tmp, key)
        #####################
        
        if len(new_data) > 0: #will not go through if messages already deleted, no more messages
            keys = new_data[0].keys()
            s3 = boto3.resource('s3') #boto is aws python sdk
            bucket = s3.Bucket('roomsortdata')
            key = filename
        #with open(filename, 'w') as output_file:
            #dict_writer = csv.DictWriter(output_file, keys)
            #dict_writer.writeheader()
            #dict_writer.writerows(new_data)
            file_tmp = '/tmp/' + filename
        
            with open(file_tmp, 'w', newline='') as f:
                w = csv.DictWriter(f, keys)
                w.writeheader()
                #fieldnames=['Time','Group URL','Photo Html','Title', 'Post Text','Per Week Guess','Suburb Guess','Suburb Guess 2']
                w.writerows(new_data)
            #upload the data into s3
            bucket.upload_file(file_tmp, key)
        else:
            s3 = boto3.resource('s3') #boto is aws python sdk
            bucket = s3.Bucket('roomsortdata')
            empty_dict = {'Empty':'Empty'}
            print('No Messages Today')
            with open('/tmp/' + time_string +'empty.csv', 'w', newline='') as f:
                w = csv.writer(f)
                w.writerows(empty_dict)
                #upload the data into s3
            bucket.upload_file('/tmp/' + time_string +'empty.csv', time_string +'empty.csv') #adds an empty csv for website asking for it
            

        uid_list_string  = ','.join(uid_list)
        #working out averages per suburb for the day:
        melb_sub_price_final = {}
        #for entry in melb_sub_price:
            #if entry[0] in melb_sub_price_final:
                
            
        try:
            M.store(uid_list_string, '+FLAGS', '(\Deleted)')   #marks emails that have been processed to be deleted
            M.expunge() #deletes marked emails
            print('Deleted Successfully')
        except:
            print('No more messages') 

            #uncomment above for deleting after being processed
        M.close()
        
    elif rv != 'OK':
        print("No messages found!")
    else:
        print("ERROR: Unable to open mailbox ", rv)
    M.logout()
