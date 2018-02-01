#-*- coding: UTF-8 -*-
# module for CMDBuild interfacing
# Trying to follow https://www.python.org/dev/peps/pep-0008/
#
# Changelog
# 2015-09-23 J. Baten Initial version
#
# Copyright 2015 Deltares
#
# Licensed under the Apache License, Version 2.0 (the "License");
# you may not use this file except in compliance with the License.
# You may obtain a copy of the License at
#
#    http://www.apache.org/licenses/LICENSE-2.0
#
# Unless required by applicable law or agreed to in writing, software
# distributed under the License is distributed on an "AS IS" BASIS,
# WITHOUT WARRANTIES OR CONDITIONS OF ANY KIND, either express or implied.
# See the License for the specific language governing permissions and
# limitations under the License.
# -- coding: UTF-8 --
#encoding:utf-8
_cmdbuild__version = "$Id: 65823ba79d5f98cfc7332bad34f34d6c4c76c29e $"
__author__ = 'Jeroen Baten'
__author__ = 'Jeroen Baten'
__copyright__ = "Copyright 2015, Deltares"

import requests
import json
from pprint import pprint
import logging
import sys
from json import JSONEncoder


# logger = logging.getLogger(__name__)


class cmdbuild:
    """CMDBuild interface class. Please see _dir_ for methods"""

    def version(self):
        """
        Method to print filename and version string
        :return:
        """
        return __file__ + " version: " + __version

    def check_valid_json(self, myjson):
        """Function to check is object passed is valid json
        Argument:
            object  json object to check
        Returns:
            true if valid json, otherwise false
        """
        try:
            json_object = json.dumps(myjson)
        except ValueError, e:
            return False
        return True

    def info(self):
        """Return version information."""
        return "CMDBuild python lib version:" + version

    def connect(self, url, user, password):
        """Method to authenticate to cmdbuild server
        Parameters: url: url of server.
                    user: username to authenticate as.
                    password: password to use when authenticating.
        Returns: 0 if succesfull or 1 for failure.
        """
        if not url:
            raise Exception('ERROR: No URL supplied')

        if not user:
            raise Exception('ERROR: No username supplied')

        if not password:
            raise Exception('ERROR: No password supplied')

        logging.debug("*** Login and get authentication token ")

        cmdbuild_url = url + "/services/rest/v2/sessions/"
        data = {'username': user, 'password': password}
        headers = {'Content-type': 'application/json', 'Accept': '*/*'}
        r = requests.post(cmdbuild_url, data=json.dumps(data), headers=headers)
        # logging.debug((r.json()))
        r1 = r.json()
        sessionid = r1["data"]["_id"]
        # logging.debug("sessionid=" + str(pprint(sessionid)))
        # logging.info(" Authentication token : " + sessionid)

        if (len(str(sessionid)) > 1):
            self.url = url
            self.user = user
            self.password = password
            self.sessionid = sessionid
            return 0
        # else:
        #    return 1
        return 1

    def session_info(self):
        """Return information about the current session in json format"""
        logging.debug("*** Session info")
        cmdbuild_url = self.url + "/services/rest/v2/sessions/" + self.sessionid
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        print headers
        return r.json()


    def lookup_types_info(self):
        """Return list of defined lookup types
           Return: Lookup types found (in json format).
        """
        logging.debug("*** lookup_types")
        cmdbuild_url = self.url + "/services/rest/v2/lookup_types"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results")
        logging.debug(r.json())
        return r.json()

    def lookup_type_values(self, id):
        """Return values for given lookup type
        Argument: id of lookup type.
        Return: list of values found in json format.
        """
        logging.debug("\nTrying to find lookup values for : " + id)
        logging.debug("*** LookupType '" + id + "'")
        cmdbuild_url = self.url + "/services/rest/v2/lookup_types/" + id + "/values"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for lookup_type " + id + "?")
        logging.debug(r.json())
        return r.json()

    def lookup_type_details(self, name, id):
        """Return value for given lookup type id
        Argument: name of lookup type
                  id of lookup type value id.
        Return: All details of lookup type value in json format.
        """
        logging.debug("*** LookupTypeValue name'" + name + "'")
        logging.debug("*** LookupTypeValue id  '" + id + "'")
        cmdbuild_url = self.url + "/services/rest/v2/lookup_types/" + name + "/values/" + id
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def domains_list(self):
        """Return list of domains defined"""
        logging.debug("*** domains")
        cmdbuild_url = self.url + "/services/rest/v2/domains"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.info("There are " + str(r.json()["meta"]["total"]) + " results")
        logging.debug(r.json())
        return r.json()

    def domain_relations(self, id):
        """Return relations of specified domain as json object
        Argument:
            id    id of requested domain
        """
        logging.debug("*** Domain relations of id:'" + id + "'")
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + id + "/relations/"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def domain_relations_with_filter(self, id1, field, value):
        """Return relations of specified domain as json object
        Argument:
            id    id of requested domain
            field   field to filter on
            value   value used in filter
        """
        logging.debug("*** Domains of type " + id1 + " where field '" + field + "' has value '" + str(value) + "'")
        filter = "{\"attribute\":{\"simple\":{\"attribute\":\"" + field + "\",\"operator\":\"equal\",\"value\":[\"" + str(
            value) + "\"]}}}"
        logging.debug("filter looks like: " + filter)
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + id1 + "/relations?filter=" + filter
        # cmdbuild_url = self.url + "/services/rest/v2/domains/" + id1 + "/relations/"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def domain_relation_details(self, name, id1):
        """Return relation details of specified domain as json object
        Argument:
            name    name of domain
            id      id of requested domain relation
        """
        logging.debug("*** Domain relation details of name " + name + " and id " + str(id1))
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + name + "/relations/" + str(id1)
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def domain_details(self, id):
        """Return details of specified domain
        Argument:
            name:  id of domain
        """
        logging.debug("*** Domain '" + id + "' details")
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + id
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def domain_attributes(self, id):
        """Return attributes of specified domain
        Argument:
            name:  id of domain
        """
        logging.debug("*** Domain '" + id + "' attributes")
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + id + "/attributes"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def domain_get_all_with_filter(self, field, value):
        """Return all cards of specified domain and user filter field=value as json object
        Argument:
            field   field to filter on
            value   value used in filter
        """
        logging.debug("*** Domains where field '" + field + "' has value '" + str(value) + "'")
        filter = "{\"attribute\":{\"simple\":{\"attribute\":\"" + field + "\",\"operator\":\"equal\",\"value\":[\"" + str(
            value) + "\"]}}}"
        cmdbuild_url = self.url + "/services/rest/v2/domains?filter=" + filter
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for this domain ")
        logging.debug(r.json())
        return r.json()


        # def domain_get_all_with_filter_2arg(self, field1, value1, oper, field2, value2):
        # """Return all cards of specified class and user filter fiel1=value1 'operator' field2=value2 as json object
        #
        # Argument:
        #     field1   field to filter on
        #     value1   value used in filter
        #     operator operator to use, Either "and" or "or".
        #     field2   field to filter on
        #     value2   value used in filter
        #
        # """
        # example filter code:
        # {
        # "attribute": {
        #     "and": [
        #         {
        #             "or": [
        #                 {
        #                     "simple": {
        #                         "value": [
        #                             146259
        #                         ],
        #                         "attribute": "Gruppo",
        #                         "parameterType": "fixed",
        #                         "operator": "equal"
        #                     }
        #                 },
        #                 {
        #                     "simple": {
        #                         "value": [
        #                             3941634
        #                         ],
        #                         "attribute": "Gruppo",
        #                         "parameterType": "fixed",
        #                         "operator": "equal"
        #                     }
        #                 }
        #             ]
        #         },
        # TODO: Do we really need this routine?
        # logging.debug("*** Domains where field1 '" + field1 + "' has value1 '" + str(value1) + "'")
        # logging.debug("*** and the operator is \'"+str(oper)+"\"")
        # logging.debug("*** where field2 '" + field2 + "' has value2 '" + str(value2) + "'")
        # filter="{\"attribute\":{ \"" + oper + "\" : [ "
        # filter = filter + "{" + "\"simple\":{\"attribute\":\"" + field1 + "\",\"operator\":\"equal\",\"value\":[\"" + str(value1) + "\"]}}"
        # filter = filter + ","
        # filter = filter +"{" +"\"simple\":{\"attribute\":\"" + field2 + "\",\"operator\":\"contain\",\"value\":[\"" + str(value2) + "\"]}}"
        # filter = filter + "] } }"
        # logging.debug("filter looks like: "+filter)
        # cmdbuild_url = self.url + "/services/rest/v2/domains?filter="+filter
        # headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        # r = requests.get(cmdbuild_url,  headers=headers)
        # if not r.status_code // 100 == 2:
        #     return "Error: Unexpected response {}".format(r)
        # logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for this domain ")
        # logging.debug(r.json())
        # return r.json()

    def domain_relation_get_all_with_filter(self, domain, field, value):
        """Return all cards of specified class and user filter field=value as json object
        Argument:
            domain  domain type to apply filter on
            field   field to filter on
            value   value used in filter
        """

        # werkende code in bash:
        # cmdbuild_url = "http://tl-218.xtr.deltares.nl:8080/cmdbuild/services/rest/v2/domains/" + id + "/relations"
        # headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': sessionid }
        # = requests.get(cmdbuild_url, data=json.dumps(data), headers=headers)

        logging.debug("*** Domains '" + domain + "' where relation '" + field + "' has value '" + str(value) + "'")
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + domain + "/relations?filter={\"attribute\":{\"simple\":{\"attribute\":\"" + field + "\",\"operator\":\"equal\",\"value\":[\"" + str(
            value) + "\"]}}}"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        # logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for this domain ")
        logging.debug(r.json())
        return r.json()

    def classes_list(self):
        """Return list of available classes"""
        logging.debug("*** Classes ")
        cmdbuild_url = self.url + "/services/rest/v2/classes"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results")
        logging.debug(r.json())
        return r.json()

    def classes_total(self):
        """Return list of available classes"""
        logging.debug("*** Classes ")
        cmdbuild_url = self.url + "/services/rest/v2/classes"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        print r.status_code
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results")
        logging.debug(str(r.json()["meta"]["total"]))
        return (r.json()["meta"]["total"])

    def class_details(self, id1):
        """Return details of specified class as json object
        Argument:
            id    id of requested class
        """
        logging.debug("*** Class details of id:'" + id1 + "'")
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + id1
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def class_get_attributes_of_type(self, id):
        """Return attributes of specified class as json object
        Argument:
            id    id of requested class
        """
        logging.debug("*** Class  '" + id + "' attributes")
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + id + "/attributes"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for class " + id + " attributes ")
        logging.debug(r.json())
        return r.json()

    def class_get_all_cards_of_type(self, typ):
        """Return all cards of specified class as json object
        Argument:
            type    type of requested class
        """
        logging.debug("*** Class  of type '" + typ + "' cards")
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + typ + "/cards"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for class of type " + typ + " cards ")
        logging.debug(r.json())
        return r.json()

    def class_get_all_cards_of_type_with_filter(self, typ, field, value):
        """Return all cards of specified class and user filter field=value as json object
        Argument:
            type    type of requested class
            field   field to filter on
            value   value used in filter

        """
        logging.debug(
            "*** Class  of type '" + typ + "' cards where field '" + field + "' has value '" + str(value) + "'")
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + typ + "/cards?filter={\"attribute\":{\"simple\":{\"attribute\":\"" + field + "\",\"operator\":\"equal\",\"value\":[\"" + str(
            value) + "\"]}}}"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for class of type " + typ + " cards ")
        logging.debug(r.json())
        return r.json()

    def class_get_all_cards_of_type_with_filter_like(self, typ, field, value):
        """Return all cards of specified class and user filter field like value as json object
        Argument:
            type    type of requested class
            field   field to filter on
            value   value used in filter
        """
        logging.debug(
            "*** Class  of type '" + typ + "' cards where field '" + field + "' has value '" + str(value) + "'")
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + typ + "/cards?filter={\"attribute\":{\"simple\":{\"attribute\":\"" + field + "\",\"operator\":\"like\",\"value\":[\"" + str(
            value) + "\"]}}}"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug("There are " + str(r.json()["meta"]["total"]) + " results for class of type " + typ + " cards ")
        logging.debug(r.json())
        return r.json()

    def class_get_card_details(self, type, id1):
        """Return all cards of specified class as json object
        Argument:
            type    type of requested class
            id      id of requested card
        """
        logging.debug("*** Class  '" + type + "' card details " + str(id1))
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + str(type) + "/cards/" + str(id1)
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def class_update_card(self, type, id1,carddata):
        """Return all cards of specified class as json object
        Argument:
            type    type of requested class
            id      id of requested card
        """
        logging.debug("*** Class  '" + type + "' card details " + str(id1))
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + str(type) + "/cards/" + str(id1)
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.put(cmdbuild_url, data=carddata, headers=headers)
        # if not r.status_code // 100 == 2:
        #     return "Error: Unexpected response {}".format(r)
        # logging.debug(r.json())
        return 0

    def class_delete_card(self, type, id1):
        """Return all cards of specified class as json object
        Argument:
            type    type of requested class
            id      id of requested card
        """
        logging.debug("*** Class  '" + type + "' card details " + str(id1))
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + str(type) + "/cards/" + str(id1)
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.delete(cmdbuild_url, headers=headers)
        # if not r.status_code // 100 == 2:
        #     return "Error: Unexpected response {}".format(r)
        # logging.debug(r.json())
        return 0

    def class_insert_card(self, cardtype, cardobject):
        """Insert card with name into cmdbuild
        Arguments:
            name    name of card
            object  json object with all relevant parameters
        Returns
            id of object created in JSON format
            error message when second argument is not a valid JSON object
        """
        if (self.check_valid_json(cardobject)):
            logging.debug(
                "Inserting card of type " + str(cardtype) + " and with object:" + str(pprint(json.dumps(cardobject))))
            cmdbuild_url = self.url + "/services/rest/v2/classes/" + str(cardtype) + "/cards/"
            headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
            try:
                r = requests.post(cmdbuild_url, data=cardobject, headers=headers)
                print r.status_code
                if not r.status_code // 100 == 2:
                    return "Error: Unexpected response {}".format(r)
                logging.debug(r.json())
                print r.json()
                return r.json()
            except requests.exceptions.RequestException as e:
                logging.debug('HTTP ERROR %s occured' % e.code)
                logging.debug(e)
                return e
        else:
            return "Second argument is not a valid JSON object"

    def get_by_type_and_id(self, typ, id1):
        """Retrieve Card or Class by id
        Arguments
            classid    id of requested classtype
            cardtype   type of card to request
            cardid     id of requested card
        """
        logging.debug("*** get Card(s) by type = " + str(typ) + " and id = " + str(id1))
        cmdbuild_url = self.url + "/services/rest/v2/classes/" + str(typ) + "/cards/" + str(id1) + "/"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def get_by_domaintype_and_id(self, typ, id1):
        """Retrieve Card or Class by id
        Arguments
            classid    id of requested classtype
            cardtype   type of card to request
            cardid     id of requested card
        """
        logging.debug("*** get domain(s) by type = " + str(typ) + " and id = " + str(id1))
        cmdbuild_url = self.url + "/services/rest/v2/domains/" + str(typ) + "/" + str(id1) + "/"
        headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        r = requests.get(cmdbuild_url, headers=headers)
        if not r.status_code // 100 == 2:
            return "Error: Unexpected response {}".format(r)
        logging.debug(r.json())
        return r.json()

    def get_id(self, uuid):
        cards = self.class_get_all_cards_of_type('virtual_machine')
        _id = None
        for i in range(0,len(cards['data'])):
            if uuid == cards['data'][i].get('uuid'):
                print cards['data'][i]
                _id = cards['data'][i].get('_id')
        return _id


        # return 1
        # <resource path="{attachmentId}/">
        # <resource path="{attachmentId}/{file: [^/]+}">
        # <resource path="{cardId}/">
        # <resource path="{classId}/">
        # <resource path="{classId}/">
        # <resource path="{domainId}/">
        # <resource path="{id}/">
        # <resource path="{relationId}/">
        # <resource path="{username}/">
        # <resource path="{lookupTypeId}/">
        # <resource path="{lookupValueId}/">
        # <resource path="{processId}/">
        # <resource path="{processId}/generate_id">
        # <resource path="{processActivityId}/">
        # <resource path="{attachmentId}/">
        # <resource path="{attachmentId}/{file: [^/]+}">
        # <resource path="{emailId}/">
        # <resource path="{processInstanceId}">
        # <resource path="{processActivityId}">
        # <resource path="{reportId}/">
        # <resource path="{reportId}/attributes/">
        # <resource path="{reportId}/{file: [^/]+}">
        # <resource path="{id}/">

        # logging.debug("*** Get object with id "+ str(id1) )
        # cmdbuild_url = self.url + "/services/rest/v1/"+ str(id1)+"/"
        # headers = {'Content-type': 'application/json', 'Accept': '*/*', 'CMDBuild-Authorization': self.sessionid}
        # r = requests.get(cmdbuild_url,  headers=headers)
        # if not r.status_code // 100 == 2:
        #     return "Error: Unexpected response {}".format(r)
        # logging.debug(r)
        # return r



