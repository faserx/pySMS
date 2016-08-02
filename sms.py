#!/usr/bin/python3
import re
import socket
import urllib, urllib.error
import http.client
import sys

def sendSMS(mittente, destinatario, testo, pincode):
  try:
    if(not(re.compile(re.escape('+39')).search(destinatario))):
      destinatario = "+39"+destinatario
    conn = http.client.HTTPConnection('www.smsgang.com');
    headers = { "Accept": "text/html,application/xhtml+xml,application/xml;q=0.9,*/*;q=0.8",
                "Content-type": "application/x-www-form-urlencoded; charset=UTF-8" }
    params = urllib.parse.urlencode({
      "tonumber":destinatario,
      "senderid":mittente,
      "iso_msg":testo,
      "pincode":pincode,
      "B2":"Send SMS",
      "unicode_msg":""
    })
    conn.request('POST', '/sendsms.php?langfile=en', params, headers)
    response = conn.getresponse();

    if(response.status == 200 and re.compile(b'Your SMS was sent').search(response.read())):
      print("SMS mandato con successo\n")
      conn.close()
    else:
      print( "Errore: impossibile mandare l'SMS")
      print(response.status, response.reason)
      print(response)
      conn.close()
  except urllib.error.HTTPError as e:
    print("HTTPError: ", e.code())
    conn.close()
  except Exception as e:
    conn.close()
    print("Exception: ", sys.exc_info()[0])
    raise

def usage():
  print ("Usage:\n")
  print ("\tsms.py <mittente> (+39)<destinatario> <testo> <pin>\n")
  
if(len(sys.argv) < 3):
  usage()
else:
  sendSMS(sys.argv[0], sys.argv[1], sys.argv[2], sys.argv[3])