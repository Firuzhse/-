# Import libraries
from PIL import Image
import pytesseract
import sys
from pdf2image import convert_from_path
import os
import scandir
import hashlib
import mysql.connector
import io

pytesseract.pytesseract.tesseract_cmd = r"C:\Program Files\Tesseract-OCR\tesseract.exe"

TMP = "tmps/"


def recognyze_pdf(PDF_file):
    global TMP
    global PATH
    

    PDF_file = PATH + PDF_file # absolute path
    print("reading " + PDF_file)

    
    #get pdf pages count
    pdf = PdfFileReader(open( PDF_file ,'rb'))
    maxPages = pdf.getNumPages()
    print( "pages cnt " , maxPages )
    
    content = ""
    #pages = convert_from_path(PDF_file) 

    for page in range(1 , maxPages , 10) : 
        pages = convert_from_path(PDF_file, dpi=200, first_page=page, last_page = min(page + 10 - 1 , maxPages)) 
        
        image_counter = 1
        
        for x in pages:
            filename = TMP + "page_" + str(image_counter) + ".jpg"
            x.save(filename, 'JPEG')
            image_counter = image_counter + 1

        filelimit = image_counter - 1
        
        for i in range(1, filelimit + 1):
            filename = TMP + "page_" + str(i) + ".jpg"
            text = str(((pytesseract.image_to_string(Image.open(filename), lang='deu'))))
            print("recognizing " + filename)
            text = text.replace('-\n', '')  # perenos stroki udalit
            content += text
            print("removing " + filename)
            os.remove(filename)
    
    return content

def get_hash( file ):
    BLOCKSIZE = 65536
    hasher = hashlib.sha1()
    with open( file, 'rb' ) as afile:
        buf = afile.read( BLOCKSIZE )
        while len( buf ) > 0:
            hasher.update( buf )
            buf = afile.read( BLOCKSIZE )
    return hasher.hexdigest()

def insert_into_db( ext, path, content, size, hashmac ):
    global host
    global user
    global password
    global database
    ext = ext.lower() # check it
    conn = mysql.connector.connect( host = host, user = user , password = password , database = database )
    cursor = conn.cursor()
    sql = "INSERT INTO files (ext, path, keywords, size, hashmac) VALUES (%s, %s, %s, %s, %s)"
    val = ( ext, path, content, size, hashmac)
    cursor.execute( sql, val )
    conn.commit()
    cursor.close()
    conn.close()

def insert_damaged_file_db( ext, path, content, size, hashmac ):
    global host
    global user
    global password
    global database
    conn = mysql.connector.connect( host = host, user = user , password = password , database = database )
    cursor = conn.cursor()
    sql = "INSERT INTO damaged_files (ext, path, keywords, size, hashmac) VALUES (%s, %s, %s, %s, %s)"
    val = ( ext, path, content, size, hashmac)
    cursor.execute( sql, val )
    conn.commit()
    cursor.close()
    conn.close()

def change_slash( path ):
    s = list( path )
    N = len( path )
    while N > 0:
        if ord( s[N-1] ) == 92:
            s[N-1] = "/"
        N -= 1
    s = "".join(s)
    return s

def get_all_pdf_files():
    conn = mysql.connector.connect( host = "192.168.222.11", user = "xzizt" , password = "hamatagom" , database = "mede_db" )
    cursor = conn.cursor()
    cursor.execute( "SELECT file_id, path FROM files where ext = 'pdf' and scanned = '0' and del = 0 limit 1000" )
    res = cursor.fetchall()
    cursor.close()
    conn.close()
    return res

def run_pdf_rec():
    pdfs = get_all_pdf_files()

    for pdf in pdfs:
        print( pdf[0] , " " , pdf[1])
        #print( recognyze_pdf(  pdf[1] ) )
        try:
            insert_keywords( pdf[0], recognyze_pdf(  pdf[1] ) )
        except:
            insert_recognation_error( pdf[0] )
            continue


path = 'X:'
#path = 'X:\Furkan Gürlek'
cnt = 0
for root, dirs, files in os.walk( path ):
    for _file in files:
        curr_file = os.path.join(root, _file)
        
        #print( curr_file ) 
        #print( change_slash( curr_file ) ) 

        try:
            size = os.stat( curr_file ).st_size
            hashmac = get_hash( curr_file )
        
            content = ""
            
            extension = os.path.splitext(_file)[1]
            extension = extension[1:]
            curr_file = curr_file[2:] # path without X:
            # files size

            
            insert_into_db( extension, change_slash( curr_file ), content, size, hashmac )
            cnt += 1
            #print( cnt, " record inserted" )
        except:
            insert_damaged_file_db( "extension", change_slash( curr_file ), "content", 0, "hashmac" )
            #print( "damaged file inserted >> " + curr_file )
            continue

        
        
print( "DONE" )



