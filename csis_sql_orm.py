from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, relationship
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, Integer, String, Date, Time, Boolean, Float, \
    DateTime, ForeignKey
import pyodbc
import warnings




def connect():

    server = 'ZIRSYSPRO'
    db = 'MAINTDATA'
    return pyodbc.connect('DRIVER={SQL Server};SERVER=' + server +
                          ';DATABASE=' + db + ';Trusted_Connection=yes')

with warnings.catch_warnings():
    warnings.simplefilter("ignore")
    engine = create_engine('mssql://', creator=connect)
connection = engine.connect()

Base = declarative_base()


class CSISBatches(Base):
    __tablename__ = 'csis_batches'

    id = Column(Integer, primary_key=True)
    folder_path = Column(String(200))
    batch_name = Column(String(100))
    end_datetime = Column(DateTime)
    stats = relationship('CSISStats')


class CSISStats(Base):
    __tablename__ = 'csis_stats'

    unique_id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey('csis_batches.id'))
    batch = relationship("CSISBatches", back_populates="stats")
    id = Column(Integer)
    overall_result = Column(String(50))
    re_station = Column(Boolean)
    fe_station = Column(Boolean)
    odp_station = Column(Boolean)
    ss_station = Column(Boolean)
    time = Column(DateTime)
    re_valid_master = Column(Boolean)
    re_present = Column(Boolean)
    re_orientation = Column(Boolean)
    re_valid = Column(Boolean)
    re_inner_bright = Column(Boolean)
    re_inner_small_dark = Column(Boolean)
    re_inner_large = Column(Boolean)
    re_outer_bright = Column(Boolean)
    re_outer_small_dark = Column(Boolean)
    re_outer_large_dark = Column(Boolean)
    re_ida_bright = Column(Float(decimal_return_scale=6))
    re_ida_large_dark = Column(Float(decimal_return_scale=6))
    re_ida_small_dark = Column(Float(decimal_return_scale=6))
    re_oda_bright = Column(Float(decimal_return_scale=6))
    re_oda_large_dark = Column(Float(decimal_return_scale=6))
    re_oda_small_dark = Column(Float(decimal_return_scale=6))
    re_m_center_x = Column(Float(decimal_return_scale=6))
    re_m_center_y = Column(Float(decimal_return_scale=6))
    re_uut_center_x = Column(Float(decimal_return_scale=6))
    re_uut_center_y = Column(Float(decimal_return_scale=6))
    fe_valid_master = Column(Boolean)
    fe_orientation = Column(Boolean)
    fe_valid = Column(Boolean)
    fe_inner_diameter = Column(Boolean)
    fe_obstruction = Column(Boolean)
    fe_chip = Column(Boolean)
    fe_inner_dia_min = Column(Float(decimal_return_scale=6))
    fe_inner_dia_max = Column(Float(decimal_return_scale=6))
    fe_obstr_area = Column(Float(decimal_return_scale=6))
    fe_chip_area = Column(Float(decimal_return_scale=6))
    odp_position = Column(Boolean)
    odp_length = Column(Boolean)
    odp_bumps = Column(Boolean)
    odp_chips = Column(Boolean)
    odp_envelope = Column(Boolean)
    odp_nose = Column(Boolean)
    odp_num_images = Column(Integer)
    odp_length_mm = Column(Float(decimal_return_scale=6))
    odp_max_bump_mm = Column(Float(decimal_return_scale=6))
    odp_max_chip_mm = Column(Float(decimal_return_scale=6))
    odp_envelope_mm = Column(Float(decimal_return_scale=6))
    odp_nose_w_min_max = Column(Float(decimal_return_scale=6))
    odp_mdn_od_mm = Column(Float(decimal_return_scale=6))
    ss_valid = Column(Boolean)
    ss_bright_defect = Column(Boolean)
    ss_blemish_defect = Column(Boolean)
    ss_spot_crack_defect = Column(Boolean)
    ss_bright_da_mm2 = Column(Float(decimal_return_scale=6))
    ss_blemish_da_mm2 = Column(Float(decimal_return_scale=6))
    ss_spot_crack_da_mm2 = Column(Float(decimal_return_scale=6))
    ss_num_frames = Column(Integer)


class CSISSummary(Base):
    __tablename__ = 'csis_summary'

    id = Column(Integer, primary_key=True)
    batch_id = Column(Integer, ForeignKey('csis_batches.id'))
    inspected = Column(Integer)
    good = Column(Integer)
    good_percent = Column(Float(1, decimal_return_scale=1))
    fail_general = Column(Integer)
    fail_gen_percent = Column(Float(1, decimal_return_scale=1))
    fail_od = Column(Integer)
    fail_od_percent = Column(Float(1, decimal_return_scale=1))
    fail_backward = Column(Integer)
    fail_backward_percent = Column(Float(1, decimal_return_scale=1))
    n_a = Column(Integer)
    n_a_percent = Column(Float(1, decimal_return_scale=1))

class CSISCurrent(Base):
    __tablename__ = 'csis_current'

    id = Column(Integer, primary_key=True)
    batch_id = Column(String(50))
    total = Column(Integer)
    passed = Column(Integer)
    failed = Column(Integer)
    failed_od = Column(Integer)
    failed_backwards = Column(Integer)
    n_a = Column(Integer)

Session = sessionmaker(bind=engine)

Base.metadata.create_all(engine)


if __name__ == '__main__':
    print("got through")
