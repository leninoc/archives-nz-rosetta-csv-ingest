import sys
from datetime import datetime
sys.path.append(r'JsonTableSchema/')
import JsonTableSchema
import ConfigParser
import argparse
import csv

class ImportSheetGenerator:

   def __init__(self):
      config = ConfigParser.RawConfigParser()
      self.config = config.read('import-value-mapping.cfg')   

      self.droidcsv = False
      self.importschema = False

   def __init__(self, droidcsv=False, importschema=False):
      self.configfilename = 'import-value-mapping.cfg'
      self.droidcsv = droidcsv
      self.importschema = importschema

   def retrieve_year_from_modified_date(self, MODIFIED_DATE):

      inputdateformat = '%Y-%m-%dT%H:%M:%S'
      moddate = datetime.strptime(MODIFIED_DATE, inputdateformat)
      return moddate.year

   def maptoimportschema(self):
      
      if self.importschema != False:
         f = open(self.importschema, 'rb')
         
         importschemajson = f.read()

         importschema = JsonTableSchema.JSONTableSchema(importschemajson)
         importschemadict = importschema.as_dict()
         importschemaheader = importschema.as_csv_header()

         #for column in importschemadict['fields']:
         #   print column

         #for row in DROID CSV...
            #for column in schema...

            #for column in importschemadict['fields']:
            #   if config.has_option('droid mapping', column['name']):
            #      print "xxx: " + config.get('droid mapping', column['name'])
                  
            #   if config.has_option('static values', column['name']):
            #      print "yyy: " + config.get('static values', column['name'])
                  
            #   if column['name'] == 'Description':       #TODO: More dynamic in config file?
            #      if config.has_option('additional values', 'descriptiontext'):
            #         print config.get('additional values', 'descriptiontext')

               # TODO: search DROID CSV string for MODIFIED_DATE strip all but year
               # input here...
            #   if column['name'] == 'Open Year':  
            #      temp1 = str(retrieve_year_from_modified_date('2006-03-10T14:31:49'))

            #   if column['name'] == 'Close Year':  
            #      temp2 = str(retrieve_year_from_modified_date('2007-03-10T14:31:49'))

   def getDROIDHeaders(self, csvcolumnheaders):
      header_list = []
      for header in csvcolumnheaders:      
         header_list.append(header)
      return header_list

   def removefolders(self, droid_list):
      #TODO: We can generate counts here and store in member vars
      for row in droid_list:
         if row['TYPE'] == 'Folder':
            droid_list.remove(row)
      return droid_list

   def readDROIDCSV(self):
      if self.droidcsv != False:
         droid_list = []

         with open(self.droidcsv, 'rb') as csvfile:
            droidreader = csv.reader(csvfile)
            for row in droidreader:      
               if droidreader.line_num == 1:		# not zero-based index
                  header_list = self.getDROIDHeaders(row)
               else:
                  droid_dict = {}
                  for i,item in enumerate(row):
                     droid_dict[header_list[i]] = item
                     # get URI Scheme: urlparse(url).scheme
                     # get DIRNAME os.path.dirname(item)
                     
                  droid_list.append(droid_dict)
         
         return droid_list

   def droid2archwayimport(self):
      if self.droidcsv != False and self.importschema != False:
         droidlist = self.readDROIDCSV()
         droidlist = self.removefolders(droidlist)
         self.maptoimportschema()

def importsheetDROIDmapping(droidcsv, importschema):
   importgenerator = ImportSheetGenerator(droidcsv, importschema)
   importgenerator.droid2archwayimport()

def main():

   #	Usage: 	--csv [droid report]

   #	Handle command line arguments for the script
   parser = argparse.ArgumentParser(description='Generate Archway Import Sheet and Rosetta Ingest CSV from DROID CSV Reports.')

   #TODO: Consider optional and mandatory elements... behaviour might change depending on output...
   #other options droid csv and rosetta schema
   #NOTE: class on its own might be used to create a blank import csv with just static options
   parser.add_argument('--csv', help='Single DROID CSV to read.', default=False, required=False)
   parser.add_argument('--imp', help='Archway import schema to use.', default=False, required=False)

   if len(sys.argv)==1:
      parser.print_help()
      sys.exit(1)

   #	Parse arguments into namespace object to reference later in the script
   global args
   args = parser.parse_args()
   
   if args.csv and args.imp:
      importsheetDROIDmapping(args.csv, args.imp)
   
   else:
      sys.exit(1)

if __name__ == "__main__":
   main()




'''
f = open('import-csv-schema.json', 'rb')
test = f.read()

ross = JsonTableSchema.JSONTableSchema(test)

rs = ross.as_dict()

for x in rs['fields']:
   print x['name']'''
   
   # TODO: Read mapping Config file... 
   # TODO: Read values config file...
   # TODO: For each matching field, import data, else, blank cell

   # get URI Scheme: urlparse(url).scheme
   # get DIRNAME os.path.dirname(item)

#sys.stdout.write(ross.as_csv_header())