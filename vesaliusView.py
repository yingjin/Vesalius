from flask import request, jsonify, render_template
from vesaliusModel import VesaliusModel

import flask.views
import json


class MetadataByZonegroup(flask.views.MethodView):
    def get(self, zone_group):
        if(zone_group):
            descriptionList = VesaliusModel.retrieve_description_by_zonegroup(zone_group)
            mediaList = VesaliusModel.retrieve_media_by_zonegroup(zone_group)
            display_zone_group = " (&#"+ zone_group.replace(",",";&#",10) + ";)"; 
            return jsonify({
                'success': True,
                'descriptionList': [{'description_text': item['description_text'], 'header_text': item['header_text']+display_zone_group} for item in descriptionList],
                'mediaList': [{'image': item['image'], 'description': item['description'], 'source_specifications': item['source_specifications'], 'citation_text': item['citation_text'], 'citation_short_display': item['citation_short_display'], 'citation_type': item['citation_type']} for item in mediaList]
            })
        