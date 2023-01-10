#!/usr/bin/env python
# coding: utf-8

# In[1]:


from mysql.connector import connect
import getpass


hostname="localhost"
dbname="idmpproject"
uname="root"
pwd=getpass.getpass(prompt="Password:\n")

conn = connect(
host=hostname,
user=uname,
password=pwd,
database=dbname,
autocommit=True
)


import getpass
import pandas as pd
pd.set_option('display.max_colwidth', None)
from IPython.display import display
from dateutil import parser
success=False
while success is not True:
    try:
        option = int(input("\n Please choose your role\n1. Therapist\n2. Patient\n3. Admin\n4. Choose 4 to exit\n"))
        if option not in [1,2,3,4]:
            raise ValueError;
        if option==4:
            success = True
        if option==1:
            tsuccess=False
            while tsuccess is not True:
                try:
                    toption = int(input("\n Please choose your role\n1. New Therapist\n2. Existing therapist\n3. Choose 3 to exit\n"))
                    if toption not in [1,2,3]:
                        raise ValueError;
                    if toption==3:
                        tsuccess = True
                    #new therapist
                    if toption==1:
                        tname=input("enter therapist name: ",)
                        pwd=input("enter 5 char password :",)
                        tnum=input("enter therapist phone number: ",)
                        tclinic=input("enter therapist clinic:",)
                        query = "SELECT * from domainofillness;"
                        with conn.cursor() as cursor: 
                            cursor.execute(query)
                            result=cursor.fetchall()
                        df = pd.read_sql(query,conn)
                        display(df)
                        did= input("enter your specialization number from the above list displayed:",)
                        cursor = conn.cursor()
                        #stored proc inserts the values into therapist table
                        query = "call new_therapist(\'"+did+"\',\'"+tname+"\',\'"+tclinic+"\',\'"+tnum+"\',\'"+pwd+"\');"
                        cursor.execute(query)
                        print("\n\nSuccessful Registration\n")
                        q1="select TID from therapist where Ppass=md5(%s) and tname=%s and tnum=%s"
                        arr=[pwd,tname,tnum]
                        cursor = conn.cursor()
                        cursor.execute(q1,arr)
                        result = cursor.fetchone()
                        #returns the id of the therapist for their reference. this id is used for login
                        print("your therapist id is:",result[0])
                    #existing therapist login
                    if toption==2:
                        tid = input("Please enter your therapist ID:\n")
                        ppass = getpass.getpass(prompt="Password:\n")
                        cursor = conn.cursor()
                        query = "SELECT TID from therapist where Ppass = md5(\'"+ppass+"\') and TID = \'"+tid+"\';"
                        cursor.execute(query)
                        result = cursor.fetchone()
                        #checks if a therapist with the matching id and password exits
                        if result is None:
                            print("there exists no therapist with this ID and password! Please register")
                        elif result[0]== int(tid):
                            tpsuccess = False
                            print("Login Success!")
                            while tpsuccess is not True:
                                try:
                                    poption = int(input("\n Choose what you would like to do\n1. Create New Schedule \n2. Check existing schedule \n3. Delete Schedule \n4. Check new appointments with patients \n5. Create diagnosis and treatment for patients \n6.View patient history \n7. Choose 7 to exit\n"))
                                    #raises error if the option is not in the list
                                    if poption not in [1,2,3,4,5,6,7]:
                                        raise ValueError;
                                    if poption==7:
                                        tpsuccess = True
                                        tsuccess = True
                                    #enter new schedule for therapist
                                    if poption==1:
                                        day=input("enter a day for schedule:",)
                                        ts=input("enter a start time [HH:MM]",)
                                        te=input("enter a end time [HH:MM]",)
                                        cursor = conn.cursor()
                                        #inserts value into the schedule table
                                        query = "call new_schedule_for_therapist(\'"+tid+"\',\'"+day+"\',\'"+ts+"\',\'"+te+"\')"
                                        cursor.execute(query)
                                    #checks the schedule for therapist
                                    if poption==2:
                                        r=[tid]
                                        query = "select * from scheduletable where TID="+str(tid)+";"
                                        cursor = conn.cursor()
                                        cursor.execute(query)
                                        result=cursor.fetchall()
                                        if bool(result) is False:
                                            print("You have no schedule")
                                        else:
                                            df = pd.read_sql(query,conn)
                                            display(df)
                                    #deletes the schedule for therapist
                                    if poption==3:

                                        sid=input("enter the Schedule id you want to delete:",)
                                        query = "delete from scheduletable where SID=%s;"
                                        s=[sid]
                                        cursor = conn.cursor()
                                        cursor.execute(query,s)
                                    #checks the appointment with patients
                                    if poption==4:
                                        query = "select p.patientID,pname,day,timestart,timeend from scheduletable s, appointmenttable a join patienttable p where s.SID=a.SID and a.patientID=p.patientID and TID="+str(tid)+";"
                                        with conn.cursor() as cursor: 
                                            cursor.execute(query)
                                            result=cursor.fetchall()
                                            if bool(result) is False:
                                                print("You have no upcoming appointments")
                                            else:
                                                df = pd.read_sql(query,conn)
                                                display(df)
                                    #creates treatment and diagnosis for patient
                                    if poption==5:
                                        pid=input("enter the patient id for diagnosis",)
                                        query = "SELECT * from domainofillness;"
                                        with conn.cursor() as cursor: 
                                            cursor.execute(query)
                                            result=cursor.fetchall()
                                        df = pd.read_sql(query,conn)
                                        display(df)
                                        did= input("enter the diagnosis from the above list displayed:",)
                                        cursor = conn.cursor()
                                        #inserts value into diagnosis table
                                        query = "call therapist_diagnosis(\'"+pid+"\',\'"+tid+"\',\'"+did+"\');"
                                        cursor.execute(query)
                                        q2="select diagnosis_id from diagnosis where patientID=%s and TID=%s and DID=%s"
                                        ar1=[pid,tid,did]
                                        cursor = conn.cursor()
                                        cursor.execute(q2,ar1)
                                        result = cursor.fetchone()
                                        diagnosisid=result[0]
                                        print("Diagnosis Updated! \n")
                                        print("Please suggest a treatment for the patient now \n")
                                        query = "SELECT * from medicine;"
                                        with conn.cursor() as cursor: 
                                            cursor.execute(query)
                                            result=cursor.fetchall()
                                        df = pd.read_sql(query,conn)
                                        display(df)
                                        medid=input("enter a medicine ID from the list above:",)
                                        dos=input("enter the dosage of the medicine (ex: 20mg):",)
                                        ndays=input("enter the number of days per week for the medicine:",)
                                        rehab=input("enter 1 if the patient needs rehab, else 0:",)
                                        #inserts value into the treatment table
                                        query="call therapist_treatment(%s,%s,\'"+dos+"\',\'"+ndays+"\',%s);"
                                        ar3=[diagnosisid,medid,int(rehab)]
                                        cursor = conn.cursor()
                                        cursor.execute(query,ar3)
                                    #checks patient history of a patient
                                    if poption==6:
                                        pid1=input("enter the patient id ",)
                                        p=[int(pid1)]
                                        cursor = conn.cursor()
                                        query = " select pname,patientID,illness from phistory where patientID="+str(pid1)+";"
                                        cursor = conn.cursor()
                                        cursor.execute(query)
                                        result=cursor.fetchall()
                                        if bool(result) is False:
                                            print("this patient has no previous medical history")
                                        else:
                                            df = pd.read_sql(query,conn)
                                            display(df)

                                except ValueError:
                                    print("Incorrect number of choices, please enter correct choice")
                except ValueError:
                            print("Incorrect number of choices, please enter correct choice")
        # If user chooses the Patient Option
        if option==2:
            newoption = int(input("\n Please choose if you are:\n1. Existing Patient\n2. New Patient\n3. Choose 3 to exit\n"))
            # Raise a ValueError if the users chooses any option outside the range
            if newoption not in [1,2,3]:
                raise ValueError;
            # Exit option
            if newoption == 3:
                psuccess = True;
            # New patient
            if newoption == 1:
                pid = input("Please enter your Patient ID:\n")
                ppass = getpass.getpass(prompt="Password:\n")
                cursor = conn.cursor()
                # Checking credentials
                query = "SELECT patientID from patienttable where Ppass = md5(\'"+ppass+"\') and patientID = \'"+pid+"\';"
                cursor.execute(query)
                result = cursor.fetchone()
                # If result is None, credentials are incorrect
                if result == None:
                    raise KeyError;
                else:
                    # Check if the pid returned is same as the user
                    if result[0]== int(pid):
                        psuccess = False
                        print("Login Success!")
                         # Run while and try - catch for options
                        while psuccess is not True:
                            try:
                                poption = int(input("\n Choose what you would like to do\n1. Check appointment with Therapist\n2. Check rehab appointment\n3. Book appointment with Therapist\n4. Book rehab appointment\n5. Delete appointment with Therapist\n6. Delete rehab appointment\n7. Check recommended treatment \n8. View your survey scores \n9. Choose 9 to exit\n"))
                                    # Raise a ValueError if the users chooses any option outside the range
                                if poption not in [1,2,3,4,5,6,7,8,9]:
                                    raise ValueError;
                                    # Exit option
                                if poption==9:
                                    psuccess = True
                                    # View therapist appointment
                                if poption==1:
                                    cursor = conn.cursor()
                                    # Joining schedule, appointment and therapist tables to display
                                    # the details while finding the SID of the patient from appointment table
                                    query = """SELECT day, timestart, timeend, tname, tclinic, tnum from scheduletable natural join appointmenttable natural join therapist
                                    where SID IN (select SID from appointmenttable where 
                                    patientID=(select patientID from patienttable where patientID='"""+pid+"""'));"""
                                    cursor.execute(query)
                                    result = cursor.fetchall()
                                    df = pd.read_sql(query, conn)
                                    display(df)
                                    # View rehab appointment
                                if poption==2:
                                    cursor = conn.cursor()
                                    # Joining rehab, rehab appointment and patient tables to display
                                    # the details of the rehab
                                    query = """select Pname, rehab_appt_id, rehab_name, rehab_type, rehab_loc, rehab_number, 
                                    admit_datetime from patienttable p natural join 
                                    rehab_appt natural join rehab where p.patientID = """+pid+";"
                                    cursor.execute(query)
                                    result = cursor.fetchall()
                                    df = pd.read_sql(query,conn)
                                    display(df)
                                    # Book therapist appointment
                                if poption==3:
                                    cursor = conn.cursor()
                                    # Joining the patientscore, patient, domainofillness, therapist and schedule tables
                                    # to display the therapists who are available and work in the same domain
                                    # as the users' diagnosed illnesses while displaying only those schedules
                                    # that are not already booked in the appointment table
                                    query = """select distinct(s.SID), tname, illness, day, timestart, timeend from patientscore ps join patienttable p on ps.patientID = p.patientID join domainofillness d on ps.DID = d.DID join therapist t on d.DID = t.DID 
                                    join scheduletable s on t.TID = s.TID where ps.DID in (select DID from patientscore where 
                                    patientID = (select patientID from patienttable where patientID=\'"""+pid+"""')) 
                                    and s.SID not in (select SID from appointmenttable);
                                    """
                                    cursor.execute(query)
                                    result = cursor.fetchall()
                                    df = pd.read_sql(query, conn)
                                    # Checks if there are any available schedules
                                    if cursor.rowcount !=0:
                                        display(df)
                                        # Prompt user to choose the schedule ID based on what is displayed
                                        book = input("Please choose the SID you want to book the appointment for:\n")
                                        cursor = conn.cursor()
                                        query = "SELECT patientID from patienttable where patientID = \'"+pid+"\';"
                                        cursor.execute(query)
                                        result = cursor.fetchone()
                                        patientID = int(result[0])
                                        cursor = conn.cursor()
                                        cursor.callproc('book_appointment',(patientID,book,))
                                        results = cursor.stored_results()
                                        for result in results:
                                            message = result.fetchall()[0][0]
                                            # if keys are not from the list displayed, stored procedue will throw an error message
                                            # that we use to prompt the user to re-enter the schedule ID
                                            if message != "Incorrect keys error encountered":
                                                print("Successfully booked appointment!")
                                                psuccess = True
                                                success = True
                                            else:
                                                print(message)
                                    else:
                                        print("Sorry, no appointment available.")
                                    # Display rehab centres to the user
                                if poption==4:
                                    cursor = conn.cursor()
                                    query = "select * from rehab"
                                    cursor.execute(query)
                                    result = cursor.fetchall()
                                    df = pd.read_sql(query,conn)
                                    display(df)
                                    # Request user to enter the rehab ID and the date as mentioned in the format
                                    print("Please enter your preferred rehab ID and admit date as Jul 7 1970 10:31AM:\n")
                                    rehabID = input("Rehab ID: ")
                                    admitdate = input("\nAdmit Date: ")
                                    # Parse the date to standard datetime format 
                                    admitdate = parser.parse(admitdate)
                                    cursor = conn.cursor()
                                    cursor.callproc('rehab_appointment',(rehabID, pid, admitdate,))
                                    results = cursor.stored_results()
                                        # if keys are not from the list displayed, stored procedue will throw an error message
                                    for result in results:
                                        message = result.fetchall()[0][0]
                                        if message != "Incorrect keys error encountered":
                                            print("Successfully booked appointment!")
                                            psuccess = True
                                            success = True
                                        else:
                                            print(message)
                                    # Delete therapist appointment
                                if poption==5:
                                    cursor = conn.cursor()
                                    # Display only the appointment schedules under the patient by joining
                                    # appointment, schedule and therapist tables
                                    query = """SELECT app_id, day, timestart, timeend, tname, tclinic 
                                    FROM appointmenttable a natural join 
                                    scheduletable natural join therapist where a.patientID = """+pid+";"
                                    cursor.execute(query)
                                    result = cursor.fetchall()
                                    df = pd.read_sql(query,conn)
                                    # If current appointments are not 0
                                    if cursor.rowcount !=0:
                                        display(df)
                                        appt_id = input("Please choose appt_id you want to delete:")
                                        cursor = conn.cursor()
                                        # Delete appointment
                                        query = """delete from appointmenttable where app_id="""+appt_id+" and patientID = "+pid+";"
                                        cursor.execute(query)
                                        results = cursor.fetchone()
                                        count = cursor.rowcount
                                        # Get affected row count, if it is 0 it means it is an invalid option
                                        if count==0:
                                            print("Please enter a valid option\n")
                                        else:
                                            print("Successfully deleted appointment!")
                                    else:
                                        # if the original rowcount is 0 means user has no appointments currently
                                        print("You currently have no appointments booked.")
                                    # Delete rehab appointment
                                if poption==6:
                                    cursor = conn.cursor()
                                    # Display only the rehab appointments under the patient by joining
                                    # rehab appointment, rehab and patient tables
                                    query = """SELECT rehab_appt_id, Pname, rehab_name, rehab_loc,
                                    admit_datetime FROM rehab_appt natural join patienttable p natural join 
                                    rehab where p.patientID = """+pid+";"
                                    cursor.execute(query)
                                    result = cursor.fetchall()
                                    df = pd.read_sql(query,conn)
                                    display(df)
                                    appt_id = input("Please choose rehab_appt_id you want to delete:")
                                    cursor = conn.cursor()
                                    # delete query
                                    query = """delete from rehab_appt where rehab_appt_id="""+appt_id+" and patientID = "+pid+";"
                                    cursor.execute(query)
                                    results = cursor.fetchone()
                                    count = cursor.rowcount
                                    # If row count is 0 it means non existent option selected
                                    if count==0:
                                        print("Please enter a valid option\n")
                                    else:
                                        print("Successfully deleted appointment!")
                                    # Check treatment
                                if poption==7:
                                    cursor = conn.cursor()
                                    # Select medicine details and dosage under the patient's ID
                                    # by joining patient, diagnosis, treatment, medicine and domainofillness tables
                                    query = """select illness, med_name, med_brand, dosage, num_days, Rehab_recommendation 
                                    from patienttable natural join diagnosis natural join treatment 
                                    natural join medicine natural join domainofillness where patientID="""+pid+";"
                                    cursor.execute(query)
                                    results = cursor.fetchall()
                                    df = pd.read_sql(query,conn)
                                    # if the rowcount is not 0 it means the patient has been treated
                                    if cursor.rowcount!=0:
                                        display(df.iloc[:,:-1])
                                        # check if patient has been recommended rehab
                                        if int(results[0][5]) == 1:
                                            print("You have been recommended rehabilitation")
                                    else:
                                        print("You have no treatment recommended currently")
                                    # Display patient diagnosed illnesses
                                if poption==8:
                                    cursor = conn.cursor()
                                    # Display the results by joining the patientscore and domainofillness tables
                                    query = """select illness from patientscore p, domainofillness d where p.DID=d.DID and patientID="""+pid+";"
                                    with conn.cursor() as cursor: 
                                        cursor.execute(query)
                                        result=cursor.fetchall()
                                    print("You have been diagnosed with the following based on the survey you have taken:")
                                    df = pd.read_sql(query,conn)   
                                    display(df) 
                                
                            except ValueError:
                                print("Incorrect choice, please enter correct choice")
                # New user
            if newoption==2:
                # Take user details
                print("Please enter your details as requested below\n")
                username = input("Please enter your full name: ")
                num = input("Please enter your contact number: ")
                add = input("Please enter your address: ")
                email = input("Please enter your email id: ")
                password = getpass.getpass(prompt="Please enter your password: ")
                cursor = conn.cursor()
                cursor.callproc('user_registration',(username,num,add,email,password,))
                # User questionnaire
                print("Please take the questionnaire below. Answer with Y or N only.")
                cursor = conn.cursor()
                query =  "select patientID from patienttable where Pemail='"+email+"';"
                cursor.execute(query)
                result = cursor.fetchone()
                patientID = result[0]
                # Display user's ID
                print("PatientID: ", int(patientID))
                cursor = conn.cursor()
                # Insert user
                cursor.callproc('new_questionnaire',(patientID,))
                # List of symptoms of illnesses
                illnesses = ["Do you feel worried, frightened or avoid situations that make you anxious?",                            "Feeling down or little interest in doing things?",                            "Do you have extreme mood swings and/or loss of memory?",                            "Are you easily agitated, get nightmares or horrifying flashbacks?",                            "Are you easily disoriented or have thought disorder?",                            "Do you ever go long periods without eating or binge eating? Have you felt socially pressured to lose weight?",                            "Do you find yourself constantly arguing, having temper flares and the urge to not follow rules?",                            "Do you have problems with language and speech, motor functions or other skills related to memory and learning?",                            "For children, did they have a drastic change in personality, blaming others or feel socially isolated?",                            "Do you have the need for things to be ordered, hypervigilance, impulsivity, agitation or repeatedly go over things?",                            "Are you constantly defensive, hostile or aggresive, take offense to things easily, not able to trust or confide in people?",                            "Do you lack empathy or have a total lack of regard for the consequences of your actions?"]
                for i in range(len(illnesses)):
                    try:
                        print(illnesses[i])
                        resp = input("Please choose Y or N: ")
                        # If prompt not in range raise error
                        if resp not in ['Y','y','N','n']:
                            raise IndexError;
                            # If Y/y, insert patient ID with domain of illness ID
                        elif resp=='Y' or resp=='y':
                            DID = str(i+1)
                            cursor = conn.cursor()
                            # Select the QID of new patient
                            query = "select QID from questdiag where patientID="+str(patientID)+";"
                            cursor.execute(query)
                            result = cursor.fetchone()
                            QID = int(result[0])
                            cursor = conn.cursor()
                            # Inserting the score using stored proc
                            cursor.callproc('new_patientscore',(patientID,QID,DID,))
                            
                    except IndexError:
                        print("Incorrect choice, please enter valid choice")
                print("Thank you for taking the mental health survey! Please login to view your results")
        # admin enters the system
        if option == 3:
            asuccess=False
            while asuccess is not True:
                try:
                    option = int(input("\n What would you like to do today \n1. check the number of therapist in a particular domain of illness \n2. Check the number of patients under a therapist \n3. Return the most common illness \n4. Check the number of patients under a Rehab \n5. Return the most popular therapist \n6. Choose 6 to exit\n"))
                    if option not in [1,2,3,4,5,6]:
                        raise ValueError; 
                    if option==6:
                        asuccess = True
                    #check the number of therapist in a particular domain of illness
                    if option==1:
                        domainid=input("enter the domain ID:",)
                        cursor = conn.cursor()
                        #function to display the results
                        query = "select therapist_countby_domain(%s);"
                        s1=[domainid]
                        cursor.execute(query,s1)
                        result = cursor.fetchone()
                        print("Number of therapist:",result[0])
                    if option==2:
                        tid = input("Please enter your therapist ID:",)
                        cursor = conn.cursor()
                        #function to check the number of patients under a therapist
                        query = "select patients_under_therapist(%s);"
                        s2=[tid]
                        cursor.execute(query,s2)
                        result = cursor.fetchone()
                        print("Number of Patients:",result[0])
                    if option==3:
                        cursor = conn.cursor()
                        # function to return the most common illness
                        query = "select most_patients_in_domain();"
                        cursor.execute(query)
                        result = cursor.fetchone()
                        print("Most common illness:",result[0])
                    if option==4:
                        rid = input("Please enter your rehab ID:",)
                        cursor = conn.cursor()
                        s3=[rid]
                        #function to Check the number of patients under a Rehab
                        query = "select patients_in_rehab(%s);"
                        cursor.execute(query,s3)
                        result = cursor.fetchone()
                        print("Number of patients in this rehab:",result[0])     
                    if option==5:
                        cursor = conn.cursor()
                        #function to Return the most popular therapist
                        query = "select most_popular_therapist();"
                        cursor.execute(query)
                        result = cursor.fetchone()
                        print("Number of patients in a particular rehab:",result[0]) 

                except ValueError:
                            print("Incorrect number of choices, please enter correct choice")
            
    except ValueError:
                print("Incorrect choice, please enter valid choice")
    except KeyError:
                print("Incorrect ID or Password. Please try again.")


# In[ ]:





# In[ ]:




