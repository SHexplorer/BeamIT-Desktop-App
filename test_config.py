import unittest

import util

class TestConfig(unittest.TestCase):
    def testStoreAndGetConfig(self):
        serverurl = "https://www.test.url:1234"
        username = "testuser"
        devicename = "testdevice"
        devicetoken = "T-123456HWS"
        filepath = "C:/test/testpath"
        autoOpen = True
        
        self.assertTrue(util.storeConfig(serverurl=serverurl, username=username, devicename=devicename, devicetoken=devicetoken, filepath=filepath, autoOpen=autoOpen), "Config was not stored")

        config = util.getConfig()
        self.assertEqual(config['serverurl'], "https://www.test.url:1234", "Serverurl not stored propery")
        self.assertEqual(config['username'], "testuser", "Username not stored propery")
        self.assertEqual(config['devicename'], "testdevice", "Devicename not stored propery")
        self.assertEqual(config['devicetoken'], "T-123456HWS", "Token not stored propery")
        self.assertEqual(config['filepath'], "C:/test/testpath", "Filepath not stored propery")
        self.assertEqual(config['autoOpen'], "True", "Filepath not stored propery")


if __name__ == '__main__':
    unittest.main()