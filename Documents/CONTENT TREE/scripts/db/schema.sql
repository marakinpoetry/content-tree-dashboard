-- Content Tree SQLite Schema
-- 6 tables: content_files, topics, content_types, languages, priorities, content_fts

-- Main table: every file in Content/
CREATE TABLE IF NOT EXISTS content_files (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    path TEXT UNIQUE NOT NULL,
    name TEXT NOT NULL,

    -- Hierarchy
    product TEXT,
    stage TEXT,
    category TEXT,
    topic TEXT,

    -- Content attributes
    content_type TEXT,
    language TEXT,
    status TEXT DEFAULT 'draft',

    -- Metadata
    title TEXT,
    word_count INTEGER DEFAULT 0,
    size INTEGER DEFAULT 0,
    modified TIMESTAMP,
    created_at TIMESTAMP DEFAULT CURRENT_TIMESTAMP,
    content_hash TEXT,

    -- Google Drive
    drive_url TEXT,

    -- Future CMS integration
    cms_id TEXT,
    cms_status TEXT,
    cms_url TEXT,
    published_at TIMESTAMP
);

CREATE INDEX IF NOT EXISTS idx_coverage ON content_files(category, topic, content_type, language);
CREATE INDEX IF NOT EXISTS idx_language ON content_files(language, status);
CREATE INDEX IF NOT EXISTS idx_product ON content_files(product, stage);
CREATE INDEX IF NOT EXISTS idx_content_type ON content_files(content_type);
CREATE INDEX IF NOT EXISTS idx_topic ON content_files(topic);
CREATE INDEX IF NOT EXISTS idx_status ON content_files(status);

-- Reference: all known topics
CREATE TABLE IF NOT EXISTS topics (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    category TEXT NOT NULL,
    name TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL
);

CREATE INDEX IF NOT EXISTS idx_topics_category ON topics(category);

-- Reference: content formats
CREATE TABLE IF NOT EXISTS content_types (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    name TEXT UNIQUE NOT NULL,
    display_name TEXT NOT NULL
);

-- Reference: languages
CREATE TABLE IF NOT EXISTS languages (
    code TEXT PRIMARY KEY,
    name TEXT NOT NULL,
    is_primary BOOLEAN DEFAULT 0
);

-- Reference: gap priority rules
CREATE TABLE IF NOT EXISTS priorities (
    id INTEGER PRIMARY KEY AUTOINCREMENT,
    stage TEXT,
    category TEXT,
    content_type TEXT,
    language TEXT,
    priority INTEGER NOT NULL,
    priority_label TEXT NOT NULL
);

-- Full-text search index (standalone, for CLI search)
CREATE VIRTUAL TABLE IF NOT EXISTS content_fts USING fts5(
    file_id UNINDEXED,
    path,
    title,
    body
);
