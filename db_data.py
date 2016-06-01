from csis_sql_orm import Session, CSISBatches, CSISSummary, CSISStats
from sqlalchemy.orm.exc import NoResultFound, MultipleResultsFound
from collections import namedtuple
from csis_folders import CSISFolders
from csis_summary import Summary
from csis_stats import Stats
from typing import NamedTuple


class DBData:
    def __init__(self):
        self.session = Session()

    def batches_from_db(self):
        """
        Collect the batch data sets entered in the database. Use as reference
        against existing folders.
        :return: set of batch lists
        """
        db_data = set()
        Point = namedtuple('db_batch', 'file_path, batch_name, batch_datetime')
        for folder_name, name, datetime in self.session.query(
                CSISBatches.folder_path, CSISBatches.batch_name,
                CSISBatches.end_datetime):
            db_data.add(Point(folder_name, name, datetime))
        return db_data

    def add_batch(self, batch: NamedTuple) -> None:
        """
        Adds a batch to the db session from a batch namedtuple
        :param batch: (namedtuple) batch details
        :return: No return
        """
        batch_line = CSISBatches(**batch._asdict())
        self.session.add(batch_line)
        self.session.flush()

    def add_summary(self, batch: NamedTuple) -> None:
        summary = Summary(batch)
        if summary.exists():
            summary_data = summary.summary_data()
            batch_id = self.batch_id(batch)
            summary_line = CSISSummary(batch_id=batch_id, **summary_data._asdict())
            self.session.add(summary_line)

    def add_stats(self, batch: NamedTuple) -> None:
        stats = Stats(batch)
        if stats.exists():
            with self.session.no_autoflush:
                stats_gen = stats.type_map()
                batch_id = self.batch_id(batch)
                for line in stats_gen:
                    self.session.add(CSISStats(batch_id=batch_id, **line))

    def batch_id(self, batch: NamedTuple) -> int:
        try:
            query = self.session.query(CSISBatches.id).\
                        filter(CSISBatches.folder_path == batch[0]).one()
            return query[0]
        except NoResultFound:
            return None

    def summary_entered(self, batch: NamedTuple) -> bool:
        batch_id = self.batch_id(batch)
        query = self.session.query(CSISSummary.batch_id).\
            filter(CSISSummary.batch_id == batch_id).first()
        return False if query is None else True

    def stats_entered(self, batch: NamedTuple) -> bool:
        batch_id = self.batch_id(batch)
        query = self.session.query(CSISStats.batch_id).\
            filter(CSISStats.batch_id == batch_id).first()
        return False if query is None else True

    def commit(self):
        self.session.commit()

    def reset_session(self):
        self.session.close()
        self.session = Session()

if __name__ == '__main__':
    test_obj = DBData()
    test_obj.add_batch(CSISFolders().current_batch())
    test_obj.commit()

