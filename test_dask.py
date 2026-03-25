from dask.distributed import Client, LocalCluster

def main():
    cluster = LocalCluster(n_workers=4, threads_per_worker=1)
    client = Client(cluster)
    print(client.dashboard_link)   # should print a localhost URL
    client.close()
    cluster.close()

if __name__ == "__main__":
    main()