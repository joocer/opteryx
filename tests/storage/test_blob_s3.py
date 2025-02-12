"""
Test we can read from S3
"""
import os
import sys

sys.path.insert(1, os.path.join(sys.path[0], "../.."))

import opteryx

from opteryx.connectors import AwsS3Connector

from tests.tools import skip_if, is_arm, is_windows, is_mac

BUCKET_NAME = "mabellabs"
SECRETS = None


@skip_if(is_arm() or is_windows() or is_mac())
def test_minio_storage():
    opteryx.register_store(BUCKET_NAME, AwsS3Connector)

    conn = opteryx.connect()

    # SELECT EVERYTHING
    cur = conn.cursor()
    cur.execute(f"SELECT * FROM {BUCKET_NAME}.space_missions WITH(NO_PARTITION);")
    assert cur.rowcount == 4630, cur.rowcount

    # PROCESS THE DATA IN SOME WAY
    cur = conn.cursor()
    cur.execute(
        f"SELECT COUNT(*) AS Missions, Company FROM {BUCKET_NAME}.space_missions WITH(NO_PARTITION) GROUP BY Company;"
    )
    assert cur.rowcount == 62, cur.rowcount

    conn.close()


if __name__ == "__main__":  # pragma: no cover
    test_minio_storage()
    print("✅ okay")
