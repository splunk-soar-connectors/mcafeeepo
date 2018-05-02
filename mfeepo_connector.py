# --
# File: mfeepo_connector.py
#
# Copyright © 2016-2018 Splunk Inc.
#
# SPLUNK CONFIDENTIAL – Use or disclosure of this material in whole or in part
# without a valid written license from Splunk Inc. is PROHIBITED.
# --

# Phatom imports
import phantom.app as phantom
from phantom.base_connector import BaseConnector
from phantom.action_result import ActionResult


# Local imports
from mfeepo_consts import *

import simplejson as json

import threading
import time
import ssl

# McAfee import
import os
os.sys.path.insert(0, '{}/mcafee'.format(os.path.dirname(os.path.abspath(__file__))))  # noqa
import mcafee


class EpoConnector(BaseConnector):

    ACTION_ID_ADD_TAG = "add_tag"
    ACTION_ID_REMOVE_TAG = "remove_tag"
    ACTION_ID_GET_DEVICE_INFO = "get_device_info"
    ACTION_ID_QUARANTINE_DEVICE = "quarantine_device"
    ACTION_ID_UNQUARANTINE_DEVICE = "unquarantine_device"

    def __init__(self):

        self._mc_client = None

        self._lock = threading.Lock()
        self._done = False  # Is it done waking up agent?

        super(EpoConnector, self).__init__()
        return

    def _connect_to_epo(self):
        """ Try to establish connection with ePO
        """
        conf = self.get_config()
        host = conf[EPO_JSON_HOST]
        port = conf[EPO_JSON_PORT]
        username = conf[EPO_JSON_USERNAME]
        password = conf[EPO_JSON_PASSWORD]

        if not conf.get(phantom.APP_JSON_VERIFY):
            # The mcafee.py file does a request using just URL lib
            # This will generate SSL warnings when connecting to an unverified server
            # This monkeypatch will solve that problem
            ssl._create_default_https_context = ssl._create_unverified_context

        self.save_progress("Attempting to connect to ePO")
        try:
            self._mc_client = mcafee.client(host, port, username, password)
        except Exception as e:
            return self.set_status_save_progress(phantom.APP_ERROR, str(e))

        return self.set_status_save_progress(phantom.APP_SUCCESS, "Created client")

    def _check_tag(self, tags, tag):
        """ Check if tag is present in tags
          " Tags is expected to be a string, like "tag1, tag2..."
        """
        # Convert tags to a list from a string
        tags = [x.strip() for x in tags.split(',')]
        if tag in tags:
            return True
        else:
            return False

    def _transmogrify_dict(self, x):
        """ Turn the tags from the literal string "tag1, tag2,...
          "  into a list
          " Replace periods w/ underscores in key names
        """
        try:
            x[KEY_TAGS] = [{"Tag": v.strip()} for v in x[KEY_TAGS].split(',')]
            x[KEY_ETAGS] = [{"Tag": v.strip()} for v in x[KEY_ETAGS].split(',')]
        except:  # Something went wrong. Probably the wrong dictionary
            pass
        return dict((k.replace('.', '_'), v) for k, v in x.iteritems())

    def _test_connectivity(self, param):

        status_code = self._connect_to_epo()

        if (phantom.is_fail(status_code)):
            return self.set_status_save_progress(phantom.APP_ERROR, "Unable to connect to ePO")

        return self.set_status_save_progress(phantom.APP_SUCCESS, "Connectivity test passed")

    def _wakeup_agent(self, action_result, host):

        self.save_progress("Attempting to wake up agent")
        thread = threading.Thread(target=self._wait_for_wakeup)
        thread.start()
        try:
            ret_val = self._mc_client.system.wakeupAgent(host)
        except Exception as e:
            self._join_thread(thread)
            self.set_status(phantom.APP_ERROR)
            return action_result.set_status(phantom.APP_ERROR, str(e))

        self._join_thread(thread)
        if (ret_val == 0):
            self.set_status(phantom.APP_ERROR)
            return action_result.set_status(phantom.APP_ERROR, "Failed to wakeup agent")
        else:
            return action_result.set_status(phantom.APP_SUCCESS, "Successfully woke up agent")

    def _join_thread(self, thread):
        self._lock.acquire()
        self._done = True
        self._lock.release()
        thread.join()
        return

    def _wait_for_wakeup(self):
        """ Keep message updated while waking up host
        """
        i = 0
        while True:
            self._lock.acquire()
            if (self._done):
                self._lock.release()
                break
            self.send_progress("Attempting to wake up agent" + "." * i)
            self._lock.release()
            i = i % 5 + 1
            time.sleep(1)
        return

    def _validate_tag(self, action_result, host, tag):
        """ Validate that a tag exists
          " Also, fix the case of the tag
        """
        try:
            tag_dicts = self._mc_client.system.findTag(tag)
        except Exception as e:
            self.set_status(phantom.APP_ERROR)
            action_result.set_status(phantom.APP_ERROR, str(e))
            return action_result, None

        for tag_dict in tag_dicts:
            if (tag_dict['tagName'].lower() == tag.lower()):
                action_result.set_status(phantom.APP_SUCCESS)
                return action_result, tag_dict['tagName']

        # Couldn't find tag
        self.set_status(phantom.APP_ERROR)
        action_result.set_status(phantom.APP_ERROR, "There is no tag: {}".format(tag))
        return action_result, None

    def _add_tag(self, param):
        """ Actual handler for add_tag action
        """
        return self.__add_tag(param)

    def _quarantine_device(self, param):
        return self.__add_tag(param, quarantine=True)

    def __add_tag(self, param, quarantine=False):

        action_result = self.add_action_result(ActionResult(dict(param)))

        status_code = self._connect_to_epo()

        if (phantom.is_fail(status_code)):
            return action_result.set_status(phantom.APP_ERROR, self.get_status_message())

        host = param[EPO_JSON_HOST]  # Endpoint to add tag to
        wakeup_agent = param.get(EPO_JSON_WAKEUP_AGENT, False)
        if (quarantine):
            tag = self.get_config().get(EPO_JSON_QTAG, "")
            if (not tag):
                self.set_status(phantom.APP_ERROR)
                return action_result.set_status(phantom.APP_ERROR, "Need to set quarantine tag")
        else:
            tag = param[EPO_JSON_TAG]

        action_result, tag = self._validate_tag(action_result, host, tag)

        # Tag doesn't exist
        if (phantom.is_fail(action_result.get_status())):
            return action_result.get_status()

        action_result, r_dict = self._find(action_result, host)

        # Host doesn't exist
        if (phantom.is_fail(action_result.get_status())):
            return action_result.get_status()

        # Endpoint already has tag
        if (self._check_tag(r_dict[KEY_TAGS], tag)):
            return action_result.set_status(phantom.APP_SUCCESS, "Success, tag already added")

        action_result = self._apply_tag(action_result, host, tag)

        if (not wakeup_agent or phantom.is_fail(action_result.get_status())):
            return action_result.get_status()

        ret_val = self._wakeup_agent(action_result, host)

        if (phantom.is_fail(ret_val)):
            return action_result.set_status(phantom.APP_ERROR,
                    "Assigned tag but host did not recieve configuration")

        return action_result.set_status(phantom.APP_SUCCESS,
                "Assigned tag and host received configuration")

    def _apply_tag(self, action_result, host, tag):

        try:
            ret_val = self._mc_client.system.applyTag(host, tag)
        except:  # Something went wrong
            self.set_status(phantom.APP_ERROR)
            action_result.set_status(phantom.APP_ERROR, "Failed to assign tag")
            return action_result

        if (ret_val == 0):  # Something else went wrong
            self.set_status(phantom.APP_ERROR)
            action_result.set_status(phantom.APP_SUCCESS, "Failed to assign tag")
        else:
            action_result.set_status(phantom.APP_SUCCESS, "Successfully assigned tag")

        return action_result

    def _remove_tag(self, param):
        """ actual handler for remove_tag action
        """
        return self.__remove_tag(param)

    def _unquarantine_device(self, param):
        return self.__remove_tag(param, quarantine=True)

    def __remove_tag(self, param, quarantine=False):

        action_result = self.add_action_result(ActionResult(dict(param)))

        status_code = self._connect_to_epo()

        if (phantom.is_fail(status_code)):
            return action_result.set_status(phantom.APP_ERROR, self.get_status_message())

        host = param[EPO_JSON_HOST]  # Endpoint to remove tag from
        wakeup_agent = param.get(EPO_JSON_WAKEUP_AGENT, False)
        if (quarantine):
            tag = self.get_config().get(EPO_JSON_QTAG, "")
            if (not tag):
                self.set_status(phantom.APP_ERROR)
                return action_result.set_status(phantom.APP_ERROR, "Need to set quarantine tag")
        else:
            tag = param[EPO_JSON_TAG]

        action_result, tag = self._validate_tag(action_result, host, tag)

        # Tag doesn't exist
        if (phantom.is_fail(action_result.get_status())):
            return action_result.get_status()

        action_result, r_dict = self._find(action_result, host)

        # Host doesn't exist
        if (phantom.is_fail(action_result.get_status())):
            return action_result.get_status()

        # Endpoint already has tag
        if (not self._check_tag(r_dict[KEY_TAGS], tag)):
            return action_result.set_status(phantom.APP_SUCCESS, "Success, tag not present")

        action_result = self._clear_tag(action_result, host, tag)

        if (not wakeup_agent or phantom.is_fail(action_result.get_status())):
            return action_result.get_status()

        ret_val = self._wakeup_agent(action_result, host)

        if (phantom.is_fail(ret_val)):
            return action_result.set_status(phantom.APP_ERROR,
                    "Removed tag but host did not recieve configuration")

        return action_result.set_status(phantom.APP_SUCCESS,
                "Removed tag and host received configuration")

    def _clear_tag(self, action_result, host, tag):

        try:
            ret_val = self._mc_client.system.clearTag(host, tag)
        except:
            self.set_status(phantom.APP_ERROR)
            action_result.set_status(phantom.APP_ERROR, "Failed to remove tag")
            return action_result

        if (ret_val == 0):
            self.set_status(phantom.APP_ERROR)
            action_result.set_status(phantom.APP_ERROR, "Failed to remove tag")
        else:
            action_result.set_status(phantom.APP_SUCCESS, "Successfully removed tag")

        return action_result

    def _get_device_info(self, param):

        action_result = self.add_action_result(ActionResult(dict(param)))

        status_code = self._connect_to_epo()

        if (phantom.is_fail(status_code)):
            return action_result.set_status(phantom.APP_ERROR, self.get_status_message())

        host = param[EPO_JSON_HOST]  # Endpoint to get info from

        action_result, r_dict = self._find(action_result, host)

        if (phantom.is_fail(action_result.get_status())):
            return action_result.get_status()

        config = self.get_config()
        r_dict = self._transmogrify_dict(r_dict)
        r_dict['EPO_IP/Hostname'] = config[EPO_JSON_HOST]
        r_dict['EPO_Port'] = config[EPO_JSON_PORT]
        action_result.add_data(r_dict)
        return action_result.get_status()

    def _find(self, action_result, host):
        """ Get device info and add it to action result
          " Also used to confirm that device exists / is connectable
        """
        try:
            # result is a list of matching hosts
            result = self._mc_client.system.find(host)
        except Exception as e:
            self.set_status(phantom.APP_ERROR)
            action_result.set_status(phantom.APP_ERROR, str(e))
            return action_result, None

        for r in result:
            if (r[IP_ADDR] == host or r[NAME].lower() == host.lower()):
                action_result.set_status(phantom.APP_SUCCESS, "Successfully retrieved device info")
                return action_result, r

        self.set_status(phantom.APP_ERROR)
        action_result.set_status(phantom.APP_ERROR, "Failed to locate host")
        return action_result, None

    def handle_action(self, param):

        action = self.get_action_identifier()
        ret_val = phantom.APP_SUCCESS

        if (action == phantom.ACTION_ID_TEST_ASSET_CONNECTIVITY):
            ret_val = self._test_connectivity(param)
        elif (action == self.ACTION_ID_ADD_TAG):
            ret_val = self._add_tag(param)
        elif (action == self.ACTION_ID_REMOVE_TAG):
            ret_val = self._remove_tag(param)
        elif (action == self.ACTION_ID_GET_DEVICE_INFO):
            ret_val = self._get_device_info(param)
        elif (action == self.ACTION_ID_QUARANTINE_DEVICE):
            ret_val = self._quarantine_device(param)
        elif (action == self.ACTION_ID_UNQUARANTINE_DEVICE):
            ret_val = self._unquarantine_device(param)

        return ret_val


if __name__ == '__main__':
    # Imports
    import sys
    import pudb

    # Breakpoint at runtime
    pudb.set_trace()

    # The first param is the input json file
    with open(sys.argv[1]) as f:

        # Load the input json file
        in_json = f.read()
        in_json = json.loads(in_json)
        print(json.dumps(in_json, indent=' ' * 4))

        # Create the connector class object
        connector = EpoConnector()

        # Se the member vars
        connector.print_progress_message = True

        # Call BaseConnector::_handle_action(...) to kickoff action handling.
        ret_val = connector._handle_action(json.dumps(in_json), None)

        # Dump the return value
        print ret_val

    exit(0)
