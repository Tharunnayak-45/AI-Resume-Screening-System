import os
import mysql.connector


def get_db_connection():

    connection = mysql.connector.connect(
        host=os.environ.get(
            "DB_HOST",
            "localhost"
        ),

        user=os.environ.get(
            "DB_USER",
            "root"
        ),

        password=os.environ.get(
            "DB_PASSWORD",
            "root"
        ),

        database=os.environ.get(
            "DB_NAME",
            "ai_resume_db"
        ),

        port=int(
            os.environ.get(
                "DB_PORT",
                3306
            )
        )
    )

    return connection