EXECUTABLE=function
all:
	env GOOS=linux GOARCH=amd64 go build -i -v -o $(EXECUTABLE) -ldflags="-s -w" main.go