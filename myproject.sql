-- MySQL dump 10.13  Distrib 8.3.0, for macos14.2 (x86_64)
--
-- Host: localhost    Database: myproject
-- ------------------------------------------------------
-- Server version	8.1.0

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8mb4 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `auth_group`
--

DROP TABLE IF EXISTS `auth_group`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(150) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `name` (`name`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group`
--

LOCK TABLES `auth_group` WRITE;
/*!40000 ALTER TABLE `auth_group` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_group_permissions`
--

DROP TABLE IF EXISTS `auth_group_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_group_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `group_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_group_permissions_group_id_permission_id_0cd325b0_uniq` (`group_id`,`permission_id`),
  KEY `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_group_permissio_permission_id_84c5c92e_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_group_permissions_group_id_b120cbf9_fk_auth_group_id` FOREIGN KEY (`group_id`) REFERENCES `auth_group` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_group_permissions`
--

LOCK TABLES `auth_group_permissions` WRITE;
/*!40000 ALTER TABLE `auth_group_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_group_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_permission`
--

DROP TABLE IF EXISTS `auth_permission`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_permission` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(255) NOT NULL,
  `content_type_id` int NOT NULL,
  `codename` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_permission_content_type_id_codename_01ab375a_uniq` (`content_type_id`,`codename`),
  CONSTRAINT `auth_permission_content_type_id_2f476e4b_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=69 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_permission`
--

LOCK TABLES `auth_permission` WRITE;
/*!40000 ALTER TABLE `auth_permission` DISABLE KEYS */;
INSERT INTO `auth_permission` VALUES (1,'Can add log entry',1,'add_logentry'),(2,'Can change log entry',1,'change_logentry'),(3,'Can delete log entry',1,'delete_logentry'),(4,'Can view log entry',1,'view_logentry'),(5,'Can add permission',2,'add_permission'),(6,'Can change permission',2,'change_permission'),(7,'Can delete permission',2,'delete_permission'),(8,'Can view permission',2,'view_permission'),(9,'Can add group',3,'add_group'),(10,'Can change group',3,'change_group'),(11,'Can delete group',3,'delete_group'),(12,'Can view group',3,'view_group'),(13,'Can add user',4,'add_user'),(14,'Can change user',4,'change_user'),(15,'Can delete user',4,'delete_user'),(16,'Can view user',4,'view_user'),(17,'Can add content type',5,'add_contenttype'),(18,'Can change content type',5,'change_contenttype'),(19,'Can delete content type',5,'delete_contenttype'),(20,'Can view content type',5,'view_contenttype'),(21,'Can add session',6,'add_session'),(22,'Can change session',6,'change_session'),(23,'Can delete session',6,'delete_session'),(24,'Can view session',6,'view_session'),(25,'Can add daily activity',7,'add_dailyactivity'),(26,'Can change daily activity',7,'change_dailyactivity'),(27,'Can delete daily activity',7,'delete_dailyactivity'),(28,'Can view daily activity',7,'view_dailyactivity'),(29,'Can add my model',8,'add_mymodel'),(30,'Can change my model',8,'change_mymodel'),(31,'Can delete my model',8,'delete_mymodel'),(32,'Can view my model',8,'view_mymodel'),(33,'Can add user',9,'add_user'),(34,'Can change user',9,'change_user'),(35,'Can delete user',9,'delete_user'),(36,'Can view user',9,'view_user'),(37,'Can add financial record',10,'add_financialrecord'),(38,'Can change financial record',10,'change_financialrecord'),(39,'Can delete financial record',10,'delete_financialrecord'),(40,'Can view financial record',10,'view_financialrecord'),(41,'Can add investing record',11,'add_investingrecord'),(42,'Can change investing record',11,'change_investingrecord'),(43,'Can delete investing record',11,'delete_investingrecord'),(44,'Can view investing record',11,'view_investingrecord'),(45,'Can add contact',12,'add_contact'),(46,'Can change contact',12,'change_contact'),(47,'Can delete contact',12,'delete_contact'),(48,'Can view contact',12,'view_contact'),(49,'Can add income record',13,'add_incomerecord'),(50,'Can change income record',13,'change_incomerecord'),(51,'Can delete income record',13,'delete_incomerecord'),(52,'Can view income record',13,'view_incomerecord'),(53,'Can add meeting',14,'add_meeting'),(54,'Can change meeting',14,'change_meeting'),(55,'Can delete meeting',14,'delete_meeting'),(56,'Can view meeting',14,'view_meeting'),(57,'Can add monthly expense',15,'add_monthlyexpense'),(58,'Can change monthly expense',15,'change_monthlyexpense'),(59,'Can delete monthly expense',15,'delete_monthlyexpense'),(60,'Can view monthly expense',15,'view_monthlyexpense'),(61,'Can add note',16,'add_note'),(62,'Can change note',16,'change_note'),(63,'Can delete note',16,'delete_note'),(64,'Can view note',16,'view_note'),(65,'Can add sleep log',17,'add_sleeplog'),(66,'Can change sleep log',17,'change_sleeplog'),(67,'Can delete sleep log',17,'delete_sleeplog'),(68,'Can view sleep log',17,'view_sleeplog');
/*!40000 ALTER TABLE `auth_permission` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user`
--

DROP TABLE IF EXISTS `auth_user`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user` (
  `id` int NOT NULL AUTO_INCREMENT,
  `password` varchar(128) NOT NULL,
  `last_login` datetime(6) DEFAULT NULL,
  `is_superuser` tinyint(1) NOT NULL,
  `username` varchar(150) NOT NULL,
  `first_name` varchar(150) NOT NULL,
  `last_name` varchar(150) NOT NULL,
  `email` varchar(254) NOT NULL,
  `is_staff` tinyint(1) NOT NULL,
  `is_active` tinyint(1) NOT NULL,
  `date_joined` datetime(6) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user`
--

LOCK TABLES `auth_user` WRITE;
/*!40000 ALTER TABLE `auth_user` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `auth_user_user_permissions`
--

DROP TABLE IF EXISTS `auth_user_user_permissions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `auth_user_user_permissions` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `permission_id` int NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `auth_user_user_permissions_user_id_permission_id_14a6b632_uniq` (`user_id`,`permission_id`),
  KEY `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` (`permission_id`),
  CONSTRAINT `auth_user_user_permi_permission_id_1fbb5f2c_fk_auth_perm` FOREIGN KEY (`permission_id`) REFERENCES `auth_permission` (`id`),
  CONSTRAINT `auth_user_user_permissions_user_id_a95ead1b_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `auth_user_user_permissions`
--

LOCK TABLES `auth_user_user_permissions` WRITE;
/*!40000 ALTER TABLE `auth_user_user_permissions` DISABLE KEYS */;
/*!40000 ALTER TABLE `auth_user_user_permissions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `contacts`
--

DROP TABLE IF EXISTS `contacts`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `contacts` (
  `id` int NOT NULL AUTO_INCREMENT,
  `name` varchar(100) NOT NULL,
  `phone_number` varchar(20) NOT NULL,
  `note` text,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=32 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `contacts`
--

LOCK TABLES `contacts` WRITE;
/*!40000 ALTER TABLE `contacts` DISABLE KEYS */;
INSERT INTO `contacts` VALUES (18,'Херопрактор От Виктора Галины сын','3476663456','Записаться ',34),(20,'Tatiana Miami','1 3059512580','Tatiana Miami Lazer',34),(21,'Cndela Lazer','929 280 58 43','Laser associate',34),(23,'Mike Regina   Ultherapy','516 864 1389','',34),(24,'14B Michel','9176791516','Tennis',34),(25,'Pain Manager from Alexey 14E','7189989890','',34),(26,'Stomatologist','(718) 416-6364','2952 Brighton 3rd St suite 501, Brooklyn, NY 11235',34),(27,'Louis Recruter | BHI Bank Hapoalim','+1 6465178526','',34),(30,'Recruter for onboarding BHI bank','517 347 7609','',34),(31,'Vitia from Emir','929 488 6985','',34);
/*!40000 ALTER TABLE `contacts` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_admin_log`
--

DROP TABLE IF EXISTS `django_admin_log`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_admin_log` (
  `id` int NOT NULL AUTO_INCREMENT,
  `action_time` datetime(6) NOT NULL,
  `object_id` longtext,
  `object_repr` varchar(200) NOT NULL,
  `action_flag` smallint unsigned NOT NULL,
  `change_message` longtext NOT NULL,
  `content_type_id` int DEFAULT NULL,
  `user_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `django_admin_log_content_type_id_c4bce8eb_fk_django_co` (`content_type_id`),
  KEY `django_admin_log_user_id_c564eba6_fk_auth_user_id` (`user_id`),
  CONSTRAINT `django_admin_log_content_type_id_c4bce8eb_fk_django_co` FOREIGN KEY (`content_type_id`) REFERENCES `django_content_type` (`id`),
  CONSTRAINT `django_admin_log_user_id_c564eba6_fk_auth_user_id` FOREIGN KEY (`user_id`) REFERENCES `auth_user` (`id`),
  CONSTRAINT `django_admin_log_chk_1` CHECK ((`action_flag` >= 0))
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_admin_log`
--

LOCK TABLES `django_admin_log` WRITE;
/*!40000 ALTER TABLE `django_admin_log` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_admin_log` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_content_type`
--

DROP TABLE IF EXISTS `django_content_type`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_content_type` (
  `id` int NOT NULL AUTO_INCREMENT,
  `app_label` varchar(100) NOT NULL,
  `model` varchar(100) NOT NULL,
  PRIMARY KEY (`id`),
  UNIQUE KEY `django_content_type_app_label_model_76bd3d3b_uniq` (`app_label`,`model`)
) ENGINE=InnoDB AUTO_INCREMENT=18 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_content_type`
--

LOCK TABLES `django_content_type` WRITE;
/*!40000 ALTER TABLE `django_content_type` DISABLE KEYS */;
INSERT INTO `django_content_type` VALUES (1,'admin','logentry'),(3,'auth','group'),(2,'auth','permission'),(4,'auth','user'),(5,'contenttypes','contenttype'),(12,'myapp','contact'),(7,'myapp','dailyactivity'),(10,'myapp','financialrecord'),(13,'myapp','incomerecord'),(11,'myapp','investingrecord'),(14,'myapp','meeting'),(15,'myapp','monthlyexpense'),(8,'myapp','mymodel'),(16,'myapp','note'),(17,'myapp','sleeplog'),(9,'myapp','user'),(6,'sessions','session');
/*!40000 ALTER TABLE `django_content_type` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_migrations`
--

DROP TABLE IF EXISTS `django_migrations`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_migrations` (
  `id` bigint NOT NULL AUTO_INCREMENT,
  `app` varchar(255) NOT NULL,
  `name` varchar(255) NOT NULL,
  `applied` datetime(6) NOT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=21 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_migrations`
--

LOCK TABLES `django_migrations` WRITE;
/*!40000 ALTER TABLE `django_migrations` DISABLE KEYS */;
INSERT INTO `django_migrations` VALUES (1,'contenttypes','0001_initial','2024-03-21 17:50:17.516775'),(2,'auth','0001_initial','2024-03-21 17:50:17.662804'),(3,'admin','0001_initial','2024-03-21 17:50:17.698362'),(4,'admin','0002_logentry_remove_auto_add','2024-03-21 17:50:17.713361'),(5,'admin','0003_logentry_add_action_flag_choices','2024-03-21 17:50:17.717819'),(6,'contenttypes','0002_remove_content_type_name','2024-03-21 17:50:17.748033'),(7,'auth','0002_alter_permission_name_max_length','2024-03-21 17:50:17.782927'),(8,'auth','0003_alter_user_email_max_length','2024-03-21 17:50:17.799401'),(9,'auth','0004_alter_user_username_opts','2024-03-21 17:50:17.804493'),(10,'auth','0005_alter_user_last_login_null','2024-03-21 17:50:17.825481'),(11,'auth','0006_require_contenttypes_0002','2024-03-21 17:50:17.826684'),(12,'auth','0007_alter_validators_add_error_messages','2024-03-21 17:50:17.832519'),(13,'auth','0008_alter_user_username_max_length','2024-03-21 17:50:17.851367'),(14,'auth','0009_alter_user_last_name_max_length','2024-03-21 17:50:17.870350'),(15,'auth','0010_alter_group_name_max_length','2024-03-21 17:50:17.880355'),(16,'auth','0011_update_proxy_permissions','2024-03-21 17:50:17.884746'),(17,'auth','0012_alter_user_first_name_max_length','2024-03-21 17:50:17.913897'),(18,'myapp','0001_initial','2024-03-21 17:50:17.919281'),(19,'sessions','0001_initial','2024-03-21 17:50:17.930171'),(20,'myapp','0002_contact_investingrecord_amount_at_maturity_and_more','2024-06-11 18:51:38.444747');
/*!40000 ALTER TABLE `django_migrations` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `django_session`
--

DROP TABLE IF EXISTS `django_session`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `django_session` (
  `session_key` varchar(40) NOT NULL,
  `session_data` longtext NOT NULL,
  `expire_date` datetime(6) NOT NULL,
  PRIMARY KEY (`session_key`),
  KEY `django_session_expire_date_a5c62663` (`expire_date`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `django_session`
--

LOCK TABLES `django_session` WRITE;
/*!40000 ALTER TABLE `django_session` DISABLE KEYS */;
/*!40000 ALTER TABLE `django_session` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `financial_records`
--

DROP TABLE IF EXISTS `financial_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `financial_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `record_date` date DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `financial_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=361 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `financial_records`
--

LOCK TABLES `financial_records` WRITE;
/*!40000 ALTER TABLE `financial_records` DISABLE KEYS */;
INSERT INTO `financial_records` VALUES (93,34,'2024-04-30','T-mobil for aprile ',99.00),(130,37,'2024-05-01','dengi na veter',4823023.00),(131,37,'2024-05-01','Veter',11.00),(134,34,'2024-05-02','New Expense',200.00),(137,34,'2024-05-04','Tea&sweets',8.00),(138,34,'2024-05-04','Drink ',7.00),(139,34,'2024-05-04','Buth',3.00),(141,34,'2024-05-06','Car',150.00),(142,34,'2024-05-06','Drink',5.00),(144,34,'2024-05-07','gas',35.00),(145,34,'2024-05-07','Salads BBQ neighbors',35.00),(146,34,'2024-05-07','Mama restaurant ',45.00),(147,34,'2024-05-07','Gas',45.00),(150,34,'2024-05-08','Trimmer',20.00),(151,34,'2024-05-08','post',6.00),(152,34,'2024-05-08','drink ',12.00),(154,34,'2024-05-09','Mama Document notorization',60.00),(155,34,'2024-05-09','Eat',28.00),(156,34,'2024-05-09','Mama pharmacy',35.00),(157,34,'2024-05-10','Mama Flight',800.00),(158,34,'2024-05-10','Mama uber ',60.00),(159,34,'2024-05-10','Mama Dovidka',200.00),(160,34,'2024-05-10','Touchpad',185.00),(161,34,'2024-05-12','Drink Shipshead bay',5.00),(162,34,'2024-05-13','Food Ruslan',25.00),(163,34,'2024-05-13','T-mobile',140.00),(164,34,'2024-05-13','Food',28.00),(165,34,'2024-05-13','Car',150.00),(166,34,'2024-05-13','Food',32.00),(174,34,'2024-05-14','Car Gas',63.00),(176,34,'2024-05-14','Food ',42.00),(177,34,'2024-05-14','Key',15.00),(178,34,'2024-05-15','Food',52.00),(179,44,'2024-05-15','investing in Vlad',111111.00),(180,34,'2024-05-16','food ',23.00),(181,45,'2024-05-16','Car ticket',80.00),(192,34,'2024-05-17','Food',34.00),(193,34,'2024-05-18','Food ',35.00),(194,34,'2024-05-18','Smoothy Food',10.00),(195,34,'2024-05-18','Champaign',35.00),(196,34,'2024-05-18','Food ',33.00),(197,34,'2024-05-19','Food ',4.50),(198,34,'2024-05-20','Food',10.00),(200,34,'2024-05-21','Car Rent',110.00),(201,34,'2024-05-21','Girl Rooftop',200.00),(202,34,'2024-05-21','Food',40.00),(203,34,'2024-05-22','Car Gas',55.00),(204,34,'2024-05-22','Mama Flight',145.00),(205,34,'2024-05-22','Chat GPT',22.00),(209,34,'2024-05-23','Food',8.00),(210,46,'2024-05-23','Test',1000.00),(211,36,'2024-05-10','Groceries',150.00),(212,36,'2024-05-15','Utilities',100.00),(213,36,'2024-05-20','Dining Out',75.00),(214,36,'2024-05-01','Rent',1200.00),(215,36,'2024-05-02','Internet',60.00),(216,36,'2024-05-03','Transportation',50.00),(217,36,'2024-05-04','Shopping',200.00),(218,36,'2024-05-05','Entertainment',80.00),(219,36,'2024-05-06','Medical',150.00),(220,36,'2024-05-07','Insurance',100.00),(222,34,'2024-05-28','Food Starbucks',20.00),(223,34,'2024-05-28','Food',42.00),(224,34,'2024-05-29','Car Rent',160.00),(225,34,'2024-05-29','Car gas ',33.00),(226,34,'2024-05-29','Food ',9.00),(227,34,'2024-05-30','Car gas',40.00),(228,34,'2024-05-30','Food ',46.00),(229,34,'2024-05-30','Rent apt',2512.00),(230,34,'2024-05-31','Food ',23.00),(231,34,'2024-05-31','Botulax',300.00),(232,34,'2024-05-31','Food ',45.00),(233,34,'2024-06-01','Food',12.00),(234,34,'2024-06-01','Mama food ',52.00),(235,34,'2024-06-01','Mama',7.00),(236,34,'2024-06-01','Work Authorization',55.00),(237,34,'2024-06-01','EAD',470.00),(238,34,'2024-06-02','Food Smoothy',12.00),(239,34,'2024-06-02','Food smoothy',12.00),(240,34,'2024-06-02','Food',43.00),(241,34,'2024-06-03','Mama Food',9.00),(242,34,'2024-06-03','Clothse',70.00),(243,34,'2024-06-03','mama closing',75.00),(244,34,'2024-06-04','Food',7.00),(245,34,'2024-06-04','Food',36.00),(246,34,'2024-06-04','Mama Hyaron',80.00),(247,34,'2024-06-04','Train ',12.00),(248,34,'2024-06-04','Electricity ',120.00),(249,34,'2024-06-05','Food smoothy ',7.00),(250,34,'2024-06-05','Train',3.00),(251,34,'2024-06-06','Food',35.00),(252,34,'2024-06-06','Mama food ',57.00),(253,34,'2024-06-06','Mama Fis rostvor ',35.00),(254,36,'2024-06-06','Amazon',1000.00),(256,34,'2024-06-06','Mama Food',40.00),(257,34,'2024-06-06','Mama food',8.00),(258,34,'2024-06-06','Food smoothy ',10.00),(259,34,'2024-06-06','Filler Revolax',228.00),(260,34,'2024-06-08','Food ',50.00),(261,34,'2024-06-09','Food Smoothy',10.00),(262,34,'2024-06-10','Food Smoothy',10.00),(263,34,'2024-06-10','Food ',35.00),(265,34,'2024-06-11','Food',10.00),(266,34,'2024-06-11','Food Smoothy',10.00),(267,34,'2024-06-11','Food',66.00),(268,34,'2024-06-12','Girl food ',170.00),(269,34,'2024-06-12','Girl Car ',100.00),(270,34,'2024-06-12','Конюля Mama ',30.00),(271,34,'2024-06-12','Gas Car',30.00),(272,34,'2024-06-12','Food Smoothy ',10.00),(273,34,'2024-06-12','Food',24.00),(275,34,'2024-06-13','Food Smoothy',10.00),(276,34,'2024-06-13','T mobil',80.00),(277,34,'2024-06-13','Anna Mirentieva Mama',225.00),(278,34,'2024-06-13','Mama Food ',23.00),(279,34,'2024-06-14','Food Burger',9.00),(280,34,'2024-06-14','Food Smoothy',8.00),(281,34,'2024-06-14','Food ',30.00),(282,34,'2024-06-14','mama food ',40.00),(283,34,'2024-06-14','Vlad Chair',8800.00),(284,34,'2024-06-14','Ruslan Vlad',70.00),(285,34,'2024-06-14','Mama',70.00),(286,34,'2024-06-16','Food',20.00),(287,34,'2024-06-16','Mama Igor BRSD',50.00),(288,34,'2024-06-16','Food ',35.00),(289,34,'2024-06-17','Food ',27.00),(290,34,'2024-06-18','Food',35.00),(292,34,'2024-06-19','Mama Flight ',285.00),(293,34,'2024-06-19','Loundry ',10.00),(294,34,'2024-06-19','Mama Food ',31.00),(295,34,'2024-06-21','Food',47.00),(296,34,'2024-06-21','Mama',5.00),(297,34,'2024-06-21','Facebook',35.00),(298,34,'2024-06-21','Mama Food',12.00),(299,34,'2024-06-22','Food mama',10.00),(300,34,'2024-06-22','Food ',80.00),(301,34,'2024-06-23','Gopro',300.00),(302,34,'2024-06-23','Tmir parking',4.00),(303,34,'2024-06-24','Loundry',10.00),(304,34,'2024-06-24','Food ',38.00),(305,34,'2024-06-25','Food',28.00),(306,34,'2024-06-25','Mama flight',1280.00),(307,34,'2024-06-25','Apt Rent July',2512.00),(308,34,'2024-06-26','Food Smooth',8.00),(309,34,'2024-06-26','Mama',9.00),(310,34,'2024-06-26','Food',9.00),(311,34,'2024-06-26','Beauty tattoo cream',38.00),(312,34,'2024-06-26','Facebook',35.00),(313,34,'2024-06-27','Food',24.00),(314,34,'2024-06-27','Food',43.00),(315,34,'2024-06-28','Food',25.00),(316,34,'2024-06-28','Botex Beauty',300.00),(317,34,'2024-06-29','Mama',53.00),(318,34,'2024-06-29','Uber mama',57.00),(319,34,'2024-06-29','Mama',35.00),(320,34,'2024-06-30','Vlad Amazon',15.00),(321,34,'2024-06-30','Mama uber miami',40.00),(322,34,'2024-06-30','Food',15.00),(323,34,'2024-06-30','Vlad Footbal ',4.00),(324,34,'2024-07-01','Food',78.00),(325,34,'2024-07-01','Vlad Doctor main Menegment',25.00),(326,34,'2024-07-02','Food Manhattan Ruslan ',70.00),(327,34,'2024-07-02','Card Fo go pro ',50.00),(328,34,'2024-07-02','Train',3.00),(329,34,'2024-07-02','T mobil',76.00),(332,34,'2024-07-03','Footbal',10.00),(333,34,'2024-07-03','Electricity',82.00),(334,36,'2024-07-04','Food',47.00),(335,36,'2024-07-04','Mama Uber ',15.00),(336,36,'2024-07-04','Food ',15.00),(337,34,'2024-07-05','Food',42.00),(338,34,'2024-07-06','Food',40.00),(339,34,'2024-07-06','Mama bag for airport',50.00),(340,34,'2024-07-06','Oatmilk',56.00),(341,34,'2024-07-07','Mama ',28.00),(342,34,'2024-07-08','Tennis ',250.00),(343,34,'2024-07-08','eda',40.00),(344,34,'2024-07-09','Food ',34.00),(345,34,'2024-07-09','Mama food ',12.00),(346,34,'2024-07-10','Donation',5.00),(347,34,'2024-07-10','Mama HomeEttand',300.00),(348,34,'2024-07-12','mama ',6.00),(349,34,'2024-07-12','Water',30.00),(350,34,'2024-07-12','food ',14.00),(351,34,'2024-07-12','Amazon insole ',23.00),(352,34,'2024-07-13','T mobil',82.00),(353,34,'2024-07-13','Food shaurma with Ruslan',26.00),(354,34,'2024-07-13','Food',14.00),(355,34,'2024-07-14','Food ',55.00),(356,34,'2024-07-14','Emir euro 2024',15.00),(357,34,'2024-07-14','Food',15.00),(358,34,'2024-07-15','Udemy courc',17.00),(359,34,'2024-07-15','domain https://domains.squarespace.com/domain-search',12.00),(360,34,'2024-07-15','Mama flight ',1520.00);
/*!40000 ALTER TABLE `financial_records` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_insert_financial_record` AFTER INSERT ON `financial_records` FOR EACH ROW BEGIN
    DECLARE week_start DATE;
    DECLARE month_start DATE;
    DECLARE year_start DATE;

    SET week_start = DATE_SUB(NEW.record_date, INTERVAL WEEKDAY(NEW.record_date) DAY);
    SET month_start = DATE_SUB(NEW.record_date, INTERVAL DAY(NEW.record_date) - 1 DAY);
    SET year_start = DATE_SUB(NEW.record_date, INTERVAL DAYOFYEAR(NEW.record_date) - 1 DAY);

    -- Update the user's financial summary and decrease the balance
    UPDATE users
    SET 
        money_spent = money_spent + NEW.amount,
        spent_by_week = (
            SELECT COALESCE(SUM(amount), 0)
            FROM financial_records
            WHERE user_id = NEW.user_id AND record_date >= week_start AND record_date < DATE_ADD(week_start, INTERVAL 7 DAY)
        ),
        spent_by_month = (
            SELECT COALESCE(SUM(amount), 0)
            FROM financial_records
            WHERE user_id = NEW.user_id AND record_date >= month_start AND record_date < DATE_ADD(month_start, INTERVAL 1 MONTH)
        ),
        spent_by_year = (
            SELECT COALESCE(SUM(amount), 0)
            FROM financial_records
            WHERE user_id = NEW.user_id AND record_date >= year_start AND record_date < DATE_ADD(year_start, INTERVAL 1 YEAR)
        ),
        balance = balance - NEW.amount
    WHERE id = NEW.user_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_delete_financial_record` AFTER DELETE ON `financial_records` FOR EACH ROW BEGIN
    DECLARE week_start DATE;
    DECLARE month_start DATE;
    DECLARE year_start DATE;

    SET week_start = DATE_SUB(OLD.record_date, INTERVAL WEEKDAY(OLD.record_date) DAY);
    SET month_start = DATE_SUB(OLD.record_date, INTERVAL DAY(OLD.record_date) - 1 DAY);
    SET year_start = DATE_SUB(OLD.record_date, INTERVAL DAYOFYEAR(OLD.record_date) - 1 DAY);

    -- Update the user's financial summary and increase the balance
    UPDATE users
    SET 
        money_spent = money_spent - OLD.amount,
        spent_by_week = (
            SELECT COALESCE(SUM(amount), 0)
            FROM financial_records
            WHERE user_id = OLD.user_id AND record_date >= week_start AND record_date < DATE_ADD(week_start, INTERVAL 7 DAY)
        ),
        spent_by_month = (
            SELECT COALESCE(SUM(amount), 0)
            FROM financial_records
            WHERE user_id = OLD.user_id AND record_date >= month_start AND record_date < DATE_ADD(month_start, INTERVAL 1 MONTH)
        ),
        spent_by_year = (
            SELECT COALESCE(SUM(amount), 0)
            FROM financial_records
            WHERE user_id = OLD.user_id AND record_date >= year_start AND record_date < DATE_ADD(year_start, INTERVAL 1 YEAR)
        ),
        balance = balance + OLD.amount
    WHERE id = OLD.user_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `income_records`
--

DROP TABLE IF EXISTS `income_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `income_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `record_date` date NOT NULL,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `income_records_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=116 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `income_records`
--

LOCK TABLES `income_records` WRITE;
/*!40000 ALTER TABLE `income_records` DISABLE KEYS */;
INSERT INTO `income_records` VALUES (49,46,'Test',1000.00,'2024-05-23'),(50,46,'Test2',2000.00,'2024-05-23'),(51,36,'Salary',2000.00,'2024-05-05'),(52,36,'Freelance Work',800.00,'2024-05-14'),(53,36,'Bonus',300.00,'2024-05-21'),(54,36,'Interest',150.00,'2024-05-01'),(55,36,'Dividends',200.00,'2024-05-02'),(56,36,'Gift',100.00,'2024-05-03'),(57,36,'Rent Income',500.00,'2024-05-04'),(58,36,'Part-Time Job',600.00,'2024-05-05'),(59,36,'Sale of Goods',250.00,'2024-05-06'),(60,36,'Consulting',700.00,'2024-05-07'),(61,36,'Amazon',15000.00,'2024-01-16'),(62,36,'Amazon',10000.00,'2023-12-06'),(63,36,'Amazon',20000.00,'2023-01-16'),(64,36,'Amazon',10000.00,'2023-02-02'),(67,36,'Amazon',5000.00,'2023-02-23'),(68,36,'amazon',9000.00,'2024-03-21'),(69,36,'Amazon',15000.00,'2024-05-15'),(71,34,'Mama',80.00,'2024-05-30'),(72,34,'Atria',817.00,'2024-05-31'),(73,34,'Mama ',100.00,'2024-05-31'),(74,34,'Mama',150.00,'2024-05-31'),(76,34,'Mama',420.00,'2024-06-03'),(78,34,'ruslan',44.00,'2024-06-05'),(79,34,'Mama',720.00,'2024-06-05'),(80,34,'Mama ',200.00,'2024-06-06'),(81,34,'Mama',600.00,'2024-06-09'),(82,34,'Mama Cards',600.00,'2024-06-09'),(83,34,'Mama',720.00,'2024-06-12'),(84,34,'Mama',150.00,'2024-06-12'),(85,34,'Mama',340.00,'2024-06-11'),(86,34,'Mama',240.00,'2024-06-13'),(87,34,'Mama',180.00,'2024-06-14'),(88,34,'Mama cards',600.00,'2024-06-17'),(89,34,'Mama ',108.00,'2024-06-17'),(93,34,'Mama',115.00,'2024-06-18'),(94,34,'Mama ',150.00,'2024-06-18'),(96,34,'Mama',410.00,'2024-06-24'),(97,34,'Mama',100.00,'2024-06-24'),(98,34,'Mama',210.00,'2024-06-24'),(99,34,'Mama Food stamp',380.00,'2024-06-03'),(100,34,'Mama',60.00,'2024-06-25'),(101,34,'Мама ',380.00,'2024-06-26'),(102,34,'Mama',980.00,'2024-06-27'),(103,34,'Mama',100.00,'2024-06-27'),(104,34,'Mama ',120.00,'2024-06-28'),(105,34,'Mama',648.00,'2024-07-01'),(108,34,'Mama',370.00,'2024-07-04'),(109,34,'Mama',260.00,'2024-07-07'),(112,34,'Mama ',170.00,'2024-07-08'),(113,36,'Test',1000.00,'2024-07-11'),(114,34,'Mama',570.00,'2024-07-12'),(115,34,'Mama',250.00,'2024-07-12');
/*!40000 ALTER TABLE `income_records` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `investing_records`
--

DROP TABLE IF EXISTS `investing_records`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `investing_records` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `record_date` date DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT NULL,
  `tenor` varchar(255) DEFAULT NULL,
  `type_invest` varchar(255) DEFAULT NULL,
  `amount_at_maturity` decimal(15,2) DEFAULT NULL,
  `rate` decimal(5,2) DEFAULT NULL,
  `maturity_date` date DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB AUTO_INCREMENT=46 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `investing_records`
--

LOCK TABLES `investing_records` WRITE;
/*!40000 ALTER TABLE `investing_records` DISABLE KEYS */;
INSERT INTO `investing_records` VALUES (22,46,'2024-05-21','Main',100000.00,'1','Real Estate',112000.00,12.00,'2025-05-21'),(45,36,'2024-07-11','Main investing',100000.00,'20','ETFs',386968.45,7.00,'2044-07-06');
/*!40000 ALTER TABLE `investing_records` ENABLE KEYS */;
UNLOCK TABLES;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_insert_investment_record` AFTER INSERT ON `investing_records` FOR EACH ROW BEGIN
    -- Update the user's investment summary and decrease the balance
    UPDATE users
    SET 
        money_invested = money_invested + NEW.amount,
        balance = balance - NEW.amount
    WHERE id = NEW.user_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;
/*!50003 SET @saved_cs_client      = @@character_set_client */ ;
/*!50003 SET @saved_cs_results     = @@character_set_results */ ;
/*!50003 SET @saved_col_connection = @@collation_connection */ ;
/*!50003 SET character_set_client  = utf8mb4 */ ;
/*!50003 SET character_set_results = utf8mb4 */ ;
/*!50003 SET collation_connection  = utf8mb4_0900_ai_ci */ ;
/*!50003 SET @saved_sql_mode       = @@sql_mode */ ;
/*!50003 SET sql_mode              = 'ONLY_FULL_GROUP_BY,STRICT_TRANS_TABLES,NO_ZERO_IN_DATE,NO_ZERO_DATE,ERROR_FOR_DIVISION_BY_ZERO,NO_ENGINE_SUBSTITUTION' */ ;
DELIMITER ;;
/*!50003 CREATE*/ /*!50017 DEFINER=`root`@`localhost`*/ /*!50003 TRIGGER `after_delete_investment_record` AFTER DELETE ON `investing_records` FOR EACH ROW BEGIN
    -- Update the user's investment summary and increase the balance
    UPDATE users
    SET 
        money_invested = money_invested - OLD.amount,
        balance = balance + OLD.amount
    WHERE id = OLD.user_id;
END */;;
DELIMITER ;
/*!50003 SET sql_mode              = @saved_sql_mode */ ;
/*!50003 SET character_set_client  = @saved_cs_client */ ;
/*!50003 SET character_set_results = @saved_cs_results */ ;
/*!50003 SET collation_connection  = @saved_col_connection */ ;

--
-- Table structure for table `meetings`
--

DROP TABLE IF EXISTS `meetings`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `meetings` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(255) NOT NULL,
  `datetime` datetime NOT NULL,
  `done` tinyint(1) DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `meetings_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=63 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `meetings`
--

LOCK TABLES `meetings` WRITE;
/*!40000 ALTER TABLE `meetings` DISABLE KEYS */;
INSERT INTO `meetings` VALUES (15,46,'Test','2024-05-21 14:00:00',0),(22,34,'Eanglish class','2024-06-11 16:57:00',1),(30,34,'Cardio','2024-06-13 00:34:00',1),(32,34,'Cardio','2024-06-23 21:32:00',1),(33,34,'Cardio','2024-06-25 14:21:00',1),(34,34,'Teath clean 1 pm','2024-07-02 01:23:00',1),(35,34,'Pain manager 2279 Cony island ave 2 floor 11223 3pm','2024-07-01 23:00:00',1),(36,34,'KingsBorow Your appointment is confirmed for: 07/17/2024 at 03:30 PM Room - M108','2024-07-17 15:30:00',0),(37,34,'Cardio','2024-06-28 02:26:00',1),(38,34,'Cardio','2024-06-30 00:35:00',1),(40,34,'Cardio','2024-06-30 18:23:00',1),(41,34,'Main interview','2024-07-10 15:00:00',1),(42,34,'Tatiana Dental 2:30 Wednsday','2024-07-03 14:59:00',1),(52,34,'Dental at monday 2.30 pm; 2952 Brighton Third St Unit 501 Brooklyn, NY  11235 United States','2024-07-08 14:30:00',1),(54,34,'Cardio','2024-07-02 16:03:00',1),(57,36,'test','2024-07-05 08:05:00',0),(58,34,'Cardio','2024-07-04 14:27:00',1),(59,34,'Cardio','2024-07-04 14:27:00',1),(60,34,'Pain menegment','2024-07-11 09:45:00',1),(61,34,'Interview','2024-07-10 12:00:00',1),(62,34,'MRI at 7 pm ','2024-07-18 19:00:00',0);
/*!40000 ALTER TABLE `meetings` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `monthly_expenses`
--

DROP TABLE IF EXISTS `monthly_expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `monthly_expenses` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `title` varchar(255) DEFAULT NULL,
  `amount` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `monthly_expenses_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=33 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `monthly_expenses`
--

LOCK TABLES `monthly_expenses` WRITE;
/*!40000 ALTER TABLE `monthly_expenses` DISABLE KEYS */;
INSERT INTO `monthly_expenses` VALUES (13,34,'Rent Apt',2512.00),(14,34,'Internet',60.00),(17,34,'Utilities ',70.00),(22,45,'Rent',2800.00),(24,46,'Rent apt',2700.00),(25,46,'Car ',800.00),(27,34,'App',22.00),(29,36,'Car',800.00),(31,36,'Test',222.00),(32,34,'Phone mom and me and watch',96.00);
/*!40000 ALTER TABLE `monthly_expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `notes`
--

DROP TABLE IF EXISTS `notes`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `notes` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int DEFAULT NULL,
  `title` varchar(255) DEFAULT NULL,
  `note` text,
  `date` date DEFAULT NULL,
  `priority` text,
  `done` tinyint(1) DEFAULT '0',
  `hide` tinyint(1) DEFAULT '0',
  `order` int NOT NULL DEFAULT '0',
  PRIMARY KEY (`id`),
  KEY `fk_notes_user` (`user_id`),
  CONSTRAINT `fk_notes_user` FOREIGN KEY (`user_id`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=129 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `notes`
--

LOCK TABLES `notes` WRITE;
/*!40000 ALTER TABLE `notes` DISABLE KEYS */;
INSERT INTO `notes` VALUES (4,36,'Test','TestNote','2024-05-04','High Priority',1,1,2),(5,36,'Updated Note Title','Test','2024-05-04','High Priority',1,1,1),(6,34,'Random Note','This is a random note added for testing purposes.','2024-05-10','Medium Priority',1,1,3),(7,36,'Test Note','Test22',NULL,'',0,1,1),(8,36,'Test Note','This is a test note.',NULL,'',0,1,2),(9,36,'Test Note','This is a test note.',NULL,'',0,1,3),(10,36,'Test Note','This is a test note.',NULL,'',0,1,4),(11,36,'Test Note','This is a test note.',NULL,'',0,1,5),(12,36,'Test Note','This is a test note.',NULL,'',0,1,6),(13,36,'Test Note','This is a test note.','2024-04-25','High Priority',1,1,10),(14,36,'Test33','Test23223','2024-05-06','High Priority',1,1,11),(15,36,'Test2','Test23','2024-05-06','',0,1,7),(16,36,'Test','Test','2024-05-06','High Priority',0,1,1),(17,34,'Insert add buttons in each modal to increase space ','Insert add buttons in each modal to increase space ','2024-05-06','Low Priority',1,1,14),(18,34,'Priority filtering ','Make that if exist notes with different priaority type it should filter first hight priority then midle and then low','2024-05-06','Low Priority',1,1,15),(19,34,'Time ','Add time above the user data title ','2024-05-06','Low Priority',1,1,16),(20,34,'Note Descriptions ','make that if descrioption is more then 12 simvols then show \"...\" and on hover show full description ','2024-05-06','Low Priority',1,1,17),(21,36,'Test33','Test23','2024-05-06','High Priority',0,1,3),(22,34,'Monthly expenses ','Monthly expenses modal ','2024-05-07','Low Priority',1,1,19),(23,34,'Chanhe logo','Monthly expenses ','2024-05-07','Low Priority',1,1,20),(24,34,'Create logo modal','Create logo modal','2024-05-07','Low Priority',1,1,21),(25,34,'Cosmetick course ','Search for cosmetick course ','2024-05-07','Medium Priority',1,1,7),(26,34,'Touch pad','buy touch pad','2024-05-07','Low Priority',1,1,23),(27,34,'Rudolph KCCollage','Aks which documents he need ','2024-05-07','Medium Priority',1,1,24),(28,34,'Trimmer attachment','Buy trimmer attachment','2024-05-07','Medium Priority',1,1,25),(29,34,'User data','Update user data','2024-05-07','Low Priority',1,1,26),(30,34,'Loundry','Loundry','2024-05-08','Medium Priority',1,1,27),(31,34,'Modal widths','Modal widths','2024-05-08','Low Priority',1,1,28),(32,34,'Create express clone for django ','Create express clone for django ','2024-05-08','Low Priority',1,1,16),(33,34,'Send Laptop','Send Laptop','2024-05-08','Medium Priority',1,1,30),(34,34,'Lounge zone ','Ask Galina to Close the lounge zone at 11 pm','2024-05-08','Medium Priority',1,1,31),(35,34,'Alt Station','Ask what is the time and cost of delivering','2024-05-08','Medium Priority',1,1,32),(36,34,'Green Card ','Check green holder ','2024-05-08','Medium Priority',1,1,33),(37,34,'Financial Aid ','Room V201 till 5:30pm','2024-05-08','Medium Priority',1,1,34),(38,34,'Data','Add data that to disply money spent by last month and week','2024-05-08','Low Priority',1,1,35),(39,34,'Cash assistens ','Extend the Cash assistens ','2024-05-09','Medium Priority',1,1,36),(40,34,'Work Authorization ','Extend Work Authorization ','2024-05-09','Medium Priority',1,1,1),(41,34,'Find the job Remoutly','Dice, Indeed','2024-05-09','High Priority',1,1,6),(42,34,'Touch Pad','Touch Pad','2024-05-10','Medium Priority',1,1,39),(43,34,'Ira','Ask Ira about co-working, and advertizing of laser ','2024-05-10','Medium Priority',1,1,7),(44,34,'Yan ','Ask for selling the Apt, car, restaurant ','2024-05-10','Medium Priority',1,1,6),(45,34,'Working Developer / 2 projects ','Working Developer / 2 projects ','2024-05-10','High Priority',0,0,9),(46,34,'Nurse / Doctor','Nurse / Stomatologist','2024-05-10','High Priority',0,0,10),(47,34,'Financial advisor','Financial advisor','2024-05-10','High Priority',0,0,12),(48,41,'Cat','Give food','2024-05-10','High Priority',0,1,45),(49,34,'data Add, delete','Make that we can add, update, delete the investing','2024-05-10','Low Priority',1,1,46),(50,34,'Note refresh','Note refresh after adding','2024-05-10','Low Priority',1,1,47),(51,34,'Investing type rate','Make modal which allo to see the interest base in the investing type, amount and tenor','2024-05-10','Low Priority',1,1,48),(52,34,'Horisontal button','Make Note, Spending, Investing buttons be horisontal ','2024-05-10','Low Priority',1,1,49),(53,34,'Amount of notes ','Add the Amount of notes lane at the notes modal ','2024-05-10','Low Priority',1,1,50),(54,34,'Carusel','Fix the carusel ','2024-05-10','Low Priority',1,1,51),(55,34,'Notes order','We should be able to change the order of notes when we press on the note and transfer it to the new place it the list','2024-05-10','Low Priority',1,1,1),(56,34,'Title, Note updating','We should be able to update title and description of the note','2024-05-10','Low Priority',1,1,1),(57,34,'User Photo','Create the modal to upload the photo of the user ','2024-05-10','Low Priority',1,1,2),(58,34,'Chart of Balance, Spending ','Create the chart to see the amount for the balance for each week and month +','2024-05-10','Low Priority',1,1,2),(59,34,'Companies','Need to open compoanies of :\n1. Investing (Accounting) \n2. Medicine service \n3. Law servise \n4. Insurance \n5. Building ','2024-05-10','High Priority',0,0,13),(60,34,'Green card / insurance ','1. Need to connect with Irian loweyr in Miami, to expedite the case process \n2. Need to get insurance to make the injections of blocada ','2024-05-10','High Priority',1,1,7),(61,34,'Champain','Champain for Vadim','2024-05-10','Medium Priority',1,1,4),(62,34,'Green Card ','Green Card Acceleration \n\n- Sertification that I completed Politech\n\n- 20 serctifications\n\n- That I was judge some turnire ','2024-05-11','Medium Priority',0,0,19),(63,34,'Insurance ','Open Insurance Because no work','2024-05-11','Medium Priority',1,1,15),(64,34,'Glass for toothbrushes','Glass for toothbrushes','2024-05-11','Medium Priority',1,1,5),(65,36,'Test121','Test121','2024-05-13','High Priority',0,1,2),(66,36,'Test','Test','2024-05-13','Low Priority',0,1,2),(67,34,'Income','Fix That when we add income Balance should increase or decrease','2024-05-14','Low Priority',1,1,4),(68,34,'Horisontal','Make buttons, tasks, income, spendings, investing hotisontal','2024-05-14','Low Priority',1,1,5),(69,34,'Income table','Income table with columns user_id, amount, source','2024-05-14','Low Priority',1,1,3),(70,34,'Make 3 sections','1) user Data. 2) income 3) Spendings ','2024-05-14','Low Priority',1,1,7),(71,34,'New crocs','New crocs','2024-05-14','Medium Priority',1,1,3),(72,34,'New crocs','New crocs','2024-05-14','Medium Priority',1,1,11),(73,34,'Contacts Modal','Contacts modal for user which have is_superuser = 1','2024-05-15','Low Priority',1,1,5),(74,34,'Maturity date ','Add maturity date for Investing ','2024-05-15','Low Priority',1,1,6),(75,34,'Condition Cleaning','Condition Cleaning 11.30 am 28 May','2024-05-16','Medium Priority',1,1,9),(76,34,'Make data bigger','Make data bigger, one the left data, on the right buttons ','2024-05-16','Low Priority',1,1,73),(77,36,'Test','Test22','2024-05-16','Low Priority',1,1,1),(78,36,'Test','test22','2024-05-16','High Priority',1,1,1),(79,36,'Vlad','Buzhor','2024-05-16','High Priority',0,1,2),(80,45,'Test','Test2','2024-05-16','Low Priority',0,0,0),(81,34,'Delete spendings ','Delete spendings and update ','2024-05-16','Low Priority',1,1,1),(82,34,'Drop Down spendings','Drop Down spendings by month, year','2024-05-16','Low Priority',1,1,0),(83,36,'Test','test','2024-05-17','Medium Priority',1,1,0),(84,34,'Adnular project','Create angular project for medicine and cosmethologist','2024-05-17','Low Priority',1,1,3),(85,34,'Work Authorization','1. ФИО на англ - Бужор Влад Анатолиевич \n2. Дата рождения, город рождения -  04.27.1996\n3. Номер паспорта, дата истечения срока действия \n    number - ER886611\n    exiration - 27 Nov 2026\n4. Фото формы 94 (если есть) \n5. Адрес в США - 221 Sea breeze ave apt 13E\n6. ФИО родителей на англ -  Buzhor Diana \n7. Контактный номер - 3474308497\n8. Эл. почта  - pritzkervlad@gmail.com\n9. Получали ли вы ранее SSN? - Yes\n10. Дата и место пересечения границы США - June 22 2017 \n   JFK\n11. А-номер  - A216-224-023\n12. Семейное положение - Single \n','2024-05-17','Medium Priority',1,1,5),(86,34,'Advertizing','Реклама для Эпиляции, Hifu, Hidrofacial, Уборка тату ','2024-05-17','Medium Priority',1,1,1),(87,34,'Mama','Buy Phone For Mama ','2024-05-18','Medium Priority',1,1,14),(88,34,'Ira Manhattan','Вторник на 5 30\nЧетверг на 10 30 ','2024-05-19','Medium Priority',1,1,0),(89,46,'Client ','Schedule the apoinment fo client','2024-05-21','High Priority',0,1,2),(90,46,'Go to Vlad','Amidiatly ','2024-05-21','High Priority',1,0,1),(91,34,'Selenium','Selenium Python project','2024-05-22','Low Priority',1,1,20),(92,34,'Income ','1. Fix issue when we add income it should be added to the balance.\n2. Add Income by month, and year.\n','2024-05-22','Low Priority',1,1,0),(93,34,'Clothes','Treaser and jacket, t-shirt, Nordstrom','2024-05-22','Medium Priority',1,1,2),(94,36,'Presentation','For generalassemb','2024-05-23','High Priority',0,0,0),(95,34,'Financial Aid','Check with Rudolph that al is good ','2024-05-24','Medium Priority',1,1,1),(96,34,'Angular','1. User Dashboard:\n    * Create a dashboard where users can see their profile, health history, and upcoming appointments.\n    * Allow users to update their personal information and health details.','2024-05-28','Low Priority',0,0,5),(97,34,'Angular','2. Symptom Checker:\n    * Develop a symptom checker where users can input their symptoms and receive suggestions on the type of doctor they might need to see.\n    * Use a questionnaire format to guide users through describing their symptoms.','2024-05-28','Low Priority',0,0,7),(98,34,'Angular','3. Doctor Specialties:\n    * Provide information on different types of doctors and their specialties (e.g., general practitioners, cardiologists, dermatologists).\n    * Include a search feature to find doctors based on the user\'s symptoms or condition.','2024-05-28','Low Priority',0,0,8),(99,34,'Angular','4. Appointment Scheduling:\n    * Implement a system for booking appointments with doctors.\n    * Allow users to see available times, book, reschedule, or cancel appointments.','2024-05-28','Low Priority',0,0,11),(100,34,'Angular','5. Health Resources:\n    * Offer articles, videos, and other resources on common health issues and preventive care.\n    * Include tips on maintaining a healthy lifestyle.','2024-05-28','Low Priority',0,0,16),(101,34,'Angular','6. Consultation Types:\n    * Provide options for different types of consultations (e.g., in-person, telehealth).\n    * Explain the benefits and limitations of each type.','2024-05-28','Low Priority',0,0,17),(102,34,'Angular','7. Emergency Information:\n    * Provide information on what to do in case of an emergency.\n    * Include emergency contact numbers and steps to take.','2024-05-28','Low Priority',0,0,18),(103,34,'Renew the Card Snap','Renew the Card Snap','2024-06-01','Medium Priority',1,1,0),(104,34,'KingsBoro collage','- Eanglish class at 9 : 30 on 06 11 Building T 7 7119 room\n- Schedule the online meeting to set up the classes for Fall 2024\n- Apply for dream financial aid \n- ask what is the next step ','2024-06-01','Medium Priority',0,0,4),(105,34,'Lazer','1. Write to cosmetic associate Check which  laser to buy\n2. Buy\n3. Advertizing \n4. Cabinet in manhattan \n5. Buy SMAS\n6. Buy Hair removal lazer\n7. Buy RF lazer\n8. Buy Hydro facial lazer\n','2024-06-01','Medium Priority',1,1,0),(106,34,'Ask Lower','Ask Loyer where I can see the status of my case in the USCIS site','2024-06-01','Medium Priority',1,1,0),(107,34,'Financial','Fix time of meeting display','2024-06-01','Low Priority',1,1,3),(108,34,'Day Plan','Create Day plan feature \n- Mama add\n- Job search\n- Project\n- Order the chair\n- Buy phone for mam\n- Check which lazer to buy','2024-06-02','Low Priority',1,1,1),(109,34,'Day Plan','Today:\n- Touro collage\n- Set up mama Instagram for ads\n- Make an ad for SMAS\n- Search for a job\n- Project fixing \n\n\nNext day:\n1.\n2.\n3. ','2024-06-02','High Priority',1,1,1),(110,34,'Main Tasks','1. Buy a chair.\n    - Make ads for SMAS (!)\n2. Buy hair remove mochine for mom.\n3. Search for the job.\n    - Buy courses for Botox\n    - Buy courses for Filler\n    - Buy courses for \n      Biorevitalization\n4. \n    - Start study in KingsBorow collage for the nursing program\n\n5. As soon mon earn money, buy a Hair removal and Smas machine and a Hydrofacial machine.\n6. Buy real botox\n7. Study at Dental school\n','2024-06-02','High Priority',1,1,2),(111,34,'Ads for mom','Create add that mom did biotritalization and pacient get merri','2024-06-03','Medium Priority',1,1,0),(112,48,'Hit Tatiana','Noooww','2024-06-05','High Priority',0,0,2),(113,48,'Buy sushi','Buy sushi','2024-06-05','High Priority',0,0,1),(114,34,'Day Plan','Create a Day plan feature:\n\n-Assamble the chair\n-Project\n\n\n\n\n\n','2024-06-06','High Priority',0,0,0),(115,34,'Sale','- Chair 1 500$\n- Chair 2 200$\n- Scooter 500$\n- Table extension 200$\n\n','2024-06-08','Medium Priority',1,1,0),(116,34,'React','Create a feature to send the invitation for the meeting if another user accepts, it we add this meeting to both the sender and receiver','2024-06-12','Low Priority',1,1,0),(117,34,'React','Add a feature that we display the notification above the avatar picture which shows if user have a meeting today or a new unread message ','2024-06-12','Low Priority',1,1,0),(118,34,'React ','- Create the notification box Modal\n- Modal to send the message (invitation to the meeitng) \n- On sumbiting it should appear at both sender and reciever \n','2024-06-12','Low Priority',1,1,0),(119,34,'DB beckUp at git hub','DB beckUp at git hub','2024-06-15','Low Priority',1,1,0),(120,36,'Test','test2','2024-06-18','Low Priority',1,0,0),(121,34,'Coding Temple','Coding Temple finish course ','2024-06-22','Medium Priority',0,0,0),(122,34,'Meetings ','1 Time of meetings shwoing note the same as we did\n2 Done checkbox not working','2024-06-26','Low Priority',1,1,0),(123,34,'Balance ','Spendings not minus from the balance value','2024-06-26','Low Priority',1,1,0),(124,34,'Case ',' Take Case from the Loyer','2024-06-30','Medium Priority',1,1,0),(125,34,'Back','Julia - Phisitian Assistent \n- \n- Triger Injections','2024-07-01','Medium Priority',1,1,0),(126,34,'Ruslan for Shaurma ','12$ owe','2024-07-04','Low Priority',1,1,0),(127,34,'Buy sofa','Buy sofa','2024-07-12','Medium Priority',0,0,0),(128,34,'Buy cortain','Buy cortain','2024-07-12','Medium Priority',0,0,0);
/*!40000 ALTER TABLE `notes` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `sleep_logs`
--

DROP TABLE IF EXISTS `sleep_logs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `sleep_logs` (
  `id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `date` date NOT NULL,
  `sleep_time` datetime NOT NULL,
  `wake_time` datetime NOT NULL,
  `created_at` datetime DEFAULT CURRENT_TIMESTAMP,
  PRIMARY KEY (`id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `sleep_logs_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`ID`)
) ENGINE=InnoDB AUTO_INCREMENT=20 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `sleep_logs`
--

LOCK TABLES `sleep_logs` WRITE;
/*!40000 ALTER TABLE `sleep_logs` DISABLE KEYS */;
INSERT INTO `sleep_logs` VALUES (9,34,'2024-07-09','2024-07-09 23:00:00','2024-07-09 08:01:00','2024-07-10 11:58:06'),(12,34,'2024-07-10','2024-07-10 22:25:00','2024-07-10 08:25:00','2024-07-11 16:25:45'),(13,34,'2024-07-11','2024-07-11 21:30:00','2024-07-11 05:35:00','2024-07-11 16:48:51'),(15,34,'2024-07-12','2024-07-12 23:59:00','2024-07-12 05:10:00','2024-07-13 06:18:23'),(16,34,'2024-07-12','2024-07-12 23:59:00','2024-07-12 05:15:00','2024-07-14 06:50:50'),(17,34,'2024-07-13','2024-07-13 21:30:00','2024-07-13 05:00:00','2024-07-14 06:51:25'),(18,34,'2024-07-13','2024-07-13 21:30:00','2024-07-13 05:07:00','2024-07-14 13:07:22'),(19,34,'2024-07-14','2024-07-14 23:59:00','2024-07-14 08:30:00','2024-07-15 08:54:44');
/*!40000 ALTER TABLE `sleep_logs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `ID` int NOT NULL AUTO_INCREMENT,
  `username` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(100) NOT NULL,
  `money_invested` decimal(10,2) DEFAULT '0.00',
  `money_spent` decimal(10,2) DEFAULT '0.00',
  `balance` decimal(10,2) DEFAULT '0.00',
  `last_login` datetime DEFAULT NULL,
  `is_active` tinyint(1) DEFAULT '1',
  `is_staff` tinyint(1) DEFAULT '0',
  `is_superuser` tinyint(1) NOT NULL DEFAULT '0',
  `balance_goal` decimal(10,2) DEFAULT NULL,
  `spent_by_week` decimal(10,2) DEFAULT NULL,
  `spent_by_month` decimal(10,2) DEFAULT NULL,
  `spent_by_year` decimal(10,2) DEFAULT NULL,
  `photo` varchar(100) DEFAULT NULL,
  `income_by_week` decimal(10,2) DEFAULT NULL,
  `income_by_month` decimal(10,2) DEFAULT '0.00',
  `income_by_year` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`ID`),
  UNIQUE KEY `email` (`email`)
) ENGINE=InnoDB AUTO_INCREMENT=49 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (34,'Vlad','Pritzkervlad@gmail.com','pbkdf2_sha256$720000$LPVqXqrl9NvfW2B88JeX7H$uCs9YLL2cMEgzutRyasn+g9EZiv/jYefHEpkvxQNW+E=',0.00,19526.50,121185.00,'2024-04-30 11:20:48',1,0,0,200000.00,1634.00,3080.00,26643.50,'user_34/2024-04-25 19.11.33_fcpCvL0.jpg',0.00,2268.00,11342.00),(36,'TestTest','Test@gmail.com','pbkdf2_sha256$720000$2KlPXI8MABHwG8MymwmnKb$l1ZW/4StzB+qcjE2wmx8yPY12mMwmdrKuk+yT47nInQ=',-800000.00,3175.00,1000000.00,'2024-05-01 12:29:21',1,0,1,500000.00,0.00,77.00,3242.00,'user_36/2024-04-25 19.11.33.jpg',1000.00,1000.00,45600.00);
/*!40000 ALTER TABLE `users` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2024-07-15 12:41:09
