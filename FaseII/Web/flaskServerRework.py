#-------------------------------------------------------------------------------
# Name:        RedditScrapper
# Purpose:
#
# Author:      Pedro Gomes
#
# Created:     11/10/2013
# Copyright:   (c) Pedro Gomes 2013
# Licence:     <your licence>
#-------------------------------------------------------------------------------

class FlaskServer():
    
    
    def __init__(self ):
        from flask import Flask, jsonify, render_template, request
        self.app = Flask(__name__, static_folder='static', static_url_path='')
        
        import sys
        sys.path.append(fixpath('../API_IndoorPositionFindr'))
        import IndoorPositionr as IndoorPositionr
        self.indoorPositionr = IndoorPositionr.IndoorPositionr()
       

        @self.app.route("/")
        def hello():
        
            return render_template('index.html') 
        
        @self.app.route('/_get_surveyed_access_points')
        def get_ap_positions():
            
            return self.indoorPositionr.getSurveyedPositions()
        
        
        @self.app.route('/_get_measured_path')
        def _get_measured_path():

            return self.indoorPositionr.getMeasuredPathPositions()
    
    
        @self.app.route('/_get_possible_locations')
        def _get_possible_locations():
   
            tmpLng = request.args.get('lng', 9.0, type=float)
            tmplat = request.args.get('lat', 9.0, type=float)
            position=(tmplat,tmpLng)

            return self.indoorPositionr.getLocationPossibilityFromMeasuredPathPoint(position)
        
        
        @self.app.route('/_get_scan_position')
        def _get_scan_position():
           
            return self.inoorPositionr.getLocationPossibilityFromScan()
            
            
                
        @self.app.route('/_get_continuous_scan_position')
        def _get_continuous_scan_position():
           
            return self.indoorPositionr.getLocationPossibilityFromContinuousScan()
            
        @self.app.route('/_stop_continuous_scan_position')
        def _stop_continuous_scan_position():
           
            return self.indoorPositionr.stopContinuousScan()
        
        
        
        @self.app.route('/_get_walk_and_position')
        def _get_walk_and_position():
           
            return self.indoorPositionr.getPositionsFromTestWalk()
            
            
            
        @self.app.route('/_get_self_position')
        def get_self_position():
           
            return self.webAP.getSelfPositionJSON()
        
        
        @self.app.route('/_add_mobile_location_data',methods=['POST', 'GET'])
        def _add_mobile_location_data():
            
            tmpMobileData = request.json['mobileData']
            tmpMobileID =  tmpMobileData['mobileID']
            del tmpMobileData['mobileID']
            import logging
            log = logging.getLogger('werkzeug')
            
            log.warning(tmpMobileData)

            tmpReturnData = self.indoorPositionr.add_Mobile_Location_Data(tmpMobileData,tmpMobileID)

            return jsonify({'ok':'tmpReturnData'})
        
        @self.app.route('/_get_mobile_position')
        def _get_mobile_position():
            
            return self.indoorPositionr.get_Mobile_Location()
           
        
        @self.app.route('/_get_scan_area')
        def _get_scan_area():
            tmpPosition = request.args.get('lng', 9.0, type=float)
            tmpSide = request.args.get('lat', 9.0, type=float)
            position=(tmpSide,tmpPosition)
            print "cenas123123"
            print position
            print "cenas111111"
            self.webAP.scanAreaPosition(position)
            self.webAP.saveToCSV("scan-19-10.csv")
            return jsonify(scanned="true")

        @self.app.route('/_get_survey_scan')
        def _get_survey_scan():
            return jsonify(self.webAP.getSurveyedPositions())
        
        
        
       
            
        @self.app.route('/_get_guess_position')
        def _guess_position():
            self.webAP.getSurveyedPositions()

            return jsonify(self.webAP.getPossibility())
        
        
        


def testFunct():
    import sys
    sys.path.append('../API')
    import WebAP as WebAP
    webAP = WebAP.WebAP()
    test = webAP.loadMeasuredPath()

def main():

   
    testFunct()
    flask = FlaskServer()
    flask.app.debug = False
    
    flask.app.run(host='0.0.0.0',port=80)

import os
def fixpath(path):
    return os.path.abspath(os.path.expanduser(path))
    
    
if __name__ == '__main__':
    main()
