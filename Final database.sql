create table domainofillness
(
DID INT auto_increment,
illness varchar(200),
primary key(DID)
);

create table therapist
(
TID INT AUTO_INCREMENT,
DID INT,
tname varchar(50),
tclinic varchar(50),
tnum varchar(50),
Ppass varchar(50) NOT NULL,
primary key(TID),
foreign key (DID) references domainofillness (DID)
on delete cascade
);


create table scheduletable
(
SID INT auto_increment,
TID INT,
day varchar(20),
timestart varchar(20),
timeend varchar(20),
primary key(SID),
foreign key (TID) references therapist (TID)
on delete cascade
);

create table rehab (
rehab_id INT auto_increment,
rehab_name varchar(50),
rehab_type varchar(50),
rehab_loc varchar(50),
rehab_number varchar(15),
primary key(rehab_id)
);

create table patienttable (
patientID INT AUTO_INCREMENT,
Pname varchar(25),
Pcontact_num varchar(15),
Paddress varchar(50),
Pemail varchar(50) NOT NULL UNIQUE,
Ppass varchar(50) NOT NULL,
primary key(patientID),
CHECK (Pemail LIKE '%_@_%')
);


create table rehab_appt (
rehab_appt_id INT auto_increment,
rehab_id INT,
patientID INT,
admit_datetime datetime,
primary key (rehab_appt_id),
foreign key (rehab_id) references rehab (rehab_id)
on delete cascade,
foreign key (patientID) references patienttable(patientID)
on delete cascade
);

create table medicine(
med_id INT auto_increment,
med_name varchar(50),
med_brand varchar(50),
primary key(med_id)
);

create table appointmenttable(
app_id INT AUTO_INCREMENT,
patientID INT,
SID INT,
primary key(app_id),
foreign key (patientID) references patienttable (patientID)
on delete cascade,
foreign key (SID) references scheduletable (SID)
on delete cascade
);

create table diagnosis(
diagnosis_id INT auto_increment,
patientID INT,
TID INT,
DID INT,
primary key(diagnosis_id),
foreign key (patientID) references patienttable (patientID),
foreign key (TID) references therapist (TID)
on delete cascade,
foreign key (DID) references domainofillness (DID)
on delete cascade
);

create table treatment(
treatment_id INT auto_increment,
diagnosis_id INT,
med_id INT,
dosage varchar(20),
num_days varchar(20),
Rehab_recommendation BIT DEFAULT 0,
primary key(treatment_id),
foreign key (diagnosis_id) references diagnosis (diagnosis_id)
on delete cascade,
foreign key (med_id) references medicine (med_id)
on delete cascade
);

create table questdiag (
QID int auto_increment,
patientID int UNIQUE,
Date_Taken datetime,
primary key (QID, patientID),
foreign key (patientID) references patienttable(patientID)
on delete cascade
);

create table patientscore(
patientID INT NOT NULL,
QID int NOT NULL,
DID int NOT NULL,
primary key(patientID, QID, DID),
foreign key(patientID) references patienttable(patientID)
on delete cascade,
foreign key(QID) references questdiag(QID)
on delete cascade,
foreign key(DID) references domainofillness(DID)
on delete cascade
);

insert into domainofillness values(1,'Anxiety Disorders');
insert into domainofillness values(2,'Depression');
insert into domainofillness values(3,'Bipolar Disorder');
insert into domainofillness values(4,'Post-Traumatic Stress Disorder');
insert into domainofillness values(5,'Schizophrenia');
insert into domainofillness values(6,'Eating Disorders');
insert into domainofillness values(7,'Disruptive behaviour and dissocial disorders');
insert into domainofillness values(8,'Neurodevelopmental disorders');
insert into domainofillness values(9,'Behavioural and emotional disorders in children');
insert into domainofillness values(10,'Obsessive compulsive disorder');
insert into domainofillness values(11,'Paranoia');
insert into domainofillness values(12,'Psychosis');

