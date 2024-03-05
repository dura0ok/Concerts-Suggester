CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE processed_concert_links (
    id SERIAL PRIMARY KEY,
    concert_link VARCHAR(255) NOT NULL
);

CREATE TABLE users_playlists (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    playlist_link VARCHAR(255) NOT NULL
);

CREATE TABLE user_cities (
    id SERIAL PRIMARY KEY,
    user_id INTEGER REFERENCES users(id) NOT NULL,
    city_name VARCHAR(255) NOT NULL
);