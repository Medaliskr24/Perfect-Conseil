CREATE TABLE IF NOT EXISTS pc_users (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  email VARCHAR(190) NOT NULL,
  password_hash VARCHAR(255) NOT NULL,
  created_at DATETIME NOT NULL,
  last_login DATETIME NULL,
  UNIQUE KEY uq_email (email)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS pc_articles (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  slug VARCHAR(100) NOT NULL,
  title VARCHAR(190) NOT NULL,
  category VARCHAR(60) NOT NULL,
  description VARCHAR(300) NOT NULL,
  body MEDIUMTEXT NOT NULL,
  cover VARCHAR(60) NULL,
  status ENUM('draft','published') NOT NULL DEFAULT 'published',
  published_at DATE NOT NULL,
  created_at DATETIME NOT NULL,
  updated_at DATETIME NOT NULL,
  UNIQUE KEY uq_slug (slug),
  KEY idx_pub (status, published_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
CREATE TABLE IF NOT EXISTS pc_login_attempts (
  id INT UNSIGNED NOT NULL AUTO_INCREMENT PRIMARY KEY,
  ip VARCHAR(45) NOT NULL,
  email VARCHAR(190) NOT NULL DEFAULT '',
  attempted_at DATETIME NOT NULL,
  KEY idx_ip (ip, attempted_at),
  KEY idx_email (email, attempted_at)
) ENGINE=InnoDB DEFAULT CHARSET=utf8mb4 COLLATE=utf8mb4_unicode_ci;
