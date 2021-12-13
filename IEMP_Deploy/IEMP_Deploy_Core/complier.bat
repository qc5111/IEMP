set GOARCH=amd64
set GOOS=windows
go build -ldflags="-w -s" -o IEMP.deployment.windows.amd64.exe main.go
set GOARCH=amd64
set GOOS=linux
go build -ldflags="-w -s" -o IEMP.deployment.linux.amd64 main.go
set GOARCH=arm64
set GOOS=linux
go build -ldflags="-w -s" -o IEMP.deployment.linux.arm64 main.go
set GOARCH=arm64
set GOOS=android
go build -ldflags="-w -s" -o IEMP.deployment.android.arm64 main.go