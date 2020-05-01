import sys

import speedtest


def speed(progress_callback=None):
    servers = []
    # If you want to test against a specific server
    # servers = [1234]

    threads = None
    # If you want to use a single threaded test
    # threads = 1

    sys.stdout.write('Tests en cours, veuillez patienter ...')

    s = speedtest.Speedtest()
    s.get_servers(servers)
    s.get_best_server()
    s.download(threads=threads)
    s.upload(threads=threads)
    s.results.share()

    sys.stdout.write('\r')
    sys.stdout.flush()

    results_dict = s.results.dict()  # Resultats format dictionnaire

    return results_dict


if __name__ == "__main__":
    print(speed())
