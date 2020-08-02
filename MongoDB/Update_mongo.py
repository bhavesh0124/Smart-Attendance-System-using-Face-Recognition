
from pymongo import MongoClient
import pandas as pd

class database:
    def __init__(self):
        self.client=MongoClient()
        self.db=self.client.students

    def update(self,name):
        self.db.Attendance.update_one({"Name":name},{"$inc":{"Attendance":1}})

    def export_csv(self):
        data={
               "Roll Number":self.Roll_number,
               "name":self.name,
               "attendance":self.attendance
             }
             
        df=pd.DataFrame(data,columns=["name","attendance"])
        df.to_csv("attendance.csv",index=True)
