EXECUTABLE=runcdd
WINDOWS=$(EXECUTABLE)_windows_amd64.exe
LINUX=$(EXECUTABLE)_linux_amd64
DARWIN=$(EXECUTABLE)_darwin_amd64

windows: $(WINDOWS) ## Build for Windows

linux: $(LINUX) ## Build for Linux

darwin: $(DARWIN) ## Build for Darwin (macOS)

#$(WINDOWS):
#	env GOOS=windows GOARCH=amd64 go build -i -v -o $(WINDOWS) -ldflags="-s -w"  main.go

$(LINUX):
	env GOOS=linux GOARCH=amd64 go build -i -v -o $(LINUX) -ldflags="-s -w" main.go

$(DARWIN):
	env GOOS=darwin GOARCH=amd64 go build -i -v -o $(DARWIN) -ldflags="-s -w" main.go
