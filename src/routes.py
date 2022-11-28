from simplexml import dumps
from flask import make_response, jsonify
from flask_restful import Resource, reqparse

from src import api
from src import report
from src.build_data import build_drivers_data, find_driver
from src.config import FOLDER_PATH


def output_xml(data, code, headers=None):
    resp = make_response(dumps({'response': data}), code)
    resp.headers['Accept'] = 'application/xml'
    return resp


api.representations['application/xml'] = output_xml

parser = reqparse.RequestParser()


class CommonStatistics(Resource):
    def get(self):
        args = parser.parse_args()
        resp_format = args.get('resp_format')
        data = report.build_report(FOLDER_PATH)
        if resp_format == 'json':
            output = []
            for driver in data:
                driver_data = {'place': driver[0], 'name': driver[1], 'car': driver[2], 'time': driver[3]}
                output.append(driver_data)
            return jsonify(output)
        elif resp_format == 'xml':
            output = []
            driver_tag = {}
            for driver in data:
                driver_data = {'place': driver[0], 'name': driver[1], 'car': driver[2], 'time': driver[3]}
                driver_tag['driver'] = driver_data
                output.append(driver_tag)
            return output


api.add_resource(CommonStatistics, '/api/v1/report/')


parser.add_argument('driver_id', type=str, location='args')
parser.add_argument('order', type=str, location='args')
parser.add_argument('resp_format', type=str, location='args')


class DriversStatistics(Resource):
    def get(self):
        args = parser.parse_args()
        abb_dict = build_drivers_data()
        order = args.get('order')
        driver_id = args.get('driver_id')
        resp_format = args.get('resp_format')

        output = []

        if driver_id:
            driver_id = driver_id.upper()

        if not order and not args.driver_id:
            if resp_format == 'json':
                for key in abb_dict.keys():
                    name_car_list = abb_dict.get(key)
                    driver_statistics = {'abb': key, 'name': name_car_list[0], 'car': name_car_list[1]}
                    output.append(driver_statistics)
            elif resp_format == 'xml':
                driver_tag = {}
                for key in abb_dict.keys():
                    name_car_list = abb_dict.get(key)
                    driver_statistics = {'abb': key, 'name': name_car_list[0], 'car': name_car_list[1]}
                    driver_tag['driver'] = driver_statistics
                    output.append(driver_tag)

        elif order == 'asc':
            if resp_format == 'json':
                data = report.build_report(FOLDER_PATH)
                for driver in data:
                    driver_data = {'place': driver[0], 'name': driver[1], 'car': driver[2], 'time': driver[3]}
                    output.append(driver_data)

            elif resp_format == 'xml':
                data = report.build_report(FOLDER_PATH)
                for driver in data:
                    driver_data = {'place': driver[0], 'name': driver[1], 'car': driver[2], 'time': driver[3]}
                    output.append(driver_data)

        elif order == 'desc':
            if resp_format == 'json':
                data = report.build_report(FOLDER_PATH)
                for driver in data:
                    driver_data = {'place': driver[0], 'name': driver[1], 'car': driver[2], 'time': driver[3]}
                    output.append(driver_data)
                output = output[::-1]
            elif resp_format == 'xml':
                driver_tag = {}
                data = report.build_report(FOLDER_PATH)
                data = data[::-1]
                for driver in data:
                    driver_data = {'place': driver[0], 'name': driver[1], 'car': driver[2], 'time': driver[3]}
                    driver_tag['driver'] = driver_data
                    output.append(driver_tag)

        elif driver_id in abb_dict.keys():  # if driver_id == None,driver_id.upper() raise an err.
            if resp_format == 'json':
                driver_list = find_driver(abb_dict.get(driver_id))
                output = {'place': driver_list[0], 'name': driver_list[1],
                          'car': driver_list[2], 'time': driver_list[3]}
            if resp_format == 'xml':
                driver_list = find_driver(abb_dict.get(driver_id))
                output = {'place': driver_list[0], 'name': driver_list[1],
                          'car': driver_list[2], 'time': driver_list[3]}

        else:
            output = 'Bad request'

        if resp_format == 'json':
            return jsonify(output)
        else:
            return output


api.add_resource(DriversStatistics, '/api/v1/report/drivers/')
