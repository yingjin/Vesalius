from flask import request, jsonify, render_template
from vesaliusModel import VesaliusModel

import flask.views
import json
import re

citationList = VesaliusModel.retrieve_citation()
citations = {}
for citation in citationList:
    citations[citation['citation_short_display']] = citation['citation_type'] + " " + citation['citation_text']

class MetadataByZonegroup(flask.views.MethodView):
    def getParsedDescription(self, description):
        ss = []
        ds = []
      
        print description
        #for dd in description:
        ss = re.split('\[\[\[|\]\]\]', description)

        count = 0  
        lens = len(ss)
        print lens
        while count < lens:
            des = ss[count]
            cit_short = ''
            cit_tip = ''
            count = count + 1
            if(count < lens):
                cit_short = ss[count]    
                cit_tip = citations[cit_short]
            count = count + 1
            djson = {'description': des,
                     'citation': {'cit_short': cit_short,
                                  'cit_tip': cit_tip
                                  }
                     }
            ds.append(djson)
        print ds     
        return ds
    
    def get(self, zone_group):
        if(zone_group):
            descriptionList = VesaliusModel.retrieve_description_by_zonegroup(zone_group)
            mediaList = VesaliusModel.retrieve_media_by_zonegroup(zone_group)
            display_zone_group = " (&#"+ zone_group.replace(",",";&#",10) + ";)"
            
            return jsonify({
                'success': True,
                # 'descriptionList': [{'description_text': self.getParsedDescription(item['description_text']), 'header_text': item['header_text']+display_zone_group} for item in descriptionList],
                'descriptionList': [{'description_text': item['description_text'], 'header_text': item['header_text']+display_zone_group} for item in descriptionList],
                #'mediaList': [{'image': item['image'], 'fullimagename': self.getFullImageName(item['image']), 'description_text': self.getParsedDescription(item['description_text']), 'source_specifications': item['source_specifications'], 'citation_text': item['citation_text'], 'citation_short_display': item['citation_short_display'], 'citation_type': item['citation_type']} for item in mediaList]
                'mediaList': [{'image': item['image'], 'fullimagename': self.getFullImageName(item['image']), 'description_text': item['description_text'], 'source_specifications': item['source_specifications'], 'citation_text': item['citation_text'], 'citation_short_display': item['citation_short_display'], 'citation_type': item['citation_type']} for item in mediaList]
            })
    
           
    def getFullImageName(self, imagename):
        fullimagename = ''
        
        getsuffix = re.split('\.', imagename)
        # keep the last one as the extension
        imagesuffix = getsuffix[-1:]
        imagename1 = re.split('-', imagename)
        del imagename1[-1:]
        fullimagename = '-'.join(imagename1) + '.' + imagesuffix[0] 
        return fullimagename
    
        
  
        