import sqlite3
import os

application_path = os.path.dirname(__file__)
dbFilePath = os.path.join(application_path, 'vesalius5.db')

_conn = sqlite3.connect(dbFilePath, check_same_thread=False)
_conn.row_factory = sqlite3.Row
_cursor = _conn.cursor()

class VesaliusModel:
    def __init__(self):
        pass

    @classmethod
    def retrieve_description_by_zonegroup(cls, zone_group):
        rows = _cursor.execute(
            'SELECT description_text,header_text FROM description_text WHERE description_text.zone_group=?', (zone_group, )
            )
        return [{'description_text': r['description_text'], 'header_text': r['header_text']} for r in rows]

    @classmethod
    def retrieve_media_by_zonegroup(cls, zone_group):
        rows = _cursor.execute(
            'SELECT associated_media.image, associated_media.description, associated_media.source_specifications, bibliography.citation_text, bibliography.citation_short_display, bibliography.citation_type FROM associated_media, bibliography WHERE associated_media.zone_group=? and associated_media.source=bibliography.citation_id', (zone_group, )
            )
        return [{'image': r['image'], 'description_text': r['description'], 'source_specifications': r['source_specifications'], 'citation_text': r['citation_text'], 'citation_short_display': r['citation_short_display'], 'citation_type': r['citation_type']} for r in rows]

    @classmethod
    def retrieve_citation(cls):
        rows = _cursor.execute(
            'SELECT  bibliography.citation_text, bibliography.citation_short_display, bibliography.citation_type FROM bibliography'
            )
        return [{'citation_short_display': r['citation_short_display'], 'citation_text': r['citation_text'], 'citation_type': r['citation_type']} for r in rows]
