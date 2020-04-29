from labradio.network.network import Network

n = Network()

print("IP Locale:\t\t" + n.local_ip)
print("IP Publique:\t" + n.get_public_ip())

n.speedtest()

print("Download:\t\t" + n.get_download(string=1) + " Mb/s")
print("Upload:\t\t\t" + n.get_upload(string=1) + " Mb/s")

