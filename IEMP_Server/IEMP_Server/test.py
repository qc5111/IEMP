import zstd
data = "41668454685987454758745458589548643485268521784518554547985485458".encode()
cdata = zstd.compress(data, 1)
print(len(data),data)
print(len(cdata),cdata)