import psycopg2
from config import DB_NAME, DB_USER, DB_PASSWORD, DB_HOST, DB_PORT


def connect():
    return psycopg2.connect(
        dbname=DB_NAME,
        user=DB_USER,
        password=DB_PASSWORD,
        host=DB_HOST,
        port=DB_PORT
    )


def get_or_create_player(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute("SELECT id FROM players WHERE username = %s", (username,))
    player = cur.fetchone()

    if player:
        player_id = player[0]
    else:
        cur.execute(
            "INSERT INTO players (username) VALUES (%s) RETURNING id",
            (username,)
        )
        player_id = cur.fetchone()[0]
        conn.commit()

    cur.close()
    conn.close()
    return player_id


def save_score(username, score, level):
    player_id = get_or_create_player(username)

    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        INSERT INTO game_sessions (player_id, score, level_reached)
        VALUES (%s, %s, %s)
        """,
        (player_id, score, level)
    )

    conn.commit()
    cur.close()
    conn.close()


def get_top_10():
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT p.username, g.score, g.level_reached, g.played_at
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        ORDER BY g.score DESC
        LIMIT 10
        """
    )

    data = cur.fetchall()

    cur.close()
    conn.close()
    return data


def get_personal_best(username):
    conn = connect()
    cur = conn.cursor()

    cur.execute(
        """
        SELECT MAX(g.score)
        FROM game_sessions g
        JOIN players p ON p.id = g.player_id
        WHERE p.username = %s
        """,
        (username,)
    )

    result = cur.fetchone()[0]

    cur.close()
    conn.close()

    return result if result else 0