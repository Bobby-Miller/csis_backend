import csv
import os
import pandas as pd
from datetime import date, time, datetime
from csis_sql_orm import Session, CSISStats, CSISCurrent
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from config import CSISConfigs


class CSISStatus(CSISConfigs):
    def __init__(self):
        super().__init__()
        # Initialize DB/ORM session for use in class
        self.session = Session()

        try:
            self.db_status = self.session.query(CSISCurrent).filter_by(
                id=1).one()
        except NoResultFound:
            self.db_status = None
        except MultipleResultsFound:
            print('multiple results found')
            try:
                self.session.query(CSISCurrent).delete()
                self.session.commit()
            except:
                self.session.rollback()

        self.status_list = self.status_from_file()

    @property
    def db_status(self):
        return self.__db_status

    @db_status.setter
    def db_status(self, db_status):
        if db_status is None:
            # self.db_status = CSISCurrent(self.status_from_file())
            # self.session.add(self.db_status)
            data_labels = ["batch_id", "total", "passed", "failed", "failed_od",
                           "failed_backwards", "n_a"]
            data_list = self.status_from_file()
            kwargs = dict(zip(data_labels, data_list))
            self.__db_status = CSISCurrent(id=1, **kwargs)
            self.session.add(self.__db_status)
            self.session.commit()
        else:
            self.__db_status = db_status

    @property
    def status_list(self):
        return self.__status_list

    @status_list.setter
    def status_list(self, status_list):
        if status_list is None:
            self.__status_list = self.status_from_file()
        else:
            self.__status_list = status_list

    def status_from_file(self):
        data_path = self.data_path + '/Status.txt'
        with open(data_path, 'r') as file_data:
            reader = csv.reader(file_data, delimiter=':')
            status_list = [next(reader)[1][1:]]
            for data in reader:
                try:
                    status_list.append(int(data[1]))
                except ValueError:
                    status_list.append(float(data[1]))
            print(status_list)
            return status_list

    def compare_status_w_file(self):
        file = self.status_from_file()
        if file == self.status_list:
            return True
        else:
            self.status_list = file
            return False

    def update_db_status(self):
        self.db_status.batch_id = self.status_list[0]
        self.db_status.total = self.status_list[1]
        self.db_status.passed = self.status_list[2]
        self.db_status.failed = self.status_list[3]
        self.db_status.failed_od = self.status_list[4]
        self.db_status.failed_backwards = self.status_list[5]
        self.db_status.n_a = self.status_list[6]
        self.session.add(self.db_status)
        self.session.commit()

    def reset_session(self):
        self.session.close()
        self.session = Session()

if __name__ == '__main__':
    print(CSISStatus().status_df.values[1][0])
    print(type(CSISStatus().status_df.values[1][0]))
