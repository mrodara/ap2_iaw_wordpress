"""Validate service connectivity through Docker Compose's public config command."""

import json
from pathlib import Path
import subprocess
import unittest


ROOT = Path(__file__).resolve().parents[1]


class ComposeNetworkTests(unittest.TestCase):
    def test_database_clients_share_the_database_network(self):
        result = subprocess.run(
            ["docker", "compose", "--env-file", "env.example", "config", "--format", "json"],
            cwd=ROOT,
            capture_output=True,
            text=True,
            check=False,
        )
        self.assertEqual(result.returncode, 0, result.stderr)
        self.assertEqual(result.stderr, "")
        services = json.loads(result.stdout)["services"]
        for name in ("db", "web", "phpmyadmin"):
            with self.subTest(service=name):
                self.assertEqual(set(services[name]["networks"]), {"lamp"})
        phpmyadmin = services["phpmyadmin"]
        self.assertEqual(phpmyadmin["environment"]["PMA_HOST"], "db")
        self.assertEqual(str(phpmyadmin["environment"]["PMA_PORT"]), "3306")
        self.assertEqual(phpmyadmin["depends_on"]["db"]["condition"], "service_healthy")
        self.assertTrue(any(
            str(port["published"]) == "8081" and port["target"] == 80
            for port in phpmyadmin["ports"]
        ))


if __name__ == "__main__":
    unittest.main()
