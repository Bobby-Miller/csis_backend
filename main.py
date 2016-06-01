from config import CSISConfigs
from csis_folders import CSISFolders
from csis_stats import Stats
from csis_status import CSISStatus
from csis_summary import Summary
from csis_sql_orm import Session
from db_data import DBData
from time import sleep
from threading import Thread, Lock
from sqlalchemy.exc import DBAPIError


class Main(CSISConfigs):
    def __init__(self):
        super().__init__()

        # Initialize helper objects
        self.folder_data = CSISFolders()
        self.status = CSISStatus()

        # Gather batch data for comparison
        self.folder_set = self.folder_data.parse_folder_data()
        self.db_data = DBData()
        self.db_batches = self.db_data.batches_from_db()

        # The comparison
        self.new_batches = self.unregistered_batches(self.folder_set, self.db_batches)

        # Adding data to DB
        for batch in self.new_batches:
            self.db_data.add_batch(batch)
            self.db_data.add_stats(batch)
            self.db_data.add_summary(batch)
            self.db_data.commit()

        # Initialize current batch data
        self.current_batch = self.folder_data.current_batch()
        self.stats_entered = self.db_data.stats_entered(self.current_batch)
        self.summary_entered = self.db_data.summary_entered(self.current_batch)

        # Initialize thread and locks
        self.thread_lock = Lock()

    def status_loop(self):
        while True:
            try:
                self.status.reset_session()
                sleep(.25)
                data_compare = self.status.compare_status_w_file()
                if data_compare:
                    pass
                else:
                    with self.thread_lock:
                        self.status.update_db_status()
            except DBAPIError:
                pass

    def batch_loop(self):
        while True:
            try:
                self.db_data.reset_session()
                sleep(5)
                last_batch = self.current_batch
                if not self.stats_entered:
                    stats = Stats(self.current_batch)
                    if stats.exists():
                        self.db_data.add_stats(self.current_batch)
                        self.stats_entered = True
                if not self.summary_entered:
                    summary = Summary(self.current_batch)
                    if summary.exists():
                        self.db_data.add_summary(self.current_batch)
                        self.summary_entered = True
                with self.thread_lock:
                    self.db_data.commit()
                self.current_batch = self.folder_data.current_batch()
                if self.current_batch != last_batch:
                    self.db_data.add_batch(self.current_batch)
                    self.stats_entered = False
                    self.summary_entered = False
            except DBAPIError:
                pass

    @staticmethod
    def unregistered_batches(folder_data, db_data):
        """
        Determine unentered data.
        :return: set of lists that have not been entered into the database.
        """
        unregistered_sets = set(folder_data) - set(db_data)
        return unregistered_sets

if __name__ == '__main__':
    main = Main()
    status_task = Thread(target=main.status_loop)
    batch_task = Thread(target=main.batch_loop)
    status_task.start()
    batch_task.start()