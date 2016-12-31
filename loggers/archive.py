from peewee import fn, IntegrityError
from db import db, archive_db
from datetime import datetime, timedelta
import logging


def ensure_datetime(timestamp):
    if isinstance(timestamp, datetime):
        return timestamp
    else:
        return datetime.fromtimestamp(timestamp)


def oldest_record_query(Model):
    record = (Model
              .select()
              .group_by(Model)
              .having(fn.Min(Model.timestamp)))
    return record


def archive_row(LiveModel, ArchiveModel):
    livedb_query = oldest_record_query(LiveModel)
    # ensure Table exists in archive
    ArchiveModel.create_table(fail_silently=True)
    try:
        with archive_db.atomic():
            record_data = livedb_query.dicts().get()
            archive_db.connect()
            ArchiveModel.insert(record_data).execute()
            archive_db.close()

            with db.atomic():
                (LiveModel
                 .delete()
                 .where(LiveModel.id == livedb_query.get().id)
                 .execute())
        return 'Record archived successfully.'

    except IntegrityError:
        return "Archiving failed: there was an issue with either saving the record to archive or deleting from live database."


def shuffle2archive(LiveModel, ArchiveModel, cutoff_period=2):
    cutoff = datetime.now() - timedelta(days=cutoff_period)
    oldest_record_date = ensure_datetime(oldest_record_query(LiveModel)
                                         .get()
                                         .timestamp)

    iterations = 0
    while oldest_record_date < cutoff:
        archive_row(LiveModel, ArchiveModel)

        iterations += 1
        if iterations % 100 == 1:
            logging.info('Archiving models older than {}.\n'
                         'Archived model {} with date {}.\n'
                         'Total records archived: {}.\n'
                         .format(cutoff,
                                 LiveModel,
                                 oldest_record_date,
                                 iterations))

        oldest_record_date = ensure_datetime(oldest_record_query(LiveModel)
                                             .get()
                                             .timestamp)

    logging.info('Shuffle finished with {} records archived in model {}.'
                 .format(iterations, ArchiveModel))
