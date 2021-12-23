import os
import sys
import yaml
import uuid
import unittest
import tempfile

sys.path.append(".")

from ghascompliance.policies.policy import Policy
from ghascompliance.utils.octouri import OctoUri


class TestPolicyLoading(unittest.TestCase):
    def setUp(self):
        self.policy = Policy("error", uri=OctoUri())
        return super().setUp()

    def testNotMatchContent(self):
        wildcards = ["example-*"]

        item = "test"

        result = self.policy.matchContent(item, wildcards)
        self.assertFalse(result)

    def testMatchBasicContent(self):
        wildcards = ["example", "test"]

        item = "test"

        result = self.policy.matchContent(item, wildcards)
        self.assertTrue(result)

    def testNotMatchWildcardContent(self):
        wildcards = ["example-*"]

        item = "example"

        result = self.policy.matchContent(item, wildcards)
        self.assertFalse(result)

    def testMatchWildcardContent(self):
        wildcards = ["example-*"]

        item = "example-test"

        result = self.policy.matchContent(item, wildcards)
        self.assertTrue(result)

    def testLoadingAndMatching(self):
        policy_path = "tests/samples/wildcards.yml"
        self.assertTrue(os.path.exists(policy_path))

        engine = Policy("error", OctoUri(path=policy_path))

        ids = engine.policy.licensing.conditions.ids
        # lowercase
        self.assertEqual(ids, ["*-examples", "mylicencing-*"])

        self.assertFalse(engine.checkLicensingViolation("MyLicencing"))
        self.assertTrue(engine.checkLicensingViolation("MyLicencing-1.0"))

        self.assertTrue(engine.checkLicensingViolation("Test-Examples"))


class TestDefaultPolicyWildcards(unittest.TestCase):
    def setUp(self):
        self.policy = Policy(uri=OctoUri(path="ghascompliance/defaults/policy.yml"))
        return super().setUp()

    def testDefault(self):
        ids = self.policy.policy.licensing.conditions.ids
        self.assertEqual(ids, ["gpl-*", "lgpl-*", "agpl-*"])

    def testGPLVariants(self):
        self.assertTrue(self.policy.checkLicensingViolation("GPL-2.0"))
        self.assertTrue(self.policy.checkLicensingViolation("GPL-3.0"))
        self.assertTrue(self.policy.checkLicensingViolation("LGPL-2.0"))
        self.assertTrue(self.policy.checkLicensingViolation("LGPL-3.0"))
        self.assertTrue(self.policy.checkLicensingViolation("LGPL-3.0 License"))