insert into therapist values(1,1,'Dr. Michael Mercer','DEL AMO HOSPITAL','(310) 530-1151',MD5('abc@123'));
insert into therapist values(2,12,'Dr. Craig','VERDUGO MENTAL HEALTH CENTER','(818) 244-7257',MD5('password@123'));
insert into therapist values(3,3,'Dr. Robert','VERDUGO MENTAL HEALTH CENTER','(818) 244-7257',MD5('pass@123'));
insert into therapist values(4,11,'Dr. Moshe','SAN FERNANDO VALLEY CMHC-WRAPAROUND','(818) 897-7565',MD5('abc@123'));
insert into therapist values(5,4,'Dr. James','SAN FERNANDO VALLEY CMHC-WRAPAROUND','(818) 884-8100',MD5('password@123'));
insert into therapist values(6,2,'Dr. William','USC VERDUGO HILLS HOSPITAL','(818) 547-9544',MD5('pass@123'));
insert into therapist values(7,8,'Dr. Zhandong','USC VERDUGO HILLS HOSPITAL','(661) 702-6420',MD5('abc@123'));
insert into therapist values(8,6,'Dr.Ron','USC VERDUGO HILLS HOSPITAL','(661) 254-6030',MD5('password@123'));
insert into therapist values(9,10,'Dr.Stephen','DEL AMO HOSPITAL','(818) 755-8786',MD5('pass@123'));
insert into therapist values(10,5,'Dr.Cynthia','EL DORADO-VAN NUYS MEDICAL','(818) 995-5138',MD5('password@123'));
insert into therapist values(11,7,'Dr.David','ENCINO HOSPITAL MEDICAL CENTER','(818) 374-6901',MD5('abc@123'));
insert into therapist values(12,9,'Dr.Susanna','ENCINO HOSPITAL MEDICAL CENTER','(818) 908-4999',MD5('password@123'));
insert into therapist values(13,4,'Dr.Bruce','WEST VALLEY MHC WELLNESS CENTER','(818) 598 6900',MD5('pass@123'));
insert into therapist values(14,2,'Dr.George','ALAFIA MENTAL HEALTH INSTITUTE','(626) 455-4668',MD5('pass@123'));
insert into therapist values(15,12,'Dr.Charlie','ALAFIA MENTAL HEALTH INSTITUTE','(661) 223-3838',MD5('abc@123'));
insert into therapist values(16,1,'Dr.Thomas','WEST VALLEY MHC WELLNESS CENTER','(661) 575-9365',MD5('pass@123'));
insert into therapist values(17,7,'Dr.Louis','PDP WHITE MEMORIAL MEDICAL CENTER','(323) 268-5000',MD5('pass@123'));
insert into therapist values(18,8,'Dr.Joseph','AV WELLNESS & ENRICHMENT CENTER','(661) 265-8627',MD5('abc@123'));
insert into therapist values(19,5,'Dr.Larry','PALMDALE DISCOVER CENTER','(661) 947-1595',MD5('password@123'));
insert into therapist values(20,9,'Dr.Roger','ANTELOPE VALLEY HOSPITAL','(909) 623-6651',MD5('pass@123'));

insert into scheduletable values(1,1,'monday','20:00','21:00');
insert into scheduletable values(2,2,'tuesday','17:00','18:00');
insert into scheduletable values(3,3,'monday','15:00','16:00');
insert into scheduletable values(4,4,'wednesday','1:00','2:00');
insert into scheduletable values(5,5,'friday','14:00','15:00');
insert into scheduletable values(6,6,'thursday','21:00','22:00');
insert into scheduletable values(7,7,'saturday','18:00','19:00');
insert into scheduletable values(8,8,'tueday','13:00','14:00');
insert into scheduletable values(9,9,'wednesday','15:00','16:00');
insert into scheduletable values(10,10,'thursday','19:00','20:00');
insert into scheduletable values(11,11,'friday','20:00','21:00');
insert into scheduletable values(12,12,'thursday','15:00','16:00');
insert into scheduletable values(13,5,'monday','13:00','14:00');
insert into scheduletable values(14,7,'saturday','17:00','18:00');
insert into scheduletable values(15,8,'tuesday','19:00','20:00');


