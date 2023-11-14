-- phpMyAdmin SQL Dump
-- version 5.2.0
-- https://www.phpmyadmin.net/
--
-- Host: 127.0.0.1
-- Generation Time: Nov 12, 2023 at 07:03 AM
-- Server version: 10.4.27-MariaDB
-- PHP Version: 8.1.12

SET SQL_MODE = "NO_AUTO_VALUE_ON_ZERO";
START TRANSACTION;
SET time_zone = "+00:00";


/*!40101 SET @OLD_CHARACTER_SET_CLIENT=@@CHARACTER_SET_CLIENT */;
/*!40101 SET @OLD_CHARACTER_SET_RESULTS=@@CHARACTER_SET_RESULTS */;
/*!40101 SET @OLD_COLLATION_CONNECTION=@@COLLATION_CONNECTION */;
/*!40101 SET NAMES utf8mb4 */;

--
-- Database: `ims_db`
--

-- --------------------------------------------------------

--
-- Table structure for table `inventory`
--

CREATE TABLE `inventory` (
  `computer_id` int(11) NOT NULL,
  `mouse` enum('Working','Not Working','Missing') NOT NULL,
  `keyboard` enum('Working','Not Working','Missing') NOT NULL,
  `monitor` enum('Working','Not Working','Missing') NOT NULL,
  `system_unit` enum('Working','Not Working','Missing') NOT NULL,
  `date_added` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `inventory`
--

INSERT INTO `inventory` (`computer_id`, `mouse`, `keyboard`, `monitor`, `system_unit`, `date_added`) VALUES
(1, 'Working', 'Working', 'Not Working', 'Working', '2023-11-04 18:55:24'),
(2, 'Missing', 'Missing', 'Missing', 'Missing', '2023-11-04 18:07:36'),
(3, 'Working', 'Not Working', 'Working', 'Missing', '2023-11-02 11:28:17'),
(4, 'Working', 'Working', 'Missing', 'Working', '2023-11-04 17:54:04'),
(5, 'Working', 'Missing', 'Working', 'Not Working', '2023-11-02 11:28:17'),
(6, 'Working', 'Not Working', 'Working', 'Missing', '2023-11-02 11:28:37'),
(7, 'Not Working', 'Working', 'Missing', 'Working', '2023-11-02 11:28:37'),
(8, 'Working', 'Missing', 'Working', 'Not Working', '2023-11-02 11:28:37'),
(9, 'Working', 'Not Working', 'Working', 'Missing', '2023-11-02 11:28:37'),
(10, 'Not Working', 'Working', 'Missing', 'Working', '2023-11-02 11:28:37'),
(11, 'Working', 'Missing', 'Working', 'Not Working', '2023-11-02 11:28:37'),
(12, 'Working', 'Not Working', 'Working', 'Missing', '2023-11-02 11:28:37'),
(13, 'Not Working', 'Working', 'Missing', 'Working', '2023-11-02 11:28:37'),
(14, 'Working', 'Missing', 'Working', 'Not Working', '2023-11-02 11:28:37'),
(15, 'Working', 'Not Working', 'Working', 'Missing', '2023-11-02 11:28:37'),
(19, 'Working', 'Working', 'Working', 'Working', '2023-11-04 16:00:08');

-- --------------------------------------------------------

--
-- Table structure for table `reports`
--

CREATE TABLE `reports` (
  `reprot_id` int(11) NOT NULL,
  `user_id` int(11) DEFAULT NULL,
  `computer_no` varchar(255) NOT NULL,
  `problem` varchar(255) NOT NULL,
  `description` varchar(255) NOT NULL,
  `email` varchar(255) NOT NULL,
  `date_reported` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `reports`
--

INSERT INTO `reports` (`reprot_id`, `user_id`, `computer_no`, `problem`, `description`, `email`, `date_reported`) VALUES
(1, NULL, '21', 'Network', 'no internet ', 'try@gmail.com', '2023-11-11 03:12:56'),
(2, NULL, '2', 'Hardware Issue', 'kinuha yung mouse', 'admin@gmail.com', '2023-11-11 03:18:50'),
(3, NULL, '3', 'Hardware Issue', 'TRY', 'demo@1410inc.xyz', '2023-11-11 03:18:27'),
(4, NULL, '12', 'Software Issue', 'ma lag', 'rcharlesevan@yahoo.com', '2023-11-11 02:55:55'),
(5, NULL, '2', 'Network Issue', 'di makaconnect asap', 'yuridope@gmail.com', '2023-11-11 03:30:59');

-- --------------------------------------------------------

--
-- Table structure for table `users`
--

CREATE TABLE `users` (
  `user_id` int(11) NOT NULL,
  `username` varchar(255) NOT NULL,
  `last_name` varchar(255) NOT NULL,
  `first_name` varchar(255) NOT NULL,
  `gender` enum('Male','Female','Others') NOT NULL,
  `email` varchar(255) NOT NULL,
  `password` varchar(255) NOT NULL,
  `role_id` int(11) NOT NULL DEFAULT 2,
  `date` timestamp NOT NULL DEFAULT current_timestamp() ON UPDATE current_timestamp()
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_general_ci;

--
-- Dumping data for table `users`
--

INSERT INTO `users` (`user_id`, `username`, `last_name`, `first_name`, `gender`, `email`, `password`, `role_id`, `date`) VALUES
(1, 'evan', 'Ramos', 'Charles Evan Pogi ako sobra', 'Male', 'try@gmail.com', '$2b$12$EH3qWXCMS21TAnFbSMIrgO1Y8h.TQdI3GIgGUSPJkkttfzcnj2K/6', 1, '2023-11-04 18:38:25'),
(2, 'user', 'User', 'Account Number', 'Others', 'useraccount@gmail.com', '$2b$12$..Hl0Dhy12Uf7gPt7L84AeI/mAYljXGrziqDLVpG.o9WeOwhNZNAS', 2, '2023-11-04 16:41:44'),
(5, 'mama', 'Ramos', 'Carmela', 'Female', 'carmelaramos@gmail.com', '$2b$12$uEvxhfKcmc/ZUi98OHG1peAmGDK8qckwRw9p1JdpFufUMx4rLE/5K', 2, '2023-11-09 04:37:25'),
(6, 'admin', 'Admin', 'Admin', 'Others', 'admin@gmail.com', '$2b$12$3kHZVmBGlc0G6IpcB5Bw8.HuYXTvRY3qS.AAUuYfCO.X4AnL2.YE.', 1, '2023-11-07 02:30:43'),
(7, 'rex123', 'Cortez', 'Rex', 'Others', 'try@gmail.com', '$2b$12$yzYeEWpg1dphphhRv..9qOlvAXiikH6dbWjz4d8kWlYf/zqqHkkAe', 2, '2023-11-09 04:37:19'),
(8, 'try2', 'Try', 'Try', 'Female', 'try@gmail.com', '$2b$12$1.Mmzr0MC5.UZAifn310.eA7ifsdPkOOb4W3J6ZrCTVRpmoZcQyyS', 1, '2023-11-11 02:50:06'),
(9, 'yuridope', 'Yuri', 'Dope', 'Male', 'yuridope@gmail.com', '$2b$12$hmm6g5PEjMqFDoRhgKA7vOHGNRaULc0qCseVtM/GvzfUuEg4U9Eou', 2, '2023-11-11 03:30:07');

--
-- Indexes for dumped tables
--

--
-- Indexes for table `inventory`
--
ALTER TABLE `inventory`
  ADD PRIMARY KEY (`computer_id`);

--
-- Indexes for table `reports`
--
ALTER TABLE `reports`
  ADD PRIMARY KEY (`reprot_id`),
  ADD KEY `user id` (`user_id`);

--
-- Indexes for table `users`
--
ALTER TABLE `users`
  ADD PRIMARY KEY (`user_id`),
  ADD UNIQUE KEY `username` (`username`);

--
-- AUTO_INCREMENT for dumped tables
--

--
-- AUTO_INCREMENT for table `inventory`
--
ALTER TABLE `inventory`
  MODIFY `computer_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=25;

--
-- AUTO_INCREMENT for table `reports`
--
ALTER TABLE `reports`
  MODIFY `reprot_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=6;

--
-- AUTO_INCREMENT for table `users`
--
ALTER TABLE `users`
  MODIFY `user_id` int(11) NOT NULL AUTO_INCREMENT, AUTO_INCREMENT=10;

--
-- Constraints for dumped tables
--

--
-- Constraints for table `reports`
--
ALTER TABLE `reports`
  ADD CONSTRAINT `reports_ibfk_1` FOREIGN KEY (`user_id`) REFERENCES `users` (`user_id`);
COMMIT;

/*!40101 SET CHARACTER_SET_CLIENT=@OLD_CHARACTER_SET_CLIENT */;
/*!40101 SET CHARACTER_SET_RESULTS=@OLD_CHARACTER_SET_RESULTS */;
/*!40101 SET COLLATION_CONNECTION=@OLD_COLLATION_CONNECTION */;