data =JSONEncoder().encode({
    # 'site':'顺义测试',
    # # 'unit':'',
    # # 'position':'',
    # 'Mtype':'Vmware测试',
    # # 'MN':'',
    # # 'SN':'',
    # # 'WTY':'',
    # 'IP':'10.16.2.18',
    # 'OS':'Windows XP',
    # 'status':'使用中',
    # 'service':'开发测试',
    # 'usage':'CMDB',
    # 'consumer':'张凯',
    # 'host_ip':'10.10.0.0',
    # 'Mname':'',
    # 'memo':''
    'Mname': 'test',
    'IP': '10.10.10.10.',
    'type': 'Vmware测试',
    'status': '开机',
    'host_ip': '10.0.1.1',
    'os': 'rhel',
    'service': '哈哈哈',
    'usage': '呵呵呵',
    'admin': '邵衡',
    'environment': 'Vmware测试',
    'memo': '测试数据'
})
data1 = JSONEncoder().encode({
    'IPsec': '192.168.3.0',
    # 'usage':'OA'
})

data2 = JSONEncoder().encode({
    'IP': '10.16.2.18',
    'usage': 'CMDBuild',
    'status': '使用中'
})
test = cmdbuild()
test.connect('http://10.7.1.1', 'zhangk', 'zhangk')
id = test.get_id("42296a95-eacc-6316-6b35-b7c68f57c0ff")
print id
# test.class_insert_card('virtual_machine', data)
test.class_update_card('virtual_machine', 32043, data1)
# test.class_delete_card('server',)
# print test.classes_list()
# print test.class_details("IP")
# print test.class_get_all_cards_of_type('IPsec')
# print test.class_get_all_cards_of_type('server')
