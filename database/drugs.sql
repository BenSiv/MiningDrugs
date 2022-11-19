-- MySQL dump 10.13  Distrib 8.0.31, for Linux (x86_64)
--
-- Host: localhost    Database: drugs
-- ------------------------------------------------------
-- Server version	8.0.31-0ubuntu2

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
-- Table structure for table `drug_medical_conditions`
--

DROP TABLE IF EXISTS `drug_medical_conditions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drug_medical_conditions` (
  `id` int NOT NULL,
  `drug_id` int NOT NULL,
  `medical_conditions_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `drug_id` (`drug_id`),
  KEY `medical_conditions_id` (`medical_conditions_id`),
  CONSTRAINT `drug_medical_conditions_ibfk_1` FOREIGN KEY (`drug_id`) REFERENCES `drugs` (`id`),
  CONSTRAINT `drug_medical_conditions_ibfk_2` FOREIGN KEY (`medical_conditions_id`) REFERENCES `medical_conditions` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drug_medical_conditions`
--

LOCK TABLES `drug_medical_conditions` WRITE;
/*!40000 ALTER TABLE `drug_medical_conditions` DISABLE KEYS */;
/*!40000 ALTER TABLE `drug_medical_conditions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drug_side_effects`
--

DROP TABLE IF EXISTS `drug_side_effects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drug_side_effects` (
  `id` int NOT NULL,
  `drug_id` int NOT NULL,
  `side_effect_id` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `drug_id` (`drug_id`),
  KEY `side_effect_id` (`side_effect_id`),
  CONSTRAINT `drug_side_effects_ibfk_1` FOREIGN KEY (`drug_id`) REFERENCES `drugs` (`id`),
  CONSTRAINT `drug_side_effects_ibfk_2` FOREIGN KEY (`side_effect_id`) REFERENCES `side_effects` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drug_side_effects`
--

LOCK TABLES `drug_side_effects` WRITE;
/*!40000 ALTER TABLE `drug_side_effects` DISABLE KEYS */;
/*!40000 ALTER TABLE `drug_side_effects` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `drugs`
--

DROP TABLE IF EXISTS `drugs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `drugs` (
  `id` int NOT NULL,
  `drug_name` varchar(255) DEFAULT NULL,
  `scientific_name` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `drugs`
--

LOCK TABLES `drugs` WRITE;
/*!40000 ALTER TABLE `drugs` DISABLE KEYS */;
/*!40000 ALTER TABLE `drugs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `medical_conditions`
--

DROP TABLE IF EXISTS `medical_conditions`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `medical_conditions` (
  `id` int NOT NULL,
  `medical_conditions_name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `medical_conditions`
--

LOCK TABLES `medical_conditions` WRITE;
/*!40000 ALTER TABLE `medical_conditions` DISABLE KEYS */;
/*!40000 ALTER TABLE `medical_conditions` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `related_drugs`
--

DROP TABLE IF EXISTS `related_drugs`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `related_drugs` (
  `id` int NOT NULL,
  `drug_id` int NOT NULL,
  `related` int NOT NULL,
  PRIMARY KEY (`id`),
  KEY `drug_id` (`drug_id`),
  KEY `related` (`related`),
  CONSTRAINT `related_drugs_ibfk_1` FOREIGN KEY (`drug_id`) REFERENCES `drugs` (`id`),
  CONSTRAINT `related_drugs_ibfk_2` FOREIGN KEY (`related`) REFERENCES `drugs` (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `related_drugs`
--

LOCK TABLES `related_drugs` WRITE;
/*!40000 ALTER TABLE `related_drugs` DISABLE KEYS */;
/*!40000 ALTER TABLE `related_drugs` ENABLE KEYS */;
UNLOCK TABLES;

--
-- Table structure for table `side_effects`
--

DROP TABLE IF EXISTS `side_effects`;
/*!40101 SET @saved_cs_client     = @@character_set_client */;
/*!50503 SET character_set_client = utf8mb4 */;
CREATE TABLE `side_effects` (
  `id` int NOT NULL,
  `side_effects_name` varchar(255) DEFAULT NULL,
  `description` varchar(255) DEFAULT NULL,
  PRIMARY KEY (`id`)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_0900_ai_ci;
/*!40101 SET character_set_client = @saved_cs_client */;

--
-- Dumping data for table `side_effects`
--

LOCK TABLES `side_effects` WRITE;
/*!40000 ALTER TABLE `side_effects` DISABLE KEYS */;
/*!40000 ALTER TABLE `side_effects` ENABLE KEYS */;
UNLOCK TABLES;
/*!40103 SET TIME_ZONE=@OLD_TIME_ZONE */;

/*!40101 SET SQL_MODE=@OLD_SQL_MODE */;
/*!40014 SET FOREIGN_KEY_CHECKS=@OLD_FOREIGN_KEY_CHECKS */;
/*!40014 SET UNIQUE_CHECKS=@OLD_UNIQUE_CHECKS */;
/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
/*!40111 SET SQL_NOTES=@OLD_SQL_NOTES */;

-- Dump completed on 2022-11-19 14:23:55
