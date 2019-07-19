#!/usr/bin/env python3

import psycopg2, json, os, datetime, requests, slack, smtplib, csv, logging
from jira.client import JIRA
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart
from defectdojo_api import defectdojo

File_Dir = os.path.dirname(os.path.realpath('__file__'))
Configuration_File = os.path.join(File_Dir, 'plugins/common/configuration/config.json')

def Load_CSV_Configuration():
    logging.info(str(datetime.datetime.now()) + " Loading CSV configuration data.")

    try:
        with open(Configuration_File) as JSON_File:
            Configuration_Data = json.load(JSON_File)

        for CSV_Details in Configuration_Data['csv']:
            Use_CSV = CSV_Details['use-csv']
            return Use_CSV

    except Exception as e:
        logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Load_Defect_Dojo_Configuration():
    logging.info(str(datetime.datetime.now()) + " Loading DefectDojo configuration data.")

    try:
        with open(Configuration_File) as JSON_File:
            Configuration_Data = json.load(JSON_File)

        for DD_Details in Configuration_Data['defectdojo']:
            DD_API_Key = DD_Details['api_key']
            DD_Host = DD_Details['host']
            DD_User = DD_Details['user']
            DD_Engagement_ID = DD_Details['engagement-id']
            DD_Product_ID = DD_Details['product-id']
            DD_Test_ID = DD_Details['test-id']
            DD_User_ID = DD_Details['user-id']

        if DD_API_Key and DD_Host and DD_User and DD_Engagement_ID and DD_Product_ID and DD_Test_ID and DD_User_ID:
            Use_DD = True

        else:
            Use_DD = False

        return [DD_API_Key, DD_Host, DD_User, DD_Engagement_ID, DD_Product_ID, DD_Test_ID, DD_User_ID, Use_DD]

    except Exception as e:
        logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Load_Email_Configuration():
    logging.info(str(datetime.datetime.now()) + " Loading email configuration data.")

    try:
        with open(Configuration_File) as JSON_File:
            Configuration_Data = json.load(JSON_File)

        for Email_Details in Configuration_Data['email']:
            Email_SMTP_Server = Email_Details['smtp_server']
            Email_SMTP_Port = int(Email_Details['smtp_port'])
            Email_From_Address = Email_Details['from_address']
            Email_From_Password = Email_Details['from_password']
            Email_To_Address = Email_Details['to_address']

        if Email_SMTP_Server and Email_SMTP_Port and Email_From_Address and Email_From_Password and Email_To_Address:
            Use_Email = True

        else:
            Use_Email = False

        return [Email_SMTP_Server, Email_SMTP_Port, Email_From_Address, Email_From_Password, Email_To_Address, Use_Email]

    except Exception as e:
        logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Load_Elasticsearch_Configuration():
    logging.info(str(datetime.datetime.now()) + " Loading Elasticsearch configuration data.")

    try:
        with open(Configuration_File) as JSON_File:
            Configuration_Data = json.load(JSON_File)

        for Elasticsearch_Details in Configuration_Data['elasticsearch']:
            Elasticsearch_Service = Elasticsearch_Details['service']
            Elasticsearch_Host = Elasticsearch_Details['host']
            Elasticsearch_Port = int(Elasticsearch_Details['port'])

        if Elasticsearch_Service and Elasticsearch_Host and Elasticsearch_Port:
            Use_Elasticsearch = True

        else:
            Use_Elasticsearch = False

        return [Elasticsearch_Service, Elasticsearch_Host, Elasticsearch_Port, Use_Elasticsearch]

    except Exception as e:
        logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Load_Main_Database():
    logging.info(str(datetime.datetime.now()) + " Loading Scrummage's Main Database configuration data.")

    try:
        with open(Configuration_File) as JSON_File:
            Configuration_Data = json.load(JSON_File)

            for DB_Info in Configuration_Data['postgresql']:
                DB_Host = DB_Info['host']
                DB_Port = str(int(DB_Info['port']))
                DB_Username = DB_Info['user']
                DB_Password = DB_Info['password']
                DB_Database = DB_Info['database']

    except:
        logging.warning(str(datetime.datetime.now()) + " Failed to load configuration file.")

    try:
        DB_Connection = psycopg2.connect(user=DB_Username,
                                      password=DB_Password,
                                      host=DB_Host,
                                      port=DB_Port,
                                      database=DB_Database)
        return DB_Connection

    except:
        logging.warning(str(datetime.datetime.now()) + " Failed to connect to database.")

