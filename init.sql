CREATE TABLE users (
    id SERIAL PRIMARY KEY,
    telegram_id VARCHAR(255) NOT NULL,
    created_at TIMESTAMP WITH TIME ZONE DEFAULT CURRENT_TIMESTAMP NOT NULL
);

CREATE TABLE processed_concert_links (
    concert_link VARCHAR(255) NOT NULL,
    PRIMARY KEY (concert_link)
);

CREATE TABLE users_playlists (
    user_id INTEGER REFERENCES users(id) NOT NULL,
    playlist_link VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id, playlist_link)
);

CREATE TABLE users_cities (
    user_id INTEGER REFERENCES users(id) NOT NULL,
    city_name VARCHAR(255) NOT NULL,
    PRIMARY KEY (user_id, city_name)
);