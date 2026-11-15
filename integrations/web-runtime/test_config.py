"""Test installer defaults; real runtime acceptance is a separate Docker job."""
import json
from pathlib import Path
import subprocess
import sys
import unittest
import manage

class InstallerTests(unittest.TestCase):
    def test_no_host_files_or_docker_socket(self):
        service=manage.configuration()['services']['runtime']
        self.assertEqual(service['volumes'],['state:/state','workspace:/workspace'])
        self.assertNotIn('ports',service)
        self.assertNotIn('privileged',service)
    def test_no_public_tunnel_by_default(self):
        self.assertEqual(manage.configuration()['services']['runtime']['environment']['PUBLIC_BASE_URL'],'http://127.0.0.1:8766')
    def test_network_disabled_in_ci(self):
        self.assertEqual(manage.configuration(offline=True)['services']['runtime']['network_mode'],'none')
    def test_public_mode_is_explicit(self):
        self.assertEqual(manage.configuration(public=True)['services']['runtime']['environment']['PUBLIC_BASE_URL'],'')
        with self.assertRaises(ValueError): manage.configuration(public=True,offline=True)
    def test_connect_without_approval_does_not_call_docker(self):
        result=subprocess.run([sys.executable,str(Path(manage.__file__)),'connect'],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,1)
        self.assertIn('No change was made',result.stderr)
    def test_owner_key_is_not_printed_to_pipe(self):
        result=subprocess.run([sys.executable,str(Path(manage.__file__)),'owner-key'],capture_output=True,text=True,timeout=10)
        self.assertEqual(result.returncode,1)
        self.assertEqual(result.stdout,'')
    def test_versions_are_exact(self):
        self.assertRegex(manage.SHA,r'^[a-f0-9]{40}$')
        self.assertNotIn('latest',manage.IMAGE)
    def test_resource_caps(self):
        service=manage.configuration()['services']['runtime']
        self.assertTrue(service['read_only'])
        self.assertEqual(service['cap_drop'],['ALL'])
        self.assertEqual(service['pids_limit'],256)

if __name__=='__main__': unittest.main()