def Load_JIRA_Configuration():
    logging.info(str(datetime.datetime.now()) + " Loading JIRA configuration data.")

    try:

        with open(Configuration_File) as json_file:  
            Configuration_Data = json.load(json_file)

            for JSON_Details in Configuration_Data['JIRA']:
                JIRA_Project_Key = JSON_Details['project_key']
                JIRA_Address = JSON_Details['address']
                JIRA_Username = JSON_Details['username']
                JIRA_Password = JSON_Details['password']
                JIRA_Ticket_Type = JSON_Details['ticket_type']

            if JIRA_Project_Key and JIRA_Address and JIRA_Username and JIRA_Password and JIRA_Ticket_Type:
                Use_JIRA = True

            else:
                Use_JIRA = False

        return [JIRA_Project_Key, JIRA_Address, JIRA_Username, JIRA_Password, JIRA_Ticket_Type, Use_JIRA]

    except Exception as e:
        logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Load_Slack_Configuration():
    logging.info(str(datetime.datetime.now()) + " Loading Slack configuration data.")

    try:

        with open(Configuration_File) as json_file:  
            Configuration_Data = json.load(json_file)

            for JSON_Details in Configuration_Data['slack']:
                Slack_Token = JSON_Details['token']
                Slack_Channel = JSON_Details['channel']

            if Slack_Token and Slack_Channel:
                Use_Slack = True

            else:
                Use_Slack = False

        return [Slack_Token, Slack_Channel, Use_Slack]

    except Exception as e:
        logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Load_Scumblr_Configuration():
    logging.info(str(datetime.datetime.now()) + " Loading Scumblr configuration data.")

    try:

        with open(Configuration_File) as JSON_File:
            Configuration_Data = json.load(JSON_File)

            for PostgreSQL_Details in Configuration_Data['scumblr']:
                PostgreSQL_Host = PostgreSQL_Details['host']
                PostgreSQL_Port = str(PostgreSQL_Details['port'])
                PostgreSQL_Database = PostgreSQL_Details['database']
                PostgreSQL_User = PostgreSQL_Details['user']
                PostgreSQL_Password = PostgreSQL_Details['password']

            if PostgreSQL_Host and PostgreSQL_Port and PostgreSQL_Database and PostgreSQL_User and PostgreSQL_Password:
                Use_PostgreSQL = True

            else:
                Use_PostgreSQL = False

        return [PostgreSQL_Host, PostgreSQL_Port, PostgreSQL_Database, PostgreSQL_User, PostgreSQL_Password, Use_PostgreSQL]

    except Exception as e:
        logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Load_RTIR_Configuration():
    logging.info(str(datetime.datetime.now()) + " Loading RTIR configuration data.")

    try:
        with open(Configuration_File) as JSON_File:
            Configuration_Data = json.load(JSON_File)

            for RTIR_Details in Configuration_Data['rtir']:
                RTIR_HTTP_Service  = RTIR_Details['service']
                RTIR_Host = RTIR_Details['host']
                RTIR_Port = str(RTIR_Details['port'])
                RTIR_User = RTIR_Details['user']
                RTIR_Password = RTIR_Details['password']
                RTIR_Authenticator = RTIR_Details['authenticator']

            if RTIR_HTTP_Service and RTIR_Host and RTIR_Port and RTIR_User and RTIR_Password and RTIR_Authenticator:
                Use_RTIR = True

            else:
                Use_RTIR = False

        return [RTIR_Host, RTIR_Port, RTIR_User, RTIR_Password, RTIR_HTTP_Service, RTIR_Authenticator, Use_RTIR]

    except Exception as e:
        logging.warning(str(datetime.datetime.now()) + " " + str(e))

