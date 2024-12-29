CREATE DATABASE IF NOT EXISTS grimrepor_db;
USE grimrepor_db;

CREATE TABLE IF NOT EXISTS papers_and_code (
    id INT AUTO_INCREMENT PRIMARY KEY,
    paper_title VARCHAR(255) NOT NULL UNIQUE,
    paper_arxiv_id VARCHAR(255) DEFAULT NULL UNIQUE,
    paper_arxiv_url VARCHAR(255) DEFAULT NULL UNIQUE,
    paper_pwc_url VARCHAR(255) DEFAULT NULL UNIQUE,
    github_url VARCHAR(255) DEFAULT NULL UNIQUE,
    build_sys_type VARCHAR(255) DEFAULT NULL,
    deps_file_url VARCHAR(255) DEFAULT NULL UNIQUE,
    deps_file_content_orig MEDIUMTEXT,
    build_status_orig VARCHAR(255) DEFAULT NULL,
    deps_file_content_edited MEDIUMTEXT,
    build_status_edited VARCHAR(255) DEFAULT NULL,
    datetime_latest_build DATETIME DEFAULT NULL,
    num_build_attempts INT DEFAULT 0,
    github_fork_url VARCHAR(255) DEFAULT NULL UNIQUE,
    pushed_to_fork BOOLEAN DEFAULT FALSE,
    pull_request_made BOOLEAN DEFAULT FALSE,
    tweet_posted BOOLEAN DEFAULT FALSE,
    tweet_url VARCHAR(255) DEFAULT NULL UNIQUE
);