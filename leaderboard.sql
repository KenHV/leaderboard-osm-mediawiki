PRAGMA foreign_keys=OFF;
BEGIN TRANSACTION;

CREATE TABLE leaderboard (
    display_name TEXT,
    user_email TEXT UNIQUE,
    osm_username TEXT default null,
    osm_orig_score INT default 0,
    osm_current_score INT default 0,
    mw_username TEXT default null,
    mw_orig_score INT default 0,
    mw_current_score INT default 0
);

COMMIT;
