-- MySQL dump 10.13  Distrib 8.0.38, for Win64 (x86_64)
--
-- Host: localhost    Database: buhgalteria
-- ------------------------------------------------------
-- Server version	8.0.32

/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!50503 SET NAMES utf8 */;
/*!40103 SET @OLD_TIME_ZONE=@@TIME_ZONE */;
/*!40103 SET TIME_ZONE='+00:00' */;
/*!40014 SET @OLD_UNIQUE_CHECKS=@@UNIQUE_CHECKS, UNIQUE_CHECKS=0 */;
/*!40014 SET @OLD_FOREIGN_KEY_CHECKS=@@FOREIGN_KEY_CHECKS, FOREIGN_KEY_CHECKS=0 */;
/*!40101 SET @OLD_SQL_MODE=@@SQL_MODE, SQL_MODE='NO_AUTO_VALUE_ON_ZERO' */;
/*!40111 SET @OLD_SQL_NOTES=@@SQL_NOTES, SQL_NOTES=0 */;

--
-- Table structure for table `categories`
--

DROP TABLE IF EXISTS `categories`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `categories` (
  `category_id` int NOT NULL AUTO_INCREMENT,
  `category_name` varchar(100) NOT NULL,
  PRIMARY KEY (`category_id`)
) ENGINE=InnoDB AUTO_INCREMENT=27 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `categories`
--

LOCK TABLES `categories` WRITE;
/*!40000 ALTER TABLE `categories` DISABLE KEYS */;
INSERT INTO `categories` VALUES (1,'Продукты'),(2,'Транспорт'),(3,'Развлечение'),(4,'Коммунальные услуги'),(5,'Медицинские расходы'),(6,'Спорт'),(7,'Путешествия'),(8,'Книги'),(9,'Образование'),(10,'Техника'),(11,'Казино'),(12,'Оборудование');
/*!40000 ALTER TABLE `categories` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `expenses`
--

DROP TABLE IF EXISTS `expenses`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `expenses` (
  `expense_id` int NOT NULL AUTO_INCREMENT,
  `category_id` int NOT NULL,
  `amount` decimal(10,2) NOT NULL,
  `expense_date` datetime NOT NULL,
  `description_` varchar(255) DEFAULT NULL,
  `user_id` int DEFAULT NULL,
  PRIMARY KEY (`expense_id`),
  KEY `category_id` (`category_id`),
  KEY `user foreign_idx` (`user_id`),
  CONSTRAINT `expenses_ibfk_1` FOREIGN KEY (`category_id`) REFERENCES `categories` (`category_id`) ON DELETE CASCADE,
  CONSTRAINT `user foreign` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`)
) ENGINE=InnoDB AUTO_INCREMENT=34 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `expenses`
--

LOCK TABLES `expenses` WRITE;
/*!40000 ALTER TABLE `expenses` DISABLE KEYS */;
INSERT INTO `expenses` VALUES (1,1,1500.00,'2023-10-01 00:00:00','Купил в пятерочке',1),(2,2,2000.00,'2023-10-05 00:00:00','Оплата за продукты',2),(3,3,500.00,'2023-10-03 00:00:00','Бензин',3),(4,4,1200.00,'2023-10-10 00:00:00','В кино',1),(5,5,3000.00,'2023-10-15 00:00:00','Газ',2),(6,1,1000.00,'2023-10-02 00:00:00','Продукты',3),(7,1,800.00,'2023-10-07 00:00:00','Фрукты',1),(8,2,400.00,'2023-10-04 00:00:00','Автобус',1),(9,3,1500.00,'2023-10-08 00:00:00','Транспорт',2),(10,4,3000.00,'2023-10-12 00:00:00','Книга',3),(11,5,2500.00,'2023-10-18 00:00:00','Курсы английского',1),(12,6,5000.00,'2023-10-25 00:00:00','Абонемент спортзал',2),(13,7,12000.00,'2023-10-30 00:00:00','Новый ноутбук',3),(14,3,1200.00,'2024-08-30 00:00:00','Парк развлечений',1),(15,6,1500.00,'2024-08-31 00:00:00','Поход в зал',1),(16,2,1500.00,'2024-11-18 00:00:00','В зал',1),(18,4,1111.00,'2024-11-28 00:00:00','За квартиру',8),(19,1,1500.00,'2024-11-01 00:00:00','Покупка продуктов в супермаркете',1),(20,2,500.00,'2024-11-02 00:00:00','Проезд на такси',1),(21,3,1200.00,'2024-11-05 00:00:00','Билеты в кинотеатр',1),(23,4,3000.00,'2024-11-07 00:00:00','Оплата аренды жилья',1),(24,1,1000.00,'2024-11-08 00:00:00','Продукты на неделю',1),(25,2,350.00,'2024-11-09 00:00:00','Проезд на автобусе',1),(26,3,600.00,'2024-11-10 00:00:00','Поход в кафе',1),(27,5,800.00,'2024-11-11 00:00:00','Медицинские услуги',1),(28,4,3200.00,'2024-11-12 00:00:00','Оплата коммунальных услуг',1),(29,1,1500.00,'2024-11-01 00:00:00','Закупка продуктов',1),(30,2,300.00,'2024-11-02 00:00:00','Проезд на такси',1);
/*!40000 ALTER TABLE `expenses` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `reports`
--

DROP TABLE IF EXISTS `reports`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `reports` (
  `report_id` int NOT NULL AUTO_INCREMENT,
  `user_id` int NOT NULL,
  `report_date` datetime DEFAULT CURRENT_TIMESTAMP,
  `total_expenses` decimal(10,2) DEFAULT '0.00',
  PRIMARY KEY (`report_id`),
  KEY `user_id` (`user_id`),
  CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`) ON DELETE CASCADE
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `reports`
--

LOCK TABLES `reports` WRITE;
/*!40000 ALTER TABLE `reports` DISABLE KEYS */;
INSERT INTO `reports` VALUES (1,1,'2024-11-26 10:57:09',3500.00),(2,2,'2024-11-26 10:57:09',4200.00),(3,3,'2024-11-26 10:57:09',2500.00),(4,1,'2024-11-26 11:11:54',3500.00),(5,2,'2024-11-26 11:11:54',4200.00),(6,3,'2024-11-26 11:11:54',4000.00),(7,4,'2024-11-26 11:11:54',3000.00),(8,5,'2024-11-26 11:11:54',12000.00);
/*!40000 ALTER TABLE `reports` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `users`
--

DROP TABLE IF EXISTS `users`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `users` (
  `user_id` int NOT NULL AUTO_INCREMENT,
  `username` varchar(50) NOT NULL,
  `password` varchar(225) NOT NULL,
  PRIMARY KEY (`user_id`),
  UNIQUE KEY `username` (`username`)
) ENGINE=InnoDB AUTO_INCREMENT=9 DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `users`
--

LOCK TABLES `users` WRITE;
/*!40000 ALTER TABLE `users` DISABLE KEYS */;
INSERT INTO `users` VALUES (1,'ivanov','password123'),(2,'petrov','mypassword'),(3,'sidorov','securepass'),(4,'smirnov','mypassword123'),(5,'kuznetsov','qwerty'),(6,'volkov','letmein'),(7,'glolovnya','123'),(8,'1','1');
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

-- Dump completed on 2024-12-02 12:51:21