def CSV_Output(Title, Plugin_Name, Domain, Link, Result_Type, Output_File, Task_ID):

    try:
        Headings = ["Title", "Plugin", "Domain", "Link", "Created At", "Output File", "Result Type", "Task ID"]
        Data = [Title, Plugin_Name, Domain, Link, str(datetime.datetime.now()), Output_File, Result_Type, str(Task_ID)]
        File_Path = os.path.dirname(os.path.realpath('__file__'))
        File_Path = File_Path + "/static/protected/output/" + Plugin_Name
        Complete_File = File_Path + "Output.csv"

        if not os.path.exists(Complete_File):
            CSV_Output = csv.writer(open(Complete_File, 'w'))
            CSV_Output.writerow(Headings)
            CSV_Output.writerow(Data)
            logging.info(str(datetime.datetime.now()) + " CSV output file created.")

        else:
            CSV_Output = csv.writer(open(Complete_File, 'a'))
            CSV_Output.writerow(Data)
            logging.info(str(datetime.datetime.now()) + " CSV output file updated.")

    except Exception as e:
        logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Defect_Dojo_Output(Title, Description):
    DD_Details = Load_Defect_Dojo_Configuration()

    if DD_Details[7]:

        try:
            Impact = 'All Scrummage findings have the potential to cause significant damage to a business\' finances, efficiency and reputation. Therefore, findings should be investigated to assist in reducing this risk.'
            Mitigation = 'It is recommended that this issue be investigated further by the security team to determine whether or not further action needs to be taken.'
            DD_Connection = defectdojo.DefectDojoAPI(DD_Details[1], DD_Details[0], DD_Details[2], debug=False)
            Finding = DD_Connection.create_finding(Title, Description, 'Low', '', str(datetime.datetime.now().strftime('%Y-%m-%d')), DD_Details[4], DD_Details[3], DD_Details[5], DD_Details[6], Impact, True, False, Mitigation)

            try:
                Finding = str(int(str(Finding)))
                logging.info(str(datetime.datetime.now()) + " DefectDojo finding " + Finding + " created.")

            except:
                logging.info(str(datetime.datetime.now()) + " Failed to create DefectDojo finding.")

        except (Exception, psycopg2.DatabaseError) as Error:
            logging.warning(str(datetime.datetime.now()) + str(Error))

def Main_Database_Insert(Title, Plugin_Name, Domain, Link, Result_Type, Output_File, Task_ID):
    Connection = Load_Main_Database()

    try:
        # Create connection cursor.
        Cursor = Connection.cursor()
        Cursor.execute("SELECT * FROM results WHERE link like %s", (Link,))
        Item_Already_in_Database = Cursor.fetchone()

        if Item_Already_in_Database is None:
            # Execute statement.
            Cursor.execute("INSERT INTO results (title, plugin, status, domain, link, created_at, updated_at, output_file, result_type, task_id) VALUES (%s,%s,%s,%s,%s,%s,%s,%s,%s,%s)", (Title, Plugin_Name, "Open", Domain, Link, str(datetime.datetime.now()), str(datetime.datetime.now()), Output_File, Result_Type, Task_ID,))

        else:
            logging.info(str(datetime.datetime.now()) + " Entry already exists in the database. Skipping...")

    except (Exception, psycopg2.DatabaseError) as Error:
        logging.warning(str(datetime.datetime.now()) + str(Error))

    finally:

        if Connection is not None:
            Connection.commit()
            Connection.close()

def Scumblr_Main(Link, Domain, Title):
    Scumblr_Details = Load_Scumblr_Configuration()
    Connection = ""

    if Scumblr_Details[5]:

        try:
            # Connect to the PostgreSQL server.
            Connection = psycopg2.connect(host=Scumblr_Details[0], port=Scumblr_Details[1], database=Scumblr_Details[2], user=Scumblr_Details[3], password=Scumblr_Details[4])

            # Create connection cursor.
            Cursor = Connection.cursor()
            Cursor.execute("SELECT * FROM results WHERE url like %s", (Link,))
            Item_Already_in_Database = Cursor.fetchone()

            if Item_Already_in_Database is None:
                # Execute statement.
                Cursor.execute("INSERT INTO results (title, url, created_at, updated_at, domain) VALUES(%s, %s, %s, %s, %s)", (Title, Link, str(datetime.datetime.now()), str(datetime.datetime.now()), Domain))

            else:
                logging.info(str(datetime.datetime.now()) + " Entry already exists in Scumblr database. Skipping...")

        except (Exception, psycopg2.DatabaseError) as Error:
            logging.warning(str(datetime.datetime.now()) + " " + Error)

        finally:

            if Connection is not None:
                Connection.commit()
                Connection.close()
                logging.info(str(datetime.datetime.now()) + " Result added to Scumblr database.")
                logging.info(str(datetime.datetime.now()) + " Database connection closed.")

