import csv
import os

from sqlalchemy import create_engine
from sqlalchemy.orm import scoped_session, sessionmaker

engine = create_engine(os.getenv("DATABASE_URL"))
db = scoped_session(sessionmaker(bind=engine))

def main():

    # Open a file using Python's CSV reader.
    f = open("zips.csv")
    reader = csv.reader(f)
    next(reader)  #skip header row

    # Iterate over the rows of the opened CSV file.
    for row in reader:

        # Execute database queries, one per row; then print out confirmation.
        db.execute("INSERT INTO zipcodes (zipcode, city, state,latt,long,population) VALUES (:z,:c,:s,:la,:lo,:p)",
                    {"z": row[0], "c": row[1], "s": row[2], "la": row[3],"lo": row[4],"p": row[5]})
       # print(f"Added zipcodes from {row[0]} to {row[1]} lasting {row[2]} minutes.")

    # Technically this is when all of the queries we've made happen!
    db.commit()

if __name__ == "__main__":
    main()
