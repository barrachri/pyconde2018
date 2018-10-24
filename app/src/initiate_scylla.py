from cassandra.cluster import Cluster


if __name__ == "__main__":
    cluster = Cluster()
    session = cluster.connect()

    session.execute(
        "CREATE KEYSPACE devices WITH replication = {'class': 'SimpleStrategy', 'replication_factor' : 1}"
    )

    session.execute("USE devices")

    session.execute(
        "CREATE TABLE devices (deviceid uuid, timestamp timestamp, data text, PRIMARY KEY (deviceid, timestamp)) WITH compaction = { 'class' : 'LeveledCompactionStrategy' }"
    )

    cluster.shutdown()