def RTIR_Main(Ticket_Subject, Ticket_Text):
    RTIR_Details = Load_RTIR_Configuration()

    if RTIR_Details[6]:

        try:
            Request_Data = "content=id: ticket/new\nQueue: 1\nSubject: " + Ticket_Subject + "\nText: " + Ticket_Text

            if RTIR_Details[5] == "cookie_based":
                requests.post(RTIR_Details[4] + '://' + RTIR_Details[0] + ':' + RTIR_Details[1] + '/REST/1.0/ticket/new?user=' + RTIR_Details[2] + "&pass=" + RTIR_Details[3], Request_Data)

            else:
                logging.info(str(datetime.datetime.now()) + " No Authenticator specified, using the default which is cookie-based authentication,")
                requests.post(RTIR_Details[4] + '://' + RTIR_Details[0] + ':' + RTIR_Details[1] + '/REST/1.0/ticket/new?user=' + RTIR_Details[2] + "&pass=" + RTIR_Details[3], Request_Data)

            logging.info(str(datetime.datetime.now()) + " RTIR ticket created.")

        except Exception as e:
            logging.warning(str(datetime.datetime.now()) + " " + str(e))

def JIRA_Main(Ticket_Summary, Ticket_Description):
    JIRA_Details = Load_JIRA_Configuration()

    if JIRA_Details[5]:

        try:
            JIRA_Options={'server': JIRA_Details[1]}
            JIRA_Session=JIRA(options=JIRA_Options,basic_auth=(JIRA_Details[2], JIRA_Details[3]))
            JIRA_Session.create_issue(project={'key': JIRA_Details[0]}, summary=Ticket_Summary, description=Ticket_Description, issuetype={'name': JIRA_Details[4]})
            logging.info(str(datetime.datetime.now()) + " JIRA ticket created.")

        except Exception as e:
            logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Slack_Main(Description):
    Slack_Details = Load_Slack_Configuration()

    if Slack_Details[2]:

        try:
            client = slack.WebClient(token=Slack_Details[0])
            client.chat_postMessage(channel=Slack_Details[1], text=Description)
            logging.info(str(datetime.datetime.now()) + " Slack Notification created.")

        except Exception as e:
            logging.warning(str(datetime.datetime.now()) + " " + str(e))

def Elasticsearch_Main(Title, Plugin_Name, Domain, Link, Result_Type, Output_File, Task_ID, Concat_Plugin_Name):
    Elasticsearch_Details = Load_Elasticsearch_Configuration()

    if Elasticsearch_Details[3]:

        try:
            URI = Elasticsearch_Details[0] + Elasticsearch_Details[1] + ":" + str(Elasticsearch_Details[2]) + "/scrummage/result/" + Concat_Plugin_Name
            headers = {"Content-Type": "application/json"}
            data = {"title": Title, "plugin": Plugin_Name, "domain": Domain, "link": Link, "output_file": Output_File, "result_type": Result_Type, "created_at": str(datetime.datetime.now()), "associated_task_id": str(Task_ID)}
            data = json.dumps(data)
            resp = requests.post(URI, data=data, headers=headers)

            if resp.status_code == 200:
                logging.info(str(datetime.datetime.now()) + " Result created in Elasticsearch, using the URI " + URI + ".")

            else:
                logging.info(str(datetime.datetime.now()) + " Failed to create result in Elasticsearch, using the URI " + URI + ".")

        except:
            logging.warning(str(datetime.datetime.now()) + " Failed to create result in Elasticsearch.")

def Email_Main(Email_Subject, Email_Body):
    Email_Details = Load_Email_Configuration()

    if Email_Details[5]:

        try: # Send Email Alerts when called.
            server = smtplib.SMTP(Email_Details[0], Email_Details[1])
            server.ehlo()
            server.starttls()
            server.login(Email_Details[2], Email_Details[3])
            msg = MIMEMultipart()
            msg['From'] = Email_Details[2]
            msg['To'] = Email_Details[4]
            msg['Subject'] = Email_Subject
            msg.attach(MIMEText(Email_Body, 'plain'))
            text = msg.as_string()
            server.sendmail(Email_Details[2], Email_Details[4], text)
            server.quit()
            logging.info(str(datetime.datetime.now()) + " Email Sent.")

        except:
            logging.warning(str(datetime.datetime.now()) + " Failed to send alert! Check email login settings.")