INSERT INTO rehab VALUES (1,'LAUREL PARK','INSTITUTIONS FOR MENTAL DISEASE','1425 WEST LAUREL AVE.','(909) 622-1069');
INSERT INTO rehab VALUES (2,'THE VILLAGE FAMILY SERVICES','OUTPATIENT','6801 COLD WATER CANYON BLVD. STE.','(818) 755-8786');
INSERT INTO rehab VALUES (3,'SPECIALIZED FOSTER CARE','OUTPATIENT','4024 NORTH DURFEE AVE.','(626) 455-4668');
INSERT INTO rehab VALUES (4,'SAN GABRIEL VALLEY HOSPITAL','INSTITUTIONS FOR MENTAL DISEASE','3938 COGSWELL RD.','(626) 401-1557');
INSERT INTO rehab VALUES (5,'LOS PADRINOS JUVENILE HALL','JUVENILE JUSTICE','7285 EAST QUILL DR.','(562) 940-6077');
INSERT INTO rehab VALUES (6,'SPECIALIZED FOSTER CARE','OUTPATIENT','100 WEST SECOND ST.','(626) 455-4668');
INSERT INTO rehab VALUES (7,'COMMUNITY CARE CENTER','INSTITUTIONS FOR MENTAL DISEASE','2335 SOUTH MOUNTAIN AVE.','(626) 357-3207');
INSERT INTO rehab VALUES (8,'OLIVE VISTA','INSTITUTIONS FOR MENTAL DISEASE','2350 CULVER COURT.','(909) 628-6026');
INSERT INTO rehab VALUES (9,'LANDMARK MEDICAL CENTER','INSTITUTIONS FOR MENTAL DISEASE','2030 NORTH GAREY AVE.','(909) 593-2585');
INSERT INTO rehab VALUES (10,'MEADOWBROOK MANOR','OUTPATIENT','3951 EAST BLVD.','(310) 391-8266');


INSERT INTO medicine  VALUES (1,'Sterile Diluent','Cipla');
INSERT INTO medicine  VALUES (2,'Amyvid','GSK');
INSERT INTO medicine  VALUES (3,'TAUVID','Johnson');
INSERT INTO medicine  VALUES (4,'TAUVID','Pfizer');
INSERT INTO medicine  VALUES (5,'Trulicity','Cipla');
INSERT INTO medicine  VALUES (6,'Trulicity','Pfizer');
INSERT INTO medicine  VALUES (7,'EMGALITY','Novartis');
INSERT INTO medicine  VALUES (8,'TALTZ','GSK');
INSERT INTO medicine  VALUES (9,'MOUNJARO','Johnson');
INSERT INTO medicine  VALUES (10,'MOUNJARO','Cipla');


insert into patienttable values(1, "Adam Carlsen", "+1-637-2133-232", "18 Beacon st, boston, MA", "adamcarlsen@gmail.com",md5('pass@123'));
insert into patienttable values(2, "Patrick Teal", "+1-232-5664-897", "343 mels lane, boston, MA", "patrickt23@gmail.com",md5('abc@123'));
insert into patienttable values(3, "Emily Ford", "+1-578-2307-878", "777 hanover sq, newton, MA", "emilyford8@gmail.com",md5('password@123'));
insert into patienttable values(4, "Seth hawthorne", "+1-575-3269-776", "212 Boylston st, boston, MA", "hawthorneseth3@gmail.com",md5('pass@123'));
insert into patienttable values(5, "Jennifer A", "+1-637-8708-244", "45 new hill st, boston, MA", "ajennifer98@gmail.com",md5('abc@123'));
insert into patienttable values(6, "Kevin", "+1-877-4833-876", "321 newman st, boston, MA", "kevinbolton06@gmail.com",md5('password@123'));
insert into patienttable values(7, "Max fischer", "+1-532-3455-837", "4 brooks lane, boston, MA", "fischermax3@gmail.com",md5('pass@123'));
insert into patienttable values(8, "Rory Morris", "+1-879-8368-329", "156 lane st, boston, MA", "rorymorris@gmail.com",md5('abc@123'));
insert into patienttable values(9, "Phyllis Scott", "+1-677-4324-765", "4544 newman st, boston, MA", "phyllisscott@gmail.com",md5('pass@123'));
insert into patienttable values(10, "Carl Sutton", "+1-632-3827-927", "20 Beacon st, boston, MA", "carlsutton211@gmail.com",md5('password@123'));


insert into rehab_appt values (1,1,1,'2022-12-01 12:00:00');
insert into rehab_appt values (2,2,2,'2022-12-03 10:00:00');
insert into rehab_appt values (3,3,3,'2022-12-05 11:00:00');
insert into rehab_appt values (4,4,4,'2022-12-23 09:00:00');
insert into rehab_appt values (5,5,5,'2023-01-05 14:00:00');
insert into rehab_appt values (6,6,6,'2022-12-19 15:00:00');
insert into rehab_appt values (7,7,7,'2023-01-17 19:00:00');
insert into rehab_appt values (8,8,8,'2022-12-10 16:00:00');
insert into rehab_appt values (9,9,9,'2022-12-09 14:00:00');
insert into rehab_appt values (10,10,10,'2022-12-08 13:00:00');



insert into appointmenttable values(1,1, 2);
insert into appointmenttable values(2,2, 6);
insert into appointmenttable values(3,3, 12);
insert into appointmenttable values(4,4, 7);
insert into appointmenttable values(5,5, 9);
insert into appointmenttable values(6,6, 4);
insert into appointmenttable values(7,7, 3);
insert into appointmenttable values(8,8, 2);
insert into appointmenttable values(9,9, 10);
insert into appointmenttable values(10,10, 5);




insert into diagnosis values(1,1,2,12);
insert into diagnosis values(2,2,4,11);
insert into diagnosis values(3,3,8,6);
insert into diagnosis values(4,4,7,8);
insert into diagnosis values(5,5,14,2);
insert into diagnosis values(6,6,12,9);
insert into diagnosis values(7,7,14,2);
insert into diagnosis values(8,8,7,8);
insert into diagnosis values(9,9,17,7);
insert into diagnosis values(10,10,20,9);


insert into treatment values(1,1,1,'50mg', 4, 1);
insert into treatment values(2,2,2,'100mg', 2, 1);
insert into treatment values(3,3, 3,'50mg', 4, 1);
insert into treatment values(4,4,4 ,'30mg', 5, 1);
insert into treatment values(5,5,5,'100mg', 3, 1);
insert into treatment values(6,6,6,'30mg', 2, 1);
insert into treatment values(7,7,7,'25mg', 5, 1);
insert into treatment values(8,8,8,'50mg', 1, 1);
insert into treatment values(9,9,9,'25mg', 3, 1);
insert into treatment values(10,10,10,'25mg', 4, 1);

insert into questdiag values(1,1,now());
insert into questdiag values(2,2,now());
insert into questdiag values(3,3,now());
insert into questdiag values(4,4,now());
insert into questdiag values(5,5,now());
insert into questdiag values(6,6,now());
insert into questdiag values(7,7,now());
insert into questdiag values(8,8,now());
insert into questdiag values(9,9,now());
insert into questdiag values(10,10,now());

insert into patientscore values(1,1,12);
insert into patientscore values(2,2,1);
insert into patientscore values(2,2,2);
insert into patientscore values(2,2,6);
insert into patientscore values(3,3,9);
insert into patientscore values(4,4,8);
insert into patientscore values(5,5,10);
insert into patientscore values(6,6,5);
insert into patientscore values(6,6,11);
insert into patientscore values(7,7,3);
insert into patientscore values(7,7,8);
insert into patientscore values(8,8,1);
insert into patientscore values(8,8,2);
insert into patientscore values(9,9,5);
insert into patientscore values(9,9,11);
insert into patientscore values(10,10,3);
insert into patientscore values(10,10,5);

delimiter $$
CREATE PROCEDURE book_appointment(
in patientID int,
in SID int
)
BEGIN
DECLARE EXIT HANDLER FOR 1062 SELECT 'Duplicate keys error encountered' Message;
DECLARE EXIT HANDLER FOR 1452 SELECT 'Incorrect keys error encountered' Message;
insert into appointmenttable(patientID,SID) values (patientID, SID);
END $$

CREATE PROCEDURE new_patientscore(
in pID int,
in qID int,
in dID int
)
BEGIN
DECLARE EXIT HANDLER FOR 1062 SELECT 'Duplicate keys error encountered' Message;
DECLARE EXIT HANDLER FOR 1452 SELECT 'Incorrect keys error encountered' Message;
insert into patientscore values(pID,qID,dID);
END $$

CREATE PROCEDURE new_questionnaire(
in pID int
)
BEGIN
insert into questdiag(patientID, Date_Taken) values(pID,now());
END $$

CREATE PROCEDURE rehab_appointment(
in rID int,
in pID int,
in admit datetime
)
BEGIN
DECLARE EXIT HANDLER FOR 1062 SELECT 'Duplicate keys error encountered' Message;
DECLARE EXIT HANDLER FOR 1452 SELECT 'Incorrect keys error encountered' Message;
insert into rehab_appt(rehab_id, patientID, admit_datetime) values(rID,pID,admit);
END $$

CREATE PROCEDURE user_registration(
in uname varchar(25),
in contact_num varchar(15),
in address varchar(50),
in email varchar(50),
in pass varchar(50))
BEGIN
    insert into patienttable (Pname,Pcontact_num,Paddress,Pemail,Ppass) values(
    uname, contact_num, address, email, MD5(pass));
END $$

delimiter ;



delimiter $$
create procedure new_therapist(
 in did varchar(20),
 in name varchar(50),
 in clinic varchar(50),
 in number varchar(50),
 in pass varchar(5)
 )
 begin
 insert into therapist(DID,tname,tclinic,tnum,Ppass) values (did,name,clinic,number,MD5(pass)) ;
 end $$
 delimiter ;
 



delimiter $$
create procedure new_schedule_for_therapist(
 in tid int,
 in day varchar(50),
 in timestart varchar(50),
 in timeend varchar(50)
 )
 begin
 insert into scheduletable(TID,day,timestart,timeend) values (tid,day,timestart,timeend) ;
 end $$
 delimiter ;


delimiter $$
create procedure check_schedule_for_therapist(
 in tid int
 )
 begin
select *from scheduletable where TID=tid;
 end $$
 delimiter ;


delimiter $$
create procedure delete_schedule_for_therapist(
 in sid int
 )
 begin
 delete from scheduletable where SID=sid;
 end $$
 delimiter ;
 
 
 delimiter $$
create procedure check_appointment_for_therapist(
 in tid int
 )
 begin
 select * from scheduletable s, appointmenttable a where s.SID=a.SID and TID=tid; 
 end $$
 delimiter ;

 delimiter $$
create procedure therapist_diagnosis(
 in pid int,
 in tid int,
 in did int
)
 begin
 insert into diagnosis(patientID,TID,DID) values (pid,tid,did) ;
 end $$
 delimiter ;
 
 
 
delimiter $$
create procedure therapist_treatment(
 in did int,
 in mid int,
 in dosage varchar(50),
 in ndays varchar(20),
 in rrc bit 
)
 begin
 insert into treatment(diagnosis_id,med_id,dosage,num_days,Rehab_recommendation) values (did,mid,dosage,ndays,rrc) ;
 end $$
 delimiter ;
 
 call therapist_treatment(4,5,'45mg',2,0)







delimiter $$
create procedure add_treatment(in PatientID INT, in TID INT, in med_id INT, 
							in dosage varchar(20), in num_days varchar(20))
begin

	Set @DiagnosisID = (select diagnosis_id from diagnosis where patientID = @PatientID and TID=@TID);

	insert into treatment(diagnosis_id, med_id, dosage, num_days) 
	values (@DiagnosisID, med_id, dosage, num_days);
	end $$
delimiter ;

call add_treatment(1,1,2,'50mg',6);
 

delimiter $$
create function therapist_countby_domain(DID INT)
returns int
deterministic
begin
		declare domain_count int;
        
        select count(*) into domain_count
        from therapist
        where therapist.DID=DID;
        
        return domain_count;
end $$
delimiter ; 

delimiter $$
create function patients_under_therapist(tid INT)
returns int
deterministic

begin
	declare patient_count int;
    
    select count(distinct patientID) into patient_count
    from diagnosis
    where diagnosis.TID=tid;
    
    return patient_count;
end $$
delimiter ;


delimiter $$
create function most_patients_in_domain()
returns varchar(200)
deterministic
begin
	declare domain varchar(200);
    
    set domain = (select do.illness from diagnosis d, domainofillness do
    where d.DID = do.DID
    group by d.DID
    order by count(*) DESC
    limit 1);
    
    return domain;
end $$
delimiter ;

delimiter $$
create function patients_in_rehab(rehab_id int)
returns int
deterministic
begin
	declare patients_count int;
    
    select count(*) into patients_count
    from rehab r, rehab_appt ra
    where r.rehab_id=ra.rehab_id
    and ra.rehab_id=rehab_id;
    
    return patients_count;
		
end$$
delimiter ;

delimiter $$
create function most_popular_therapist()
returns varchar(50)
deterministic
begin
	
    declare therap varchar(50);
    
    select t.tname into therap
    from diagnosis d, therapist t
    where d.TID=t.TID
    group by d.TID
    order by count(*) DESC
    limit 1;
    
    return therap;
    
end	$$
delimiter ;

create view phistory as 
select pname,p.patientID,illness 
from patienttable p,diagnosis d 
join domainofillness i 
where p.patientID=d.patientID and d.DID=i.DID ;


create view medicine_for_diagnosis as 
select * from diagnosis 
natural join 
(select *from medicine natural join treatment) as p;


select * from medicine_for_diagnosis;
select illness,max(mcount) 
from (select count(*) as mcount,illness 
	 from medicine_for_diagnosis natural join domainofillness 
     group by illness) as t;
     
DELIMITER $$
CREATE TRIGGER before_patient_insert
BEFORE INSERT
ON patienttable 
FOR EACH ROW
BEGIN
    IF (NEW.Pcontact_num = '') THEN
        SET NEW.Pcontact_num = 'NA';
    END IF;
    
END$$

DELIMITER ;
     
-- drop trigger after_patient_insert;
-- DELIMITER $$
-- CREATE TRIGGER after_patient_insert
-- AFTER INSERT
-- ON patienttable FOR EACH ROW
-- BEGIN
--     IF (NEW.Pcontact_num = '') THEN
--         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Please enter a valid number ';
--     -- ELSEIF (NEW.med_id IS NULL) THEN
-- --         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Please enter medicine id ';
-- -- 	ELSEIF NEW.dosage IS NULL THEN
-- --         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Please enter dosage ';
-- --     ELSEIF NEW.num_days IS NULL THEN
-- --         SIGNAL SQLSTATE '45000' SET MESSAGE_TEXT = 'Please enter num of days ';
--     END IF;
--     
-- END$$

-- DELIMITER ;